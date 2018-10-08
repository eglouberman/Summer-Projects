#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:49:23 2018
@author: elonglouberman
"""

from scipy.misc import imread
import os
import json
import sys
import pprint
import re
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

session = Session(profile_name="default")
polly = session.client("polly")

def synthesize_speech(text):
        ###actual synthesis of speech!
        ssml = text[1]
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=ssml, OutputFormat="mp3",
                                                VoiceId= "Joanna")
        except:
            pass
#        (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
#            print(error)
#            sys.exit(-1)
        
        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important as the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            slide = "../audios/" + text[0] + ".mp3"
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(os.getcwd(), slide)
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)
        
        # Play the audio using the platform's default player
#        if sys.platform == "win32":
#            os.startfile(output)
#        else:
#            # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
#            opener = "open" if sys.platform == "darwin" else "xdg-open"
#            subprocess.call([opener, output])
def main():
    pp = pprint.PrettyPrinter(indent=4)
    ##assuming we have all the pdfs already downloaded, lets extract the figures and captions from them!
    pdf_names = []
    png_names =[]
    #finds pdf names and downloads json and images. 
    for files, roots, directories in os.walk("../pdfs/"):
        for x in directories:
            if (x.endswith(".pdf")):
                pdf_names.append(x)
    for x in pdf_names: 
        cmd ="sbt \"runMain org.allenai.pdffigures2.FigureExtractorBatchCli ../pdfs/" +x+" -g ../jsons/ -m ../images/\""
        os.system(cmd)
    
    # finds the images and downloads information to an image array
    for files, roots, directories in os.walk("../images/"):
        for x in directories:
            if (x.endswith(".png")):
                png_names.append(x)

    img_set =[]
    for x in png_names:
        img = imread('../images/' + x)
        img_set.append([x,img])
    
    
    # finds json information and loads it into a caption array
    json_data =[]
    for files, roots, directories in os.walk("../jsons/"):
        for x in directories:
            if (x.endswith(".json")):
                with open("../jsons/" +x) as f: 
                    data = f.read()
                json_data.append([x,json.loads(data)])
    
    captions =[]
    for x in json_data: 
        try:
            for y in x[1][u'figures']:
                nam= x[0].replace(".json","-") + y[u'figType'] + y[u'name']
                captions.append([nam, y[u'caption']])
        except:
            print "not found in " + str(x[0])
#    for x in captions: 
#        print x[0]
#    for y in img_set:
#        print y[0]
    newpath = str("../audios")
    if not os.path.exists(newpath):
        os.makedirs(newpath)
#    for x in captions:
#        synthesize_speech(x)
    
# convert mp3 into wav files
    filenames = [
        filename
        for filename
        in os.listdir(newpath)
        if filename.endswith('.mp3')
        ]
    for f in filenames: 
        name = "\"../audios/" +f[:-4] + ".wav"+ "\""
        j = "\"../audios/" + f + "\""
        comm = "sox " + j + " -b 16 -r 16000 -c 1 " + name
        os.system(comm)
        try: 
            os.remove("../audios/" +f)
            print "deleting " + f + "..."
        except: 
            "Could not delete " + f 
                
    

    #matching each img and its captions to a dictionary
    img_dict ={}
    for x in img_set: 
        for y in captions: 
            reg= re.findall(y[0],x[0])
            if (len(reg) >0): 
                img_dict[y[0]] = [x[1], y[1], []]
                
    for files, roots, directories in os.walk("../audios/"):
        for x in directories:
            if (x.endswith(".wav")):
                file_name = "../audios/" + x
                import soundfile as sf
                try:
                    data, samplerate = sf.read(file_name)
                    img_dict[x[:-4]][2] = [data, samplerate]
                except:
                    pass
    print img_dict
#    cmd = "sbt \"runMain org.allenai.pdffigures2.FigureExtractorBatchCli ../pdfs/ -g ../jsons/ -m ../images\""
#    print cmd
#    os.system(cmd)
#    res = subprocess.check_output(cmd, shell=True)
#    print res
#    images_list= os.listdir(os.getcwd() + "/images")
#    print images_list
#    json_files = os.listdir(os.getcwd() +"/jsons")
#    print json_files
    
    
    
    
if __name__ == '__main__':
    main()