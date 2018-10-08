#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:16:49 2018

@author: elonglouberman
"""
import difflib

a_str = open('NewList.txt', 'r').read()
b_str = open('OldList.txt', 'r').read()
a_list = a_str.split('\n')
b_list = b_str.split('\n')
print len(b_list)
print len(a_list)


html = difflib.HtmlDiff()
x = html.make_file(a_list, b_list, "newfile")
with open("newfile.html", 'w') as f: 
    f.write(x)
s = difflib.SequenceMatcher()
s.set_seqs(a_list,b_list)

oc = s.get_opcodes()

dic = {x: -1 for x in range(1,len(a_list))}

for x in oc: 
    if (x[0] == "equal"): 
        i1 = x[1]
        i2 = x[2]
        j1 = x[3]
        j2 = x[4]
        while (i1 != i2):
            i1 = i1+1
            dic[i1] = j1+1
            j1 =j1 +1


