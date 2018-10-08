#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:54:01 2018

@author: elonglouberman
"""
import os
import re
import sys
import subprocess
import signal 

#nltk.download()
from nltk import sent_tokenize

def handler(signum, frame):
    print "Took too much time to download!"
    raise Exception("end of time")

def convertTotxt(full):
    file_list= os.listdir(os.getcwd() + "/" + full) 
    pdf_list =[]
    for x in file_list:
        if (x.endswith(".pdf")): 
            filename = x[:len(x)-3] + "txt"
            if (filename in pdf_list == True): 
                break
            pdf_list.append(x)
     
    
    for x in pdf_list: 
        file_name = x[:len(x)-3] + "txt"
        cmd_line = "pdf2txt.py -o " + full+"/"+file_name + " " + full+"/"+x
        print (cmd_line)
        #setting timeout if file is too big
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(13)
        try: 
            os.system(cmd_line)
        except Exception, exc: 
            print exc
        signal.alarm(0)
#        os.system(cmd_line)
    return len(pdf_list)
        
 


def filter_txts(full_name, full):
    file_list= os.listdir(os.getcwd()+ "/" + full)
    txt_list =[]
    for x in file_list:
        if (x.endswith(".txt") and x[0:3]!= 'new'): 
            txt_list.append(x)
        
    count = 0
    delete_list =[]
    keep_list =[]
    Name = full_name.split(" ")
    try: 
        firstName= Name[0]
        lastName = Name[1]
        name_regex = firstName +'\s?[A-Z]?[\.]?[\s]' +lastName
#        print name_regex
    except: 
        name_regex= full_name
        print name_regex
    
    for y in txt_list: 
        with open(full +"/" + y, "r") as f: 
            reader = f.read()
        print "analyzing " + y
        reader_new = reader[:600]
        result = re.findall(full_name, reader_new.lower())
        if(len(result) !=0):
            result2 = re.findall('abstract|introduction', reader_new.lower())
            if (len(result2) !=0):
                count +=1
                keep_list.append(y)
            else: 
                print "...abstract not found. not a publication. File removed"
                delete_list.append(y)
        else:
            print "...author's name not found in the first 500 chars. File removed. " 
            delete_list.append(y)
    

    for x in delete_list: 
        try: 
            os.remove(full+"/"+x)
            print "...removed " + x
        except: 
            print "...could not remove " + full +"/" +x
        try: 
            file_name = x[:len(x)-3] + "pdf"
            os.remove(full +"/"+file_name)
            print "removed " + full + "/" +file_name
        except: 
            print "could not remove " + file_name
    numPubs =0
    for x in keep_list:
        print "editing..." + x
        if (junkeditor(x, full) == True):
            numPubs +=1
    return numPubs
    
    
def junkeditor(fileN, full):
    isPub = False
    currentScriptFile = fileN
    newScriptFile = 'new_' + currentScriptFile
    

    current = []
    with open(full +"/" +currentScriptFile, 'r') as f: 
        readingFile = f.read()
    
    
    #first, I will delete all the lines that only have one item
    curr = readingFile.split("\n")
#    print len(readingFile)
    curr2 = []
    for x in curr:
        words = x.split(" ")
        if (len(words) ==0):
            continue
        elif (len(words) ==1):
            if (words[0].endswith(".")):
                curr2.append(x)
                continue
            if (len(re.findall("abstract", x,re.IGNORECASE))!=0 or len(re.findall("references", x,re.IGNORECASE))!=0):
                curr2.append(x)
                continue
        else: 
            curr2.append(x)
    current = ("\n").join(curr2)
#    print len(current)
    #delete all before abstract and all after references
    try: 
        abstract_index = current.lower().index('abstract')
        print "found abstract...",
        isPub = True
    except: 
        abstract_index =0
        print "abstract not found in " + currentScriptFile
        return
    #looks at last 3000 chars
    last_many_chars = 3500
    
    try: 
        reference_index = current.lower()[len(current)-last_many_chars:].index('references')
        reference_index = reference_index + len(current) - last_many_chars
        current = current[abstract_index +8:reference_index-1]
        print "found references.. shortened"
    except: 
            try:
                last_many_chars = len(current)/2
                reference_index = current.lower()[len(current)-last_many_chars:].index('references')
                reference_index = reference_index + len(current) - last_many_chars
                current = current[abstract_index +8:reference_index-1]
                print "found references.. shortened"
            except: 
                print "COULD NOT SHORTEN because references not found"
        
        
    current = current.decode("utf8")
    
    cu = re.sub(u'ﬁ', 'fi',current)
    cu = re.sub(u'ﬂ', 'fl',cu)
    cu = re.sub(u'ﬀ', 'ff',cu)
    cu = re.sub(u'ﬃ', 'ffi',cu)
    cu = re.sub(u'\-\n', '',cu)
    #cu2  =re.sub('\d.[?\s?\.]+\d',' ',cu)
    cu3 = re.sub(u'\[.[^a-z]*\]', '', cu)
    current = cu3

    reg3 = u'[^\-^a-z^A-Z^0-9^\s^\'^\.]+'
 
    reg = '\n'

    combined_pat = r'|'.join((reg, reg3))
    
 #   comb = '|'.join((reg3, reg))
#    current2 = []
#  #  current3 =[]
#    
    rep = re.sub(combined_pat, ' ', current)
    
    current = rep
    current = current.decode("utf8")
    tokens = sent_tokenize(current)
    filteredTokens = []
    for x in tokens: 
        if (len(x) <=2):          
            continue
        filterer = re.findall('\s{3}', x)
        if (len(filterer) >=2):
            continue
        filteredTokens.append(x)
    tokens = filteredTokens
    #print tokens

#    for text in current2:
#        rep2 =re.sub(comb, ' ', text)
#        current3.append(rep2)  

        
    with open(full + "/" + newScriptFile, 'w+') as j: 
        for x in tokens: 
            if (len(x) <=2):
                continue
            filterer = re.findall('\s{4}', x)
            if (len(filterer)>=2):
                #print x
                continue
            if (len(re.findall(u'\s', x)) ==0):
                #print x
                continue
            if (len(re.findall(u'[a-zA-Z]', x)) <=3):
                #print x
                continue
            x = re.sub("  "," ",x)
            j.write(x + '\n')
    return isPub
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'eg. old.txt empty_new.txt'
        sys.exit(1)
    first = sys.argv[1].lower()
    last = sys.argv[2].lower()
#    first = "joseph"
#    last ="keshet"
    full_name = first + " " + last
    fullUname= first + "_"+ last
    numPdfs = convertTotxt(fullUname)
    numpubs = filter_txts(full_name, fullUname)
    print "Number of PDF downloads from google: " + str(numPdfs)
    print "Number of publications extracted: " +  str(numpubs)
