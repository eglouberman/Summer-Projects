#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:08:46 2018

@author: elonglouberman
"""

import scrapy
import sys
import re
import os
reload(sys)
from scrapy.utils.response import open_in_browser
sys.setdefaultencoding('utf-8')

NUMBER_OF_PAGES_TO_PARSE =5
class findContext(scrapy.Spider):
    name = "context"
    word = ""
    count = 10
    sentence_list = []

    def __init__(self, word=None, *args, **kwargs):
        super(findContext, self).__init__(*args, **kwargs)
        self.word = word
        with open("../" +self.word+".txt", "w+") as f:
            f.writelines(self.word + ":\n")
    def start_requests(self):
        login_url ="https://www.google.co.il/search?q=" + self.word + "&oq="+ self.word +"&aqs=chrome..69i57j69i60j69i61j0l3.925j0j4&sourceid=chrome&ie=UTF-8&hl=en"
        yield scrapy.Request(url=login_url, callback=self.parse_two)
        
    def parse_two(self,response):
        x = response.css('span.st').extract()
        for j in x: 
            j = re.sub("\<.[^>]*\>","",j)
            j= re.sub("\n", "",j)
            j = re.sub(u'[^\-^a-z^A-Z^0-9^\s^\'^\.]+', '', j)
            j = re.sub("  ", " ",j)
            self.sentence_list.append(j)
            with open("../" +self.word+".txt", 'a+') as f:
                f.writelines(j +"\n")
        self.log(self.sentence_list)           
        self.log("going onto the next page!!!!!")
        num = NUMBER_OF_PAGES_TO_PARSE*10
        self.log(len(self.sentence_list))
        if (self.count >num):
            raise scrapy.exceptions.CloseSpider("Download complete.")
            self.log(self.sentence_list)
        self.count+=10
        next_page = response.urljoin("https://www.google.co.il/search?q=" + str(self.word) + "&oq="+ self.word +"&aqs=chrome..69i57j69i60j69i61j0l3.925j0j4&sourceid=chrome&ie=UTF-8&hl=en&start="+str(self.count))
        request = scrapy.Request(next_page, callback=self.parse_two)
        self.log("YIELDING REQUEST IN FIRST FUNCTION")
        self.log(next_page)
        #open_in_browser(response)
        yield request
        


#        


