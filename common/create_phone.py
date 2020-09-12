# -*- coding: UTF-8 -*-
# @Time     :2020/9/5 18:30
# @Author   :raoyu
# @Email    :2458757210@qq.com
# @Phone    :18893703014
import random

from common.handle_db import db


class Create_Phone(object):

    def create_phone(self):
        while True:
            # 生成第二位数字
            second = [3, 4, 5, 7, 8][random.randint(0, 4)]
            # 生成第三位数字
            third = {
                3: random.randint(0, 9),
                4: [5, 7, 9][random.randint(0, 2)],
                5: [i for i in range(0, 10) if i != 4][random.randint(0, 8)],
                7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
                8: random.randint(0, 9)
            }[second]
            last_num = random.randint(10000000, 99999999)
            # phone = '1{}{}{}'.format(second, third, last_num)
            phone = '134{}'.format(last_num)
            sql = "select * from futureloan.member where mobile_phone = '{}';".format(phone)
            result = db.find_one(sql=sql)
            # 返回None则生成手机号数据库不存在，可以注册
            if result is None:
                return phone


if __name__ == '__main__':
    num = Create_Phone()
    a = num.create_phone()
    print(a)
