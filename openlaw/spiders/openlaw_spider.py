#coding=utf-8
import scrapy
from scrapy import log
from scrapy.selector import HtmlXPathSelector
import re
import random
import urlparse
import json
import sys
from selenium import webdriver
#from selenium.webdriver.remote.webelement import WebElement
from openlaw.items import JudgementItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor

def isTargetPage(targetpattern, url):
    regex = re.compile(targetpattern, re.IGNORECASE)
    if(regex.match(url)):
        return True
    return False

class OpenlawSpider(scrapy.Spider):
	name = "openlaw"
	allowed_domains = ["openlaw.cn"]
	start_urls = ['http://openlaw.cn/search/judgement/court']
	targetpattern = r'http://openlaw.cn/search/judgement/court\?courtId=\d+'
	#testlink=''
	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		self.driver.get(response.url)
		for court in self.driver.find_elements_by_xpath("/html/body/div/section[3]/div/div/a"):
			#log.msg("Scraping courts...............")

			link = court.get_attribute("href")
			if isTargetPage(self.targetpattern, link):
				yield scrapy.Request(link, callback=self.parse_courturl)
			else:
				#url = response.urljoin(link)
				self.driver.implicitly_wait(5)
				yield scrapy.Request(link, callback=self.parse)
		#self.driver.close()

	def parse_courturl(self, response):
		self.driver.get(response.url)
		court = self.driver.find_element_by_xpath("/html/body/div/div/div/main/div/article[1]/ul/li[2]/a")
		#item = CourtItem()
		#item['name'] = court.text
		#item['link'] = court.get_attribute("href")
		#court_url = item['link']
		#self.testlink = self.testlink + str(item['link'])
		#error: global name textlink is not defined
		#request_with_court_url = scrapy.Request(court_url, callback=self.parse_judgement)
		#yield scrapy.Request(self.testlink,callback=self.parse_judgement)
		#yield request_with_court_url
		#self.driver.close()
		link = court.get_attribute("href")
        #self.testlink = self.testlink + str(link)
        yield scrapy.Request(link,callback=self.parse_judgement)

	def parse_judgement(self, response):
		self.driver.get(response.url)
        base_url = response.url
        totalNum=self.driver.find_element_by_id('totalCount-bar').text
        maxPage=totalNum/20+1
        items = self.driver.find_elements_by_id('ht-kb').find_element_by_tag_name('article')

        for page in range(1,maxPage):
            page_url = base_url + "?page=" + page
            self.driver.get(page_url)
            for index,item in enumerate(items):
                link        = item.find_element_by_xpath('h3/a').get_attribute("href")
                title       = item.find_element_by_xpath('h3/a').text
                date        = item.find_element_by_xpath('ul/li[1]').text
                courtName   = item.find_element_by_xpath('ul/li[2]/a').text
                docType     = item.find_element_by_xpath('ul/li[3]/a').text
                num         = item.find_element_by_xpath('ul/li[4]').text

                self.attributes[link]=[title,date,courtName,docType,num]

                yield Request( url=link, callback=self.parse_details)   
            #end for
            #yield Request(url=+'?page='+page,callback=self.parse_judgement)
        #end for
        #self.driver.close()
    
    def parse_details(self, response):
        accuser[]
        aLaywerN[]
        aLawyerF[]

        defendant[]
        dLaywerN[]
        dLawyerF[]

        judge[]
        officer[]
        clerk[]

        self.driver.get(response.url)
        roles=self.driver.find_elements_by_id('sidebar').find_element_by_xpath('section[2]/ul/li')

        for index,role in enumerate(roles):
            roleName=normalize-space(role.find_element_by_xpath('div[2]').text)
            name=normalize-space(role.text)
            if not name.strip():
                name=normalize-space(role.find_element_by_xpath('a[1]').text)

            if '原告' or '上诉人' or '再审申请人' in roleName:
                accuser.append(name)
            if '被告' or '被上诉人' or '被申请人' in roleName:
                defendant.append(name)

            if '律师' in roleName:
                if '被告' or '被上诉人' or '被申请人' in normalize-space(role.find_element_by_xpath('preceding-sibling::li/div[2]').text):
                    dlawyerN.append(name)
                    dLawyerF.append(role.find_element_by_xpath('div[2]/a').text)
                else:
                    aLawyerN.append(name)
                    aLawyerF.append(role.find_element_by_xpath('div[2]/a').text)

            if '审判长' in roleName:
                judge.append(name)
            if '审判员' in roleName:
                officer.append(name)
            if '书记员' in roleName:
                clerk.append(name)

        pattern = re.compile("http:\/\/openlaw.cn\/judgement\/([a-zA-Z0-9]*)")
        caseId = pattern.search(response.url)

        judgement=JudgementItem()
        judgement['link']       = response.url
        judgement['title']      = self.attributes[response.url][0]
        judgement['date']       = self.attributes[response.url][1]
        judgement['courtName']  = self.attributes[response.url][2] 
        judgement['docType']    = self.attributes[response.url][3]
        judgement['num']        = self.attributes[response.url][4]
        judgement['caseId']     = caseId

        judgement['accuser']    = accuser[]
        judgement['aLawyerN']   = aLawyerN[]
        judgement['aLawyerF']   = aLawyerF[] 

        judgement['defendant']  = defendent[]
        judgement['dLawyerN']   = dLawyerN[]
        judgement['dLawyerF']   = dLawyerF[]

        judgement['judge']      = judge[]
        judgement['officer']    = officer[]
        judgement['clerk']      = clerk[]

        #judgement['description']=
        #judgement['result']=
  
		yield judgement
		self.driver.close()

