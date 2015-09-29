# -*- coding: utf-8 -*-
#!/usr/bin/env python
import scrapy
import MySQLdb
import urllib
import logging
import time
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

class CategorySpider(scrapy.Spider):
  name = "category_spider"
  def __init__(self):
    super(CategorySpider, self).__init__()
    self.allowed_domains = ["i.meituan.com"]
    url_list = []
    # 所有城市的拼音从A-Z
    for i in xrange(26):
      url_list.append("http://i.meituan.com/index/changecity/more/" + chr(i + ord('A')) + "?cevent=imt%2FselectCity%2Fmore")
    self.start_urls = tuple(url_list)

  def parse(self, response):
    city_list = response.selector.xpath('//ul[@class="table box nopadding"]/li/a/@data-citypinyin').extract()
    for city in city_list:
      # 每个城市的美食url，抓取1000页
      url = "http://i.meituan.com/" + city + "?cid=1&stid=_b1&cateType=poi&p="
      for i in range(1, 1000):
        yield scrapy.http.Request(url=url + str(i), callback=self.ParseItemList)

  def ParseItemList(self, response):
    main_list = response.selector.xpath('//div[@class="deal-container"]/div[@id="deals"]/dl[@class="list"]')
    for item in main_list:
      title = item.xpath('dd[@class="poi-list-item"]/a/span[@class="poiname"]/text()').extract()
      title = ''.join(title)
      sub_item_list = item.xpath('dd/dl[@class="list"]/dd/a/div[@class="dealcard dealcard-poi"]/div[@class="dealcard-block-right"]/div[@class="title text-block"]/text()').extract()
      for sub_item in sub_item_list:
        print title + " " + sub_item
  def write2DB(self, sub_item)
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
        cur=conn.cursor()
        #cur.execute('select * from user')
        value = [1, 'hello world!']
        cur.execute('insert into test values(%s,%s)',value)
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
