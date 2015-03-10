# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import sqlite3
from os import path


class SQLPipeline(object):
    filepath = 'test.db'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        if 'SQLPipeline' not in getattr(spider, 'pipelines'):
            return item
        try:
            self.conn.execute('INSERT into Authors VALUES(?,?)',
                              (item['user_name'], item['date'],))
        except:
            print 'Failed to insert item: ' + item['user_name']
            return item

    def initialize(self):
        if path.exists(self.filepath):
            self.conn = sqlite3.connect(self.filepath)
        else:
            self.conn = self.create_table(self.filepath)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_tables(self, filepath):
        conn = sqlite3.connect(filepath)
        conn.execute("CREATE TABLE Authors( author_id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, geo_loc );")
        conn.execute(
            "CREATE TABLE Posts( post_id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, "
            "FOREIGN KEY(author_id) REFERENCES Authors(author_id), Name TEXT, date TIMESTAMP, content TEXT, team TEXT"
            "position INTEGER, page INTEGER);")
        conn.commit()
        return conn