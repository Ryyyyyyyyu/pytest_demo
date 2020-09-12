# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 17:44
# @Author   :raoyu
from fake_useragent import UserAgent

headers = {
    'UserAgent': UserAgent().random,
    'Content-Type': 'application/json',
    'X-Lemonban-Media-Type': 'lemonban.v2'
}

if __name__ == '__main__':
    print(headers)
