#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:11:17 2018

@author: elonglouberman
"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
import re
from sets import Set
import gender_guesser.detector as gender



# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).

session = Session(profile_name="default")
polly = session.client("polly")

voice1 = "<speak> <amazon:effect vocal-tract-length=\"+0%\"> <prosody pitch=\"-0%\"> "
voice2 = "<speak> <amazon:effect vocal-tract-length=\"-8%\"> <prosody pitch=\"+10%\"> "
voice3 = "<speak> <amazon:effect vocal-tract-length=\"+8%\"> <prosody pitch=\"-10%\"> "
voice4 = "<speak> <amazon:effect vocal-tract-length=\"+12%\"> <prosody pitch=\"+0%\"> "
voice5 = "<speak> <amazon:effect vocal-tract-length=\"+0%\"> <prosody pitch=\"+20%\"> " 
voice6 = "<speak> <amazon:effect vocal-tract-length=\"-20%\"> <prosody pitch=\"-0%\"> "
voice7 = "<speak> <amazon:effect vocal-tract-length=\"+12%\"> <prosody pitch=\"-10%\"> "
voices_male = [voice1,voice2,voice5,voice6,voice7]
voices_female = [voice1,voice2,voice3,voice4,voice5]


def find_cast(fave_reader,male_v, female_v): 
    cast =Set([])
    for x in fave_reader: 
        ## finds the cast members and puts them into a set
        cast_member = re.findall('\d\s(\w.[^\d]+)\s\d', x)
        try:
            cast_mem = re.findall('[^\_\&]\w[A-Z][^\_\&\s]*', cast_member[0])
            for j in cast_mem:
                cast.add(j)
        except: 
            pass

#goes through cast and determines sex
    master_dict = {}
    d= gender.Detector(case_sensitive=False)
    count_male =0
    count_female =0

    for x in cast: 
        if (d.get_gender(x) == "male"):
            master_dict[x] = [male_v[0],voices_male[count_male]]
            if (count_male == len(voices_male)-1):
                count_male =0
            else: 
                count_male +=1
        elif (d.get_gender(x) == "female"): 
            master_dict[x] = [female_v[0],voices_female[count_female]]
            if (count_female == len(voices_female)-1):
                count_female =0
            else: 
                count_female +=1           
        else:
            master_dict[x] = [male_v[0],voices_male[count_male]]
            if (count_male == len(voices_male) -1):
                count_male =0
            else: 
                count_male +=1
    return master_dict
        


def get_male_female_voiceID(polly):
    #[en-US, en-IN, tr-TR, ru-RU, ro-RO, pt-PT, pl-PL, nl-NL, 
    #it-IT, is-IS, fr-FR, es-ES, de-DE, ko-KR, en-GB-WLS, hi-IN, cy-GB, 
    #da-DK, en-AU, pt-BR, nb-NO, sv-SE, ja-JP, es-US, fr-CA, en-GB]
    response = polly.describe_voices(LanguageCode= 'es-ES')

    voices =  response['Voices']
    print voices

    man_voice = []
    woman_voice =[]
    for x in voices: 
        if (x['Gender'] == 'Male'):
            man_voice.append(x['Id'])
        if (x['Gender'] == 'Female'):
            woman_voice.append(x['Id'])
    
    print woman_voice
    print man_voice
#    for x in voices2: 
#        if (x['Gender'] == 'Male'):
#            man_voices.append(x['Name'])
#        if (x['Gender'] == 'Female'):
#            woman_voices.append(x['Name'])
    
    #man_voice is a string of all the male voices
    return find_cast(fave_reader, man_voice, woman_voice)
    



def synthesize_speech(fav_reader,foreign_lang, master_dict):
    index = 550
    count =1
    assert (len(fav_reader) == len(foreign_lang))
    print len(fav_reader)
    for x in fav_reader: 
        print x
        ##finds the line from each slide
        line = re.findall('end_time\s(\D.+)\n', foreign_lang[index].lower())
        #line = re.findall('end_time\s(\D.+)\n', x.lower())
        index +=1
        ##finds the line number to name the mp3 file! 
        n = ''
        for j in x: 
            num = re.findall('\d',j)
            if (len(num) >0):
                n += str(num[0])
            else:
                break
        if (len(n) >0):
                count = int(n)
        else: 
            count +=1
        
        ##identifies the cast member to get the selected voice (Male or female)
        cast_member = re.findall('\d\s(\w.[^\d]+)\s\d', x)
        try:
            cast_mems = re.findall('[^\_\&]\w[A-Z][^\_\&\s]*', cast_member[0])
        except: 
            cast_mems = ["none"]
        
        try: 
            voice_id = master_dict[cast_mems[0]][0]
#            print voice_id
#            print cast_mems[0] +  " : " + voice_id + " on line " + str(count),
        except: 
            print master_dict[cast_mems[0]][0]
            voice_id = master_dict[0]
            #print cast_mems[0] +  " : DEFAULT on line " + str(count),
            
        #HERE, we will designate a certain amount of seconds per speech
        times = re.findall('(\d.[^\s]*\.\d.[^\s]*)', x)
        
        assert(len(times) ==2) 
        msecs = float((float(times[1]) - float(times[0])))*1000
        #print " with "+ str(msecs) +"ms"
        print line
        ssml = master_dict[cast_mems[0]][1] + "<prosody amazon:max-duration=\""+ str(msecs) +"s\">" + line[0] + "</prosody></prosody></amazon:effect></speak>"

        ###actual synthesis of speech!
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(TextType = "ssml",Text=ssml, OutputFormat="mp3",
                                                VoiceId= voice_id)
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
            slide= "slide_" + str(count) + ".mp3"
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
            
with open("bronx_new_transcription2.txt", "r") as f: 
    fave_reader = f.readlines()


with open("Bronx_new_transcription.txt","r") as f: 
    lang_diff = f.readlines()

master_dict = get_male_female_voiceID(polly)
print master_dict
synthesize_speech(fave_reader,lang_diff,master_dict)

