# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json

class WeatherPipeline(object):
    def __init__(self):
        self.file = open('weather.json', 'w', encoding='utf-8')

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.file.close()

    # 将Item实例导出到json文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

class CsvPipeline(object):
    def __init__(self):
        self.colname = ['city','data','weather','tem_higher','tem_lower']
        self.file = open('weather.csv', 'w', encoding='utf-8', newline='')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.colname)
        # 写入字段名称作为首行
        self.writer.writeheader()

    def close_spider(self,spider):
        self.file.close()

    def process_item(self,item,spider):
        self.writer.writerow(item)
        return item

class DatabasePipeline(object):
    """docstring for DatabasePipeline"""
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root',passwd = 'passwd',db = 'weather',charset = 'utf8')
        self.cursor = self.conn.cursor()
        # truncate为数据库删除操作
        self.cursor.execute("truncate table seven")
        print("连接成功")
        self.conn.commit()


    def process_item(self, item, spider):
        sql = 'insert into seven(city,date,weather,tem_higher,tem_lower) values (%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql,(item['city'],item['date'],item['weather'],item['tem_higher'],item['tem_lower']))
            self.conn.commit()
        except pymysql.Error:
            print("error,DatabasePipeline.")
        return item