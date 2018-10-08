#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 13:16:12 2018

@author: elonglouberman
"""

import sys
import os

def main(first, last): 
    cmd_line = "scrapy crawl scholar " + "-a first=" + first + " -a last=" + last
    print (cmd_line) 
    os.system(cmd_line)
    
    cmd_line ="python pdfToTxt.py " + first + " " + last
    print (cmd_line)
    os.system(cmd_line)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'eg. first last'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])