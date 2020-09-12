# -*- coding: UTF-8 -*-
# @Time     :2020/9/9 17:25
# @Author   :raoyu
import decimal
import os
import jsonpath
import pytest
import requests
from common.handle_excel import Handle_Excel
from common.handle_path import data_path
from conf.config import headers
from common.handle_conf import conf
from common.create_phone import Create_Phone
from common.handle_data import Env, Handle_data
from common.handle_log import log
from common.handle_db import db


@pytest.fixture(scope='class')
def register_fixture():
    # 注册用户
    phone = Create_Phone().create_phone()
    url = conf.get('evn', 'url') + '/member/register'
    register_date = {"mobile_phone": phone, "pwd": "12345678", "type": 1}
    expected = {'code': 0, 'msg': 'OK'}
    log.debug('----------开始执行前置处理:注册请求发送，请求入参{}'.format(register_date))
    register = requests.request(method='post', url=url, json=register_date, headers=headers)
    reg_res = register.json()
    print('前置处理中注册接口入参:', register_date)
    print('前置处理中注册接口出参:', reg_res)
    log.debug('----------前置处理:注册请求发送成功，请求出参{}'.format(reg_res))
    try:
        assert reg_res['code'] == expected['code']
        assert reg_res['msg'] == expected['msg']
        sql = "select * from futureloan.member where mobile_phone = '{}';".format(phone)
        sql_result = db.find_one(sql)
        log.debug('----------查询数据库SQL语句为:{},返回结果{}'.format(sql, sql_result))
        assert sql_result is not None
    except AssertionError as e:
        print('前置处理中注册出参不符合要求！！！', e)
        log.exception('前置处理中注册出参不符合要求！！！{}'.format(e))
    setattr(Env, 'phone', phone)
    yield phone
    pass


@pytest.fixture(scope='class')
def login_fixture(register_fixture):
    # 用户登录
    phone = register_fixture
    url = conf.get('evn', 'url') + '/member/login'
    login_date = {"mobile_phone": phone, "pwd": "12345678"}
    expected = {'code': 0, 'msg': 'OK'}
    log.debug('----------开始执行前置处理:登录请求发送，请求入参{}'.format(login_date))
    login = requests.request(method='post', url=url, json=login_date, headers=headers)
    login_res = login.json()
    print('前置处理中登录接口入参:', login_date)
    print('前置处理中登录接口出参:', login_res)
    log.debug('----------前置处理:登录请求发送成功，请求出参{}'.format(login_res))
    try:
        assert login_res['code'] == expected['code']
        assert login_res['msg'] == expected['msg']
    except AssertionError as e:
        print('前置处理中登录出参不符合要求！！！', e)
        log.exception('前置登录中注册出参不符合要求！！！{}'.format(e))
    setattr(Env, 'phone', phone)
    member_id = jsonpath.jsonpath(login_res, '$..id')[0]
    token = "Bearer" + " " + jsonpath.jsonpath(login_res, '$..token')[0]
    setattr(Env, 'member_id', member_id)
    setattr(Env, 'token', token)
    yield member_id, token
    pass


class TestRegisterCase:
    filename = os.path.join(data_path, 'apicases.xlsx')
    excel = Handle_Excel(filename, 'register')
    datas = excel.read_data()

    @pytest.mark.parametrize('case', datas)
    def test_register(self, case):
        print(case)
        # 准备测试数据
        method = case['method']
        url = case['url']
        row = case['case_id'] + 1
        title = case['title']
        if '#phone#' in case['data']:
            phone = Create_Phone().create_phone()
            setattr(Env, 'phone', phone)
        data = eval(Handle_data().replace_data(case['data']))
        expected = eval(case['expected'])
        log.debug('----------开始执行{}用例的注册请求发送，请求入参{}'.format(title, data))
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        print('注册接口中{}用例入参:'.format(title), data)
        print('注册接口中{}用例出参:'.format(title), res)
        log.debug('----------{}用例的注册请求出参{}'.format(title, res))
        try:
            assert res['code'] == expected['code']
            assert res['msg'] == expected['msg']
            if case['check_sql']:
                sql = Handle_data().replace_data(case['check_sql'])
                sql_result = db.find_one(sql)
                log.debug('----------查询数据库SQL语句为:{},返回结果{}'.format(sql, sql_result))
                assert sql_result is not None
            log.debug('----------{title}用例执行成功----------'.format(title=title))
            self.excel.write_data(row=row, column=8, value='通过')
        except AssertionError as e:
            print('----------{title}用例执行失败----------'.format(title=title))
            log.error('----------{title}用例执行失败----------'.format(title=title))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value='不通过')
            raise e


