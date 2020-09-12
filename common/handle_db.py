# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 20:07
# @Author   :raoyu
import pymysql

from common.handle_conf import conf


class Handle_db:
    def __init__(self):
        self.con = pymysql.connect(host=conf.get('mysql', 'host'),
                                   port=conf.getint('mysql', 'port'),
                                   user=conf.get('mysql', 'user'),
                                   password=conf.get('mysql', 'password'),
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        # 创建游标对象
        self.cursor = self.con.cursor()

    def find_one(self, sql):
        self.con.commit()
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    def find_all(self, sql):
        self.con.commit()
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def update_data(self, sql):
        self.cursor.execute(sql)
        self.con.commit()


db = Handle_db()
if __name__ == '__main__':
    db = Handle_db()
    sql = "select * from futureloan.member LIMIT 10"
    res = db.find_all(sql)
    res1 = db.find_one(sql)
    print(res, res1)
