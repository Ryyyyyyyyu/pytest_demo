# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 21:16
# @Author   :raoyu
import re

from common.handle_conf import conf


class Env:
    """存放测试过程中生成的变量"""
    pass


class Handle_data:
    def replace_data(self, data):
        while True:
            if re.search('#(.*?)#', data) is None:
                return data
            res = re.search('#(.*?)#', data)
            key = res.group()
            item = res.group(1)
            try:
                value = conf.get('test_data', item)
            except:
                value = str(getattr(Env, item))
            data = data.replace(key, value)


if __name__ == '__main__':
    s = Handle_data()
    setattr(Env, 'phone', '18893456789')
    res1 = s.replace_data('{"mobile_phone":"#phone#","pwd":"12345678"}')
    res2 = s.replace_data('{"mobile_phone":"18893456789","pwd":"12345678"}')
    print(res1)
