# -*- coding: utf-8 -*-
import scrapy
import re
# id for roll no: txtrollno
# id for sem selector: ddlResult

class InfilSpider(scrapy.Spider):
    name = 'infil'
    count = 0
    allowed_domains = ['govexams.com']
    start_urls = ['https://govexams.com/knit/searchResult.aspx/']
    records = []

    def parse(self, response):
    	roll_input = response.css('input#txtrollno').extract()
    	print (roll_input)
    	for roll_num in range(16201,16261):
    		try:
    			yield scrapy.FormRequest.from_response(response,
    		formdata={"txtrollno":str(roll_num)},
    		callback = self.submited)
    		except Exception as e:
    			pass

    def submited(self, response):
    	roll_input = response.css('input#txtrollno').extract()
    	selector = response.css('select#ddlResult>option').extract()
    	selected_option = re.search('value="(.*)"',selector[1]).group(1)
    	selected_option = str(selected_option)
    	yield scrapy.Request(url='https://govexams.com/knit/displayResultsEvenN.aspx?key='+selected_option,callback=self.result)

    def result(self,response):
    	num = re.search('>(.*) \/',response.css('span#lbltotlmarksDisp').extract()[0]).group(1)
    	name = re.search('>(.*)<',response.css('span#lblname').extract()[0]).group(1)
    	roll = int(re.search('>(.*)<',response.css('span#lblrno').extract()[0]).group(1))
    	
    	yield {
    		'name' : name,
    		'roll' : roll,
    		'num'  : num,
    	}

