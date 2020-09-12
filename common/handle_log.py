# -*- coding: UTF-8 -*-
# @Time     :2020/9/11 11:45
# @Author   :raoyu
import logging
import os
import time
from common.handle_conf import conf
from common.handle_path import log_path

now = time.strftime('%Y-%m-%d-')
log_file = now + conf.get('logger', 'filename')
log_path = os.path.join(log_path, log_file)


class Handle_logger:

    @staticmethod
    def create_logger():
        # 创建日志收集器
        mylog = logging.getLogger()
        # 设置日志收集器等级
        mylog.setLevel(conf.get('logger', 'Level'))

        # 设置终端输出
        sh = logging.StreamHandler()
        # 设置终端输出等级
        sh.setLevel(conf.get('logger', 'Sh_Level'))

        # 设置文件输出
        fh = logging.FileHandler(filename=log_path, encoding='utf-8')
        # 设置文件输出等级
        fh.setLevel(conf.get('logger', 'Fh_Level'))

        mylog.addHandler(sh)
        mylog.addHandler(fh)

        # 创建一个输出格式对象
        formats = '%(asctime)s -- [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        form = logging.Formatter(formats)
        sh.setFormatter(form)
        fh.setFormatter(form)

        return mylog


log = Handle_logger.create_logger()
