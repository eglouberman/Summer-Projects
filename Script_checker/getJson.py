#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:42:41 2018

@author: elonglouberman
"""

import json
import urllib
import os
import subprocess
import sys


def main(id, ttle): 
    current_show_code = id # example : '5967a518c2b06f015372f0ac' # Bronx
    api_url = 'http://app.galapro.com/api/subs/' + current_show_code
    
    
    title = ttle
    new_file = title + '_new.json'
    
    def upload_json():
        url = api_url
        print url
        response = urllib.urlopen(url)
        data = json.loads(response.read()) #loads data
        with open(new_file, 'w') as outfile:  #writes data to separate file
            json.dump(data, outfile)
        

        
    upload_json()
    
    
    
    cmd_line = "python Json2Transcription.py " + new_file
    #print (cmd_line)
    os.system(cmd_line) 
    
    cmd_line = "python Change_checker.py " + title + "_new_closedCaption.txt " + title + "_old_closedCaption.txt "
   
    #code that prints console output of whether they are different or not to the python console. 
    try: 
        os.system(cmd_line)
        result = subprocess.check_output(cmd_line, shell=True)
        #print result
    except: 
        print "Old file not found"

  
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'eg. txt files'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
    