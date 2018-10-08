#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:51:23 2018

@author: elonglouberman
"""
import os
from datetime import timedelta, datetime
import re
import sys

def main(dayz): 
    days_to_subtract = dayz
    
    
    def getTimeToDel(days_to_s):
        d = datetime.today() - timedelta(int(days_to_s))
        del_year= str(d)[0:4]
        del_month = str(d)[5:7]
        del_day = str(d)[8:10]
        time_until_delete = [int(del_year), int(del_month), int(del_day)]
        return time_until_delete
    
    def convertToList(d):
        if (str(d)[2] == '-'):
            year= str(d)[6:10]
            month = str(d)[0:2]
            day = str(d)[3:5]
        else:
            year= str(d)[0:4]
            month = str(d)[5:7]
            day = str(d)[8:10]
        time_list= [int(year), int(month), int(day)]
        return time_list


    def delete(time):
        count = 0
        lst = os.listdir(os.getcwd())
        reg = '\d{4}-\d{2}-\d{2}'
        reg2 = '\d{2}-\d{2}-\d{4}'
        combined_pat= r'|'.join((reg, reg2))
        for i in lst: 
            check = re.findall('logs', i.lower())
            if (len(check) != 1):
                continue
            for root, dirs, files in os.walk(i):
                for x in files: 
                    date = re.findall(combined_pat,x)
                    #print date
                    if (len(date)!=1):
                        continue
                    time_list = convertToList(date[0])
                    if (time_list[0] < time[0]): 
    #                    delete the file
                        try: 
                            os.remove(root + "/" + x)
                            print str(x) +  " removed!"
                            count +=1
                        except: 
                            print "could not remove " + str(x)
                    elif (time_list[0] > time[0]):
                        continue
                    elif (time_list[0] == time[0]): 
                        if (time_list[1] > time[1]): 
                            continue
                        elif (time_list[1] < time[1]):
    #                        delete the file
                            try: 
                                os.remove(root + "/" + x)
                                print str(x) +  " removed!"
                                count +=1 
                            except: 
                                print "could not remove " + str(x)
                        elif (time_list[1]==time[1]):
                            if (time_list[2] <= time[2]): 
    #                            delete the file
                                try: 
                                    os.remove(root + "/" + x)
                                    print str(x) +  " removed!"
                                    count +=1
                                except: 
                                    print "could not remove " + str(x)
                            else:
                                continue
                        
        print "Number of files deleted: " + str(count)
                
            
    timeToDelete = getTimeToDel(days_to_subtract)
    print timeToDelete
    delete(timeToDelete)
        


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'input number of days from which you want everything deleted'
        sys.exit(1)
    main(sys.argv[1])

