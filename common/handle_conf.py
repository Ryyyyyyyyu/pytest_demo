# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 19:51
# @Author   :raoyu
import os

from configparser import ConfigParser
from common.handle_path import conf_path


class Handle_conf(ConfigParser):

    def __init__(self, filename):
        super().__init__(self)
        self.read(filename, encoding='utf8')


conf_path = os.path.join(conf_path, 'config.ini')
conf = Handle_conf(conf_path)
