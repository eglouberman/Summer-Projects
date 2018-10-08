#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:20:33 2018

@author: elonglouberman
"""
import difflib
import json
import re
import os
import sys
from word_timer import action

def text_align(old_str, new_str):
    
    s = difflib.SequenceMatcher()
    s.set_seqs(new_str,old_str)
    oc = s.get_opcodes()
    
    dic = {x: -1 for x in range(1,len(new_str))}
    
    for x in oc: 
        if (x[0] == "equal"): 
            i1 = x[1]
            i2 = x[2]
            j1 = x[3]
            while (i1 != i2):
                i1 = i1+1
                dic[i1] = j1+1
                j1 =j1 +1
#    html = difflib.HtmlDiff()
#    with open ("compare.html", "w") as f: 
#        x= html.make_file(old_str,new_str)
#        f.write(x)
    return dic

def get_old_words(fave_reader):
    script_words =[]
    for x in fave_reader: 
        line = re.findall('\d.*\.\d.[^\s]*\t(.+)', x.lower())
        if (len(line)>0):
            lst = line[0].split(' ')
            for j in lst: 
                thing = re.sub('[^\w]','',j)
                if (len(thing)>0):
                    script_words.append(thing)
    #print script_words
    return script_words

def get_new_words(fave_reader):
    script_words =[]
    for x in fave_reader: 
        line = re.findall('end_time\s(.+)\n', x.lower())
        if (len(line)>0):
            lst = line[0].split(' ')
            for j in lst: 
                thing = re.sub('[^\w]','',j)
                if (len(thing)>0):
                    script_words.append(thing)
    #print script_words
    return script_words

def replace_times(fave_reader, time_list_new, newfav):
    count =0
    index = 0
    super_count =0
    with open(newfav.replace('.txt', '2.txt'), "w") as f: 
        while (super_count < len(time_list_new)):
            line = re.findall('end_time\s(.+)\n', fave_reader[count].lower())
            if (len(line)>0):
                lst2 = line[0].split(' ')
                lst =[]
                for j in lst2: 
                    thing = re.sub('[^\w]','',j)
                    if (len(thing)>0):
                        lst.append(thing)
            super_count += len(lst)
            #index-1 is the last time we need to log
            delta = index+ len(lst)-1
            begin = time_list_new[index][1]
            try: 
                end = time_list_new[delta][2]
            except: 
                end = time_list_new[len(time_list_new)-1][2]
            index = index + len(lst)
            #replace the begin time and end time in the line
            be = str(begin) + "\t" + str(end)
            real_line = re.sub('begin_time\tend_time',be,fave_reader[count])
            f.write(real_line)
            count +=1


        
## function finds all the values that have (0.0,0.0) and replaces it with values of the ones before and after
## meanwhile, it adjusts all the values according to what times were added! 
def average_values (word_list):
    count  =0
    current =word_list[0][1]
    for x in word_list: 
        first_time = float(x[1])
        second_time = float(x[2])
        delta = abs(float(second_time) - float(first_time))
        if (first_time == 0.0 and second_time == 0.0):
            try: 
                prev_start_time = float(word_list[count-1][1])
#                prev_delta = abs(float(word_list[count-1][2]) - float(word_list[count-1][1]))
                next_start_time = 0.0
                counter = 0
                while (next_start_time == 0.0):
                    #check if we're at the end of the script. problematic if we are!
                    if ((count+counter) == len(word_list)):
                        print "start" + str((word_list[count-1][2]))
                        next_start_time = float(word_list[count-1][2])
                        print "hereerereer" + str(next_start_time)
                        counter+=1
                        break
                    next_start_time = float(word_list[count+counter][1])
                    counter += 1
                print "Counter: " + str(counter)
                calc_diff = abs(float(next_start_time) - float(prev_start_time))
                print "DIFF: " + str(calc_diff)
                divider = float(counter)
                average = float((calc_diff)/divider)
                print "Dividing by... " + str(divider) + " to get " + str(average)
                current = prev_start_time + average 
                word_list[count-1][2] = current
                j =0
                while (j < counter - 1):
                    word_list[count +j][1] = current
                    word_list[count +j][2] = current +average
                    current = current + average
                    print "averaging... " + word_list[count +j][0] + "  on line " + str(count + j + 1)
                    j+=1
            except IndexError: 
                print "index error. Please check if corresponding json files exist"
                return
                sys.exit(1)
        else: 
            pass
        count +=1

def main(oldfav, newfav):
    
#    newText = 'NewText.txt'
#    oldText = 'FaveTextMaria.txt'
    with open(oldfav, "r") as f: 
        oldWords = f.readlines()
    with open(newfav, "r") as f: 
        newWords = f.readlines()

    oldListofWords = get_old_words(oldWords)
    newListofWords = get_new_words(newWords)
    
#ONLY FOR VISUAL REPRESENTATION
    with open('newList.txt', 'w') as f: 
        for x in newListofWords:
            f.write(x)
            f.write("\n")
    with open('oldList.txt', 'w') as f: 
        for x in oldListofWords:
            f.write(x)
            f.write("\n")   
#################################
    dic_align=  text_align(oldListofWords, newListofWords)
    
    time_dic = action(oldfav)
    time_list = []
    for x in time_dic:
        for y in time_dic[x]:
            time_list.append(y)
    print time_dic
    #time_list is a list of all the words including the start time and end times
    count =0
    time_list_two =[]
    for x in oldListofWords:
        try: 
            master =re.findall(time_list[count][0], x)
            if (len(master)>0):
                tup= [time_list[count][0], time_list[count][1], time_list[count][2]]
                time_list_two.append(tup)
                count +=1
            elif (time_list[count][0] == '<unk>'):
                print "adding... " + str(x)
                tup= [str(x), time_list[count][1], time_list[count][2]]
                time_list_two.append(tup)
                count +=1
            else:
                print "does not match " + str(time_list[count][0]) + " added " + str(x) +" on line " + str(count) 
                tup= [str(x), 0.0, 0.0]
                time_list_two.append(tup)
            
        except: 
            print "probably an index error, or at the end."
            if (len(time_list) == count):
                print "does not match. adding " +  str(x)
                tup= [str(x), 0.0, 0.0]
                time_list_two.append(tup)
            

            
    print len(time_list_two)
    print len(oldListofWords)
    count =0
    with open("compare.txt","w") as f: 
        for x in oldListofWords: 
            try:
                f.write(x + " : " + time_list_two[count][0])
            except: 
                f.write(x + " : ")
            f.write("\n")
            count +=1
    ##Now, we will map the new words to the list of old words. 
    ##
    time_list_new =[]
    for x in dic_align: 
        if (dic_align[x] == -1):
            tup = [str(newListofWords[x-1]), 0.0, 0.0]
            time_list_new.append(tup)
        else: 
            #print "matching.. " + str(x-1) +" with " + str(dic_align[x]-1)
            try:
                tup = time_list_two[int(dic_align[x])-1]
                time_list_new.append(tup)
            except: 
                print "index error. could not align " + str(x-1) +" with " + str(dic_align[x]-1)
            
    ## time_list_new is the real list we are interested in! 
    
    newListofW =[]
    for x in time_list_new:
        newListofW.append(x[0])
    
    assert(len(newListofW) == len(newListofWords))
    count =0
    with open("compare.txt","w+") as f: 
        for x in time_list_new:  
            f.write(x[0] + "\t\t" + str(x[1]) +  "\t" + str(x[2]))
            f.write("\n")
            count +=1
#            
    average_values(time_list_new)
    
    count =0
    with open("compare2.txt","w+") as f: 
        for x in time_list_new:  
            f.write(x[0] + "\t\t" + str(x[1]) +  "\t" + str(x[2]))
            f.write("\n")
            count +=1    
#   
    print len(time_list_new)
    replace_times(newWords, time_list_new, newfav)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'eg. old.txt empty_new.txt'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
