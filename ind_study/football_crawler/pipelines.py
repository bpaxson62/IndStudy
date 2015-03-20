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
    filepath = 'test6.sqlite3'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        if 'SQLPipeline' not in getattr(spider, 'pipelines'):
            return item

        try:
            self.conn.execute('INSERT into Authors VALUES(NULL,?,?,?)', item['user_name'], item['num_posts'],
                              item['geo_location'])
        except:
            print 'Failed to insert' + item['user_name']
        try:
            self.conn.execute('INSERT into Posts VALUES(NULL,?,?,?,?,?,?,?)',
                              (item['author_name'], item['post_title'], item['date'], item['content'],
                               item['team'], item['position'],
                               item['page']))
        except:
            print 'Failed to insert item: ' + item['team']
            return item

    def initialize(self):
        if path.exists(self.filepath):
            self.conn = sqlite3.connect(self.filepath, detect_types=sqlite3.PARSE_DECLTYPES),
        else:
            self.conn = self.create_tables(self.filepath)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_tables(self, filepath):
        conn = sqlite3.connect(filepath, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute(
            "CREATE TABLE Authors( author_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, num_posts INTEGER, "
            "geo_loc TEXT);")
        conn.execute(
            "CREATE TABLE Posts( post_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "post_author TEXT, title TEXT, "
            "date TIMESTAMP, content TEXT, team TEXT,"
            "position INTEGER, page INTEGER,"
            "FOREIGN KEY(post_author) REFERENCES Authors(name));")
        conn.commit()
        return conn