# -*- coding:utf-8 -*-

import os
import pymysql

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class Dba(object):

    def __init__(self):
        pass

    def connect(self):
        # 创建数据库连接,格式为utf8
        db = pymysql.connect(
            # host='localhost',
            host='10.4.255.129',
            user="root",
            # passwd="ideal123",
            passwd="Ideal@123",
            db='douban',
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return db

    def cursor(self):
        consor = self.connect().cursor()
        return consor

    def cux_sql_base(self, db, sql):
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.close()
        db.commit()

    def close(self):
        self.cursor().connection.commit()
        self.cursor().close()
        self.connect().close()
