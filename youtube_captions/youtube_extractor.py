#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 15:09:00 2018

@author: elonglouberman
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:42:41 2018

@author: elonglouberman
"""

import json
import re
import os
import subprocess
import sys


def main(url_f): 
    url_file= url_f

    with open(url_file, 'r') as outfile:  #reads url file
        out = outfile.readlines()
    audios =[]
    for y in out: 
        os.path.dirname(os.path.abspath(__file__))
        cmd_line = "youtube-dl --list-subs " + y
        #print cmd_line
        os.system(cmd_line)
        result = subprocess.check_output(cmd_line, shell=True)
        
        x = re.findall("has no subtitles", result)
        if (len(x) == 0):
            print "Has manual subtitles." 
            cmd_views = "youtube-dl --get-filename -o \"%(view_count)s\" " + y
            os.system(cmd_views)
            num_views= subprocess.check_output(cmd_views, shell=True)
            if (int(num_views) <100000):
                print "Skipping because it has not reached minimum view count"
                continue
            cmd_likes= "youtube-dl --get-filename -o \"%(like_count)s\" " + y
            os.system(cmd_likes)
            num_likes = subprocess.check_output(cmd_likes, shell=True)
            cmd_dis ="youtube-dl --get-filename -o \"%(dislike_count)s\" " + y
            os.system(cmd_dis)
            num_dislikes = subprocess.check_output(cmd_dis, shell=True)
            if (float(num_likes)/float(num_dislikes) <2.0):
                print "ratio of likes to dislikes is less than 2:1. Therefore, video will not be downloaded."
                continue
            cmd = "youtube-dl -x --write-srt --sub-lang en --min-views 100000 " + y
            os.system(cmd)
            blah = "youtube-dl -x --audio-format mp3 " + y
            os.system(blah)
            get_t = "youtube-dl --get-filename " + y
            os.system(get_t)
            res = subprocess.check_output(get_t, shell=True)
            title = re.findall('(\w.*)\.',res)
            audios.append(title)
            directories= os.listdir(os.getcwd())
            fileName =[]
            st = '(' + title[0] +'.*.vtt)'
            for j in directories:
                fileName = re.findall(st, j)
                if (len(fileName)>0):
                    break
            g = "python vtt2Transcription.py \"" + fileName[0] + "\""
            try: 
                os.system(g)
                #os.remove(fileName[0])
            except: 
                "There was an error transcribing."
        else: 
            print "Has no subtitles."
            continue
    
    #convert the mkv files to wav files!
    path = os.getcwd()
    filenames = [
        filename
        for filename
        in os.listdir(path)
        if filename.endswith('.mp3')
        ]
    for f in filenames: 
        name = "\"" +f[:-4] + ".wav"+ "\""
        opus = f[:-4] + ".opus"
        j = "\"" + f + "\""
        comm = "sox " + j + " -b 16 -r 16000 -c 1 " + name
        subprocess.call(comm, shell= True)
        try: 
            os.remove(f)
            os.remove(opus)
            print "deleting " + f + "..."
        except: 
            "Could not delete " + f 
       
        
    
    
    #os.system(cmd_line)
#    cmd_line = "python Json2Transcription.py " + new_file
#    #print (cmd_line)
#    os.system(cmd_line) 
#    
#    cmd_line = "python Change_checker.py " + title + "_new_closedCaption.txt " + title + "_old_closedCaption.txt "
#   
#    #code that prints console output of whether they are different or not to the python console. 
#    try: 
#        os.system(cmd_line)
#        result = subprocess.check_output(cmd_line, shell=True)
#        #print result
#    except: 
#        print "Old file not found"

  
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'input url file name as parameter'
        sys.exit(1)
    main(sys.argv[1])


