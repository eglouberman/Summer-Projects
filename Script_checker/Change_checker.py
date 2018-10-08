#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:35:43 2018

@author: elonglouberman
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#parses through each line and finds the string that starts each line
def findQuote(x):
    count = 0
    word = ""
    for j in x: 
        if count == 4:
            word += j
        if (j == "\t"):
            count+=1
            
    return word


#print len(new), len(current)

def main(curr, ol): 
    currentScriptFile = curr
    oldScriptFile = ol


    with open(currentScriptFile, 'r') as f: 
        current = f.readlines()

    with open(oldScriptFile, 'r') as k: 
        new = k.readlines()

    quotes_current =[]
    quotes_new = []
    
    for x in current:
        quotes_current.append(findQuote(x))
        
    for y in new: 
        quotes_new.append(findQuote(y))
    
    
    ind = max(len(new), len(current))
    
    diff = False
    for x in range(0,ind): 
        try: 
            if quotes_current[x] != quotes_new[x]:
                print "SCRIPTS ARE DIFFERENT STARTING AT LINE " + str(x)
                diff = True
                break
        except: #if there is an index error, we know that one is longer than the other
            print "Scripts are different starting at line " + str(x)
        
    if (diff == False):
        print "Both scripts appear to be the same!"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'eg. txt files'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
    

    

    



        




