# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#class CourtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #name = scrapy.Field()
    #link = scrapy.Field()

class JudgementItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    link         = scrapy.Field();
    title        = scrapy.Field();
    date         = scrapy.Field();    
    courtName    = scrapy.Field();
    docType      = scrapy.Field();
    num          = scrapy.Field();
    caseId       = scrapy.Field();
    
    accuser      = scrapy.Field()
    aLawyerN     = scrapy.Field()
    aLawyerF     = scrapy.Field()
    
    defendant    = scrapy.Field()
    dLawyerN     = scrapy.Field()    
    dLawyerF     = scrapy.Field()

    description  = scrapy.Field()#???????????????????????????
    result       = scrapy.Field()#?????????????????????????
    
    judge        = scrapy.Field()#审判长
    officer      = scrapy.Field()#审判员
    clerk        = scrapy.Field()#书记员