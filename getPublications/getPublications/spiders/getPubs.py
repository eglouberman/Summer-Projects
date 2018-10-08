#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:08:46 2018

@author: elonglouberman
"""

import scrapy
import sys
import os
reload(sys)
from scrapy.utils.response import open_in_browser
sys.setdefaultencoding('utf-8')

NUMBER_OF_PAGES_TO_PARSE =3
class QuotesSpider(scrapy.Spider):
    name = "scholar"
    count = 10 
    first_name = ""
    surname= ""
    def __init__(self, first=None, last = None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.first_name = first
        self.surname = last
    def start_requests(self):
        login_url ="https://www.google.com/search?ei=KdFiW8fDNYiJ0wK6uZvQBg&q=" + self.first_name+"+"+self.surname+ "+publication+pdf&oq=" + self.first_name+"+"+self.surname+ "+publication+pdf&gs_l=psy-ab.3...9695.10132.0.10253.4.4.0.0.0.0.0.0..0.0....0...1c.1.64.psy-ab..4.0.0....0.K0EmKd_MCm8&hl=en"
        yield scrapy.Request(url=login_url, callback=self.parse_two)
        
    def parse_two(self,response):
        self.log(self.count)
        x = response.css('span.sFZIhb + a::attr(href)').extract()
        for j in x: 
            yield scrapy.Request(j, callback=self.parse_pdf) 
        self.log("going onto the next page!!!!!")
        num = NUMBER_OF_PAGES_TO_PARSE*10
        if (self.count >num):
            raise scrapy.exceptions.CloseSpider("Download complete.")
            self.log(self.sentence_list)
        login_url ="https://www.google.com/search?ei=KdFiW8fDNYiJ0wK6uZvQBg&q=" + self.first_name+"+"+self.surname+ "+publication+pdf&oq=" + self.first_name+"+"+self.surname+ "+publication+pdf&gs_l=psy-ab.3...9695.10132.0.10253.4.4.0.0.0.0.0.0..0.0....0...1c.1.64.psy-ab..4.0.0....0.K0EmKd_MCm8&hl=en"
        next_page = login_url + "&start="+str(self.count)
        self.log("RECEIEVED NEXT PAGE INFO.")
        self.log(next_page)
        self.count+=10
        if next_page is not None:
            next_page = response.urljoin(next_page)
            request = scrapy.Request(next_page, callback=self.parse_two)
            self.log("going to next page!!!!")
            self.log(next_page)
            #open_in_browser(response)
            yield request
        
    def parse_pdf(self, response):       
        newpath = str(os.getcwd()) + '/' + self.first_name+"_"+self.surname
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        page = response.url.split("/")[-1]
        page = newpath+"/" + page
        if (page.endswith("pdf")):
            with open(page, 'wb') as f:
                f.write(response.body)
            self.log("Done with downloading text to PDF!")
        

#        