@pytest.mark.usefixtures('register_fixture')
class TestLoginCase:
    filename = os.path.join(data_path, 'apicases.xlsx')
    excel = Handle_Excel(filename, 'login')
    datas = excel.read_data()

    @pytest.mark.parametrize('case', datas)
    def test_login(self, case):
        # 准备测试数据
        print(case)
        method = case['method']
        url = case['url']
        title = case['title']
        row = case['case_id'] + 1
        data = eval(Handle_data().replace_data(case['data']))
        expected = eval(case['expected'])
        log.debug('----------开始执行{}用例的登录请求发送，请求入参{}'.format(title, data))
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        print('登录接口中{}用例入参:'.format(title), data)
        print('登录接口中{}用例出参:'.format(title), res)
        log.debug('----------{}用例的登录请求出参{}'.format(title, data))
        try:
            assert res['code'] == expected['code']
            assert res['msg'] == expected['msg']
            log.debug('----------{title}用例执行成功----------'.format(title=title))
            self.excel.write_data(row=row, column=8, value='通过')
        except AssertionError as e:
            print('----------{title}用例执行失败----------'.format(title=title))
            log.error('----------{title}用例执行失败----------'.format(title=title))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value='不通过')
            raise e


@pytest.mark.usefixtures('login_fixture')
class TestRechargeCase:
    filename = os.path.join(data_path, 'apicases.xlsx')
    excel = Handle_Excel(filename, 'recharge')
    datas = excel.read_data()

    @pytest.mark.parametrize('case', datas)
    def test_recharge(self, case):
        print(case)
        url = conf.get('evn', 'url') + case['url']
        method = case['method']
        title = case['title']
        row = case['case_id'] + 1
        data = eval(Handle_data().replace_data(case['data']))
        headers['Authorization'] = getattr(Env, 'token')
        expected = eval(case['expected'])
        # 获取充值前账户金额
        if case['check_sql']:
            sql = case['check_sql'].format(getattr(Env, 'member_id'))
            start_ex = db.find_one(sql)
            start_amount = start_ex['leave_amount']
            log.debug('----------充值前查询数据库SQL语句为:{},返回结果{}'.format(sql, start_ex))
        log.debug('----------开始执行{}用例的充值请求发送，请求入参{}'.format(title, data))
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        print('充值接口中{}用例入参:'.format(title), data)
        print('充值接口中{}用例出参:'.format(title), res)
        log.debug('----------开始执行{}用例的充值请求出参{}'.format(title, data))
        try:
            assert res['code'] == expected['code']
            assert res['msg'] == expected['msg']
            if case['check_sql']:
                sql = case['check_sql'].format(getattr(Env, 'member_id'))
                end_ex = db.find_one(sql)
                end_amount = end_ex['leave_amount']
                log.debug('----------充值后查询数据库SQL语句为:{},返回结果{}'.format(sql, end_ex))
                recharge_money = decimal.Decimal(str(data['amount']))
                assert end_amount - start_amount == recharge_money
            log.debug('----------{title}用例执行成功----------'.format(title=title))
            self.excel.write_data(row=row, column=8, value='通过')
        except AssertionError as e:
            print('----------{title}用例执行失败----------'.format(title=title))
            log.error('----------{title}用例执行失败----------'.format(title=title))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value='不通过')
            raise e


if __name__ == '__main__':
    pytest.main(['-sv', 'test_lemon.py'])
    # pytest.main(['-sv', '-k', 'recharge', 'test_lemon.py::TestRechargeCase'])
    # pytest.main(['-sv', 'test_lemon.py::TestLoginCase'])
