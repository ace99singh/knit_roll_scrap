# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


class RollPipeline(object):

	def __init__(self, *args, **kwargs):
	    super(RollPipeline, self).__init__(*args, **kwargs)
	    self.items = []

	def process_item(self, item, spider):
	   	self.items.append((item['name'],item['roll'],item['num']))
	   	return item

	def close_spider(self,spider):
		self.items = sorted(self.items, key = lambda x: x[2], reverse = True)
		for item in self.items:
			print (item)
		pd.DataFrame(self.items).to_excel('output.xls',header = False, index = False)
		pass
	        
