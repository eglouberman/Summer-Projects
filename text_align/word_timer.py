#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:31:49 2018

@author: elonglouberman
"""
import json
import re
import sys

def getSlideNums(fave_reader):
    slide_nums =[]
    for x in fave_reader:
        n = ''
        for j in x: 
            num = re.findall('\d',j)
            if (len(num) >0):
                n += str(num[0])
            else:
                break
        if (len(n) >0):
            slide_nums.append(int(n))
    return slide_nums
        


def getSEtimes(fave_reader):
    se_times =[]
    for x in fave_reader: 
        times = re.findall('(\d.[^\s]*\.\d.[^\s]*)', x)
        if (len(times) <0):
            continue
        else: 
            se_times.append(times)   
    return se_times
    
def get_lines(fave_reader):
    script_words =[]
    for x in fave_reader:
        line = re.findall('\d.*\.\d.[^\s]*\t(.+)', x.lower())
        try:
            lst = line[0].split(' ')
            new_list =[]
            for j in lst:
                thing = re.sub('[^\w]','',j)
                if (len(thing)>0):
                    new_list.append(thing)
            script_words.append(new_list)
        except:
            print x
            sys.exit(1)

    #print script_words
    return script_words


#function takes in slide #, word to search for and returns a list of start and end times. If
# it returns an empty list, the word was  not found. Returns a 0 if the slide doesn't have a JSON file
def addToDictionary(num, start, end, word_d):
    current = start
    file_name = "0/slide_" + str(num) + ".json"
    dict_list =[]
    try: 
        with open(file_name, "r") as f: 
            jon = f.read()
    except: 
        print "Cannot find file, or slide number does not have JSON file!" 
        print num
        return 0
    jon = json.loads(jon)
    count =0
    for x in jon[u'words']:
        try:
            if (count ==0): 
                word =  x[u'alignedWord']
                start_time= float(current)
                end_time = float(x[u'end']) + float(current)
                tup = (str(word) , start_time , end_time)
                dict_list.append(tup)
                count+=1
            else: 
                word =  x[u'alignedWord']
                start_time = float(x[u'start']) + float(current)
                end_time = float(x[u'end']) + float(current)
                tup = (str(word) , start_time , end_time)
                dict_list.append(tup)
        except:
            print "error for file with slide " + str(num)
    word_d[num] = dict_list
    

def action(fav):
    with open(fav, "r") as f: 
        fave_reader = f.readlines()
        
   # new_word_list = b_str.split('\n')
    
    # following code gets the slide numbers and inputs them into a list
    slide_nums = getSlideNums(fave_reader)

    #creates a dictionary of each line that we will add tuples of "word, startTime, endTime" to 
    word_dict ={int(x): [] for x in slide_nums}
    
    #gets a list from fave of all the start and end times, so we have easy access to it
    se_times= getSEtimes(fave_reader)

    #gets a list of strings for each line in the script
    word_lines = get_lines(fave_reader)

    #makes sure that the length of the start and end times list is equal to the dictionary size.
    try: 
        assert (len(se_times) == len(word_dict) == len(word_lines))
    except: 
        print "Oops! Length of times list is different than dictionary size"
    
    
    count =0
    for x in slide_nums: 
        start = float(se_times[count][0])
        end = se_times[count][1]
        addToDictionary(x,start, end, word_dict)
        count +=1
    count =0
#    for x in word_dict:
##        if (count ==30):
##            break
#        try: 
#            print str(word_dict[x])
#            print "\n"
#            count +=1
#        except: 
#            pass
    return word_dict
    
    
    
#if __name__ == '__main__':
##    if len(sys.argv) != 3:
##        print 'eg. txt files'
##        sys.exit(1)
#    action(fav)
    #main("Bronx_2017_09_08_fave_fix.txt")
