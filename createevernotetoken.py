#!/usr/bin/env python
# coding=utf-8
#################################################
# Author:             Billin9
# Company:            DoSec Inc.
# Created on          2019-04-17 17:48:51
# Last Modified by:   Billin9
# Last Modified time: 2019-04-22 11:20:39
# Usage: ./createevernotetoken.py
#################################################

import re
import json
import requests
from bs4 import BeautifulSoup


class CreatedEvernoteToken(object):
    """docstring for CreatedEvernoteToken"""

    def __init__(self, username, password, cfgpath):
        super(CreatedEvernoteToken, self).__init__()
        self.headers = {
            'Host': 'app.yinxiang.com',
            'Origin': 'https://app.yinxiang.com',
            'Referer': 'https://app.yinxiang.com/Login.action',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        self.login_url = "https://app.yinxiang.com/Login.action"
        self.token_url = "https://app.yinxiang.com/api/DeveloperToken.action"
        self.session = requests.session()
        self.username = username
        self.password = password
        self.cfgpath = cfgpath

    def get_login_info(self):
        html = self.session.get(self.login_url, headers=self.headers).content
        soup = BeautifulSoup(html, 'lxml')

        script = soup.findAll('script')[3].string
        hpts = re.search(r'hpts".*= "(.*)";', script).group(1)
        hptsh = re.search(r'hptsh".*= "(.*)";', script).group(1)
        _sourcePage = soup.select('input[name="_sourcePage"]')[0].get('value')
        __fp = soup.select('input[name="__fp"]')[0].get('value')
        # print("hpts: {}, hptsh: {}, _sourcePage: {}, __fp: {}".format(hpts, hptsh, _sourcePage, __fp))

        data = {
            'username': self.username,
            'password': self.password,
            'login': '登录',
            'analyticsLoginOrigin': 'login_action',
            'clipperFlow': "false",
            'showSwitchService': "true",
            'usernameImmutable': "false",
            'hpts': hpts,
            'hptsh': hptsh,
            'targetUrl': '/api/DeveloperToken.action',
            '_sourcePage': _sourcePage,
            '__fp': __fp
        }

        return data

    def login(self):
        data = self.get_login_info()
        try:
            self.session.post(self.login_url, data=data, headers=self.headers)
        except Exception as e:
            print(e)

        # self.session.cookies.clear()

    def create_token(self):

        headers = {
            'Host': 'app.yinxiang.com',
            'Origin': 'https://app.yinxiang.com',
            'Referer': 'https://app.yinxiang.com/api/DeveloperToken.action',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }

        token_page = self.session.get(self.token_url, headers=headers).text
        soup = BeautifulSoup(token_page, 'lxml')
        p = soup.findAll('p')[1].string
        is_already = re.search(r'Your Developer Token has already been created', p)

        if is_already is None:
            secret = soup.select('input[name="secret"]')[0].get('value')
            csrfBusterToken = soup.select('input[name="csrfBusterToken"]')[0].get('value')
            _sourcePage = soup.select('input[name="_sourcePage"]')[0].get('value')
            __fp = soup.select('input[name="__fp"]')[0].get('value')

            data = {
                'secret': secret,
                'csrfBusterToken': csrfBusterToken,
                '_sourcePage': _sourcePage,
                '__fp': __fp
            }

            cdata = dict(data, **{'create': 'Create a developer token'})
            # rdata = dict(data, **{'remove': 'Revoke your developer token',
                                            # 'noteStoreUrl': 'https://app.yinxiang.com/shard/s1/notestore'})
            # remove_token_page = self.session.post(self.token_url, data=rdata, headers=headers)
            create_token_page = self.session.post(self.token_url, data=cdata, headers=headers)

            # print('删除 token 返回状态', remove_token_page)
            print('创建 token 返回状态', create_token_page)

            soup = BeautifulSoup(create_token_page.text, 'lxml')
            token = soup.select('#token')[0].get('value')

            sublime_settings = {
                'noteStoreUrl': 'https://app.yinxiang.com/shard/s1/notestore',
                'token': token
            }

            with open(self.cfgpath, 'w') as f:
                json.dump(sublime_settings, f, indent=4)
                print('成功写入配置文件')
        else:
            print('Token 没有过期')


if __name__ == '__main__':
    from config import *
    evernote = CreatedEvernoteToken(name, pwd, cfg)
    evernote.login()
    evernote.create_token()
