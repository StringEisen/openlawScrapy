# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json

class DuplicatesPipeline(object):
	
	def __init__(self):
		self.ids_seen = set()
		json_file = file("judgement.json")
		data = json.load(json_file)
		self.ids_seen = set(data['caseId'])


	def process_item(self, item, spider):
		if item['caseId'] in self.ids_seen:
			raise DropItem("Contains caseId: %s" % item)
		else:
			self.ids_seen.add(item['caseId'])
		return item