# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 19:04
# @Author   :raoyu
import os

# 项目基础路径
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试数据路径
data_path = os.path.join(base_path, 'data')

# 配置文件路径
conf_path = os.path.join(base_path, 'conf')

# 日志路径
log_path = os.path.join(base_path, 'logs')

# 测试报告路径
report_path = os.path.join(base_path, 'reports')

# 测试脚本路径
case_path = os.path.join(base_path, 'testcase')

if __name__ == '__main__':
    print(base_path)
