#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/3 10:46
# @Author  : Holden
# @Site    : 
# @File    : WeiBoH5collectionService
# @Software: PyCharm
import json
from abc import ABC
from protocol_helper.exceptions import WeiBoH5SideRestrictions, DefaultException
from protocol_helper.utils import request
from protocol_helper.services import WeiBoBaseService


class WeiBoH5collectionService(WeiBoBaseService, ABC):

    def __init__(self):
        super(WeiBoH5collectionService, self).__init__()

    def wb_h5_get_latest_news(self, uid, proxies = None,**kwargs):
        """
        通过h5的接口获取最新的动态
        :param uid:
        :return:
        """
        params = {
            "uid": uid,
            "luicode": 10000011,
            "lfid": f"230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO",
            "type": "uid",
            "value": uid,
            "containerid": f"107603{uid}"
        }
        resp = request.get(f'https://m.weibo.cn/api/container/getIndex', params = params, proxies = proxies,**kwargs)
        dates = json.loads(resp.text)
        if dates.get('ok', None) != 1:
            raise WeiBoH5SideRestrictions(f'获取数据失败:{dates}')
        return dates

    def get_comments(self, mid, cookie, max_id = 0, proxies = None,**kwargs):
        header = {
            'authority': 'm.weibo.cn',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'accept': 'application/json, text/plain, */*',
            'mweibo-pwa': '1',
            'x-xsrf-token': '3914b9',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?1',
            'user-agent':       'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 ('
                                'KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
            'sec-fetch-site':   'same-origin',
            'sec-fetch-mode':   'cors',
            'sec-fetch-dest':   'empty',
            'accept-language':  'zh-CN,zh;q=0.9',
            'Cookie':           cookie
        }
        params = (
            ('id', mid),
            ('mid', mid),
            ('max_id', max_id),
            ('max_id_type', '0'),
        )
        return request.get('https://m.weibo.cn/comments/hotflow', headers = header, params = params,
                           proxies = proxies,**kwargs).json()
