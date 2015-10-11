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
  #名称
  name = "category_spider"
  def __init__(self):
    super(CategorySpider, self).__init__()
    self.allowed_domains = ["i.meituan.com"]
    url_list = []
    for i in xrange(26):
      url_list.append("http://i.meituan.com/index/changecity/more/" + chr(i + ord('A')) + "?cevent=imt%2FselectCity%2Fmore")
    self.start_urls = tuple(url_list)
  #解析
  def parse(self, response):
    city_list = response.selector.xpath('//ul[@class="table box nopadding"]/li/a/@data-citypinyin').extract()
    for city in city_list:
      url = "http://i.meituan.com/" + city + "?cid=1&stid=_b1&cateType=poi&p="
      for i in range(1, 1000):
        yield scrapy.http.Request(url=url + str(i), callback=self.ParseItemList)

  #分析每一个item
  def ParseItemList(self, response):
    main_list = response.selector.xpath('//div[@class="deal-container"]/div[@id="deals"]/dl[@class="list"]')
    conn=MySQLdb.connect('localhost','root','root','mysql',3306)
    conn.set_character_set('utf8')
    for item in main_list:
      title = item.xpath('dd[@class="poi-list-item"]/a/span[@class="poiname"]/text()').extract()
      title = ''.join(title)
      sub_item_list = item.xpath('dd/dl[@class="list"]/dd/a/div[@class="dealcard dealcard-poi"]/div[@class="dealcard-block-right"]/div[@class="title text-block"]/text()').extract()
      for sub_item in sub_item_list:
        self.write2DB(conn,sub_item)
        print title + " " + sub_item
    conn.close()
  #写数据库
  def write2DB(self,conn, sub_item):
    try:
        cur=conn.cursor()
        value = [sub_item]
        conn.set_character_set('utf8')
        cur.execute('SET NAMES utf8;') 
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        cur.execute('insert into test(foodname) values(%s)',value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
