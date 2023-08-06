#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : XiaoHongShuCollectionService.py
# @Time : 2021/7/6 15:27
import re
from protocol_helper.utils import request


class XiaoHongShuCollectionService:
    def __init__(self):
        super(XiaoHongShuCollectionService, self).__init__()

    HEADERS = {
        'Cookie': 'hasaki=1',  # 长链接加上这个才能取到正文
        # 默认用手机user-agent
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 '
                      'MQQBrowser/8.9 Mobile Safari/537.36',
    }

    def works_request(self, url,proxies=None):
        """
        请求作品链接
        :param url:作品链接
        :return:
        """
        try:
            source_url = url
            if 'http' not in source_url:
                url = f'https://www.xiaohongshu.com/discovery/item/{source_url}'
            data = {}
            from urllib.parse import unquote, parse_qs
            url = unquote(url)
            if 'redirectPath' in url:
                for k, value_list in parse_qs(url).items():
                    if 'redirectPath' in k:
                        url = value_list[0]
                        break
            resp = request.get(url, proxies=proxies, timeout=3)

            if 'Temporary Redirect' in resp.text:
                url_list = re.findall('<a href="(.*?)">', resp['response'])
                if url_list:
                    url = unquote(url_list[0])
                    url = url.split('?', 1)[0]
            if 'xhslink' in url:
                long_url = resp.url
                mid = long_url.split('%2F')[-1].split('%3F')[0]
                if mid:
                    data['url'] = source_url
                    data['mid'] = mid
                    return {'code': 0, 'data': data, 'resp': resp}
            if 'discovery/item' in url:
                mid = url.rsplit('/', 1)[-1].split("?")[0]
                if mid:
                    data['url'] = source_url
                    data['mid'] = mid
                    return {'code': 0, 'data': data, 'resp': resp}
            if 'xiaohongshu.com' not in url:
                url = resp.url
                resp = request.get(url,proxies=proxies)
                return resp
        except Exception as _error:
            return {"code": 107, "msg": f'获取失败 {_error}', 'response': f'获取失败 {_error}'}

    def works_collection(self, url,proxies=None):
        """
        采集作品信息
        :param url:作品链接
        :return:
        """
        try:
            resp = self.works_request(url,proxies=proxies)
            data = resp['data']
            return {'code': 0, 'data': data}
        except Exception as _error:
            return {"code": 107, "msg": f'获取失败 {_error}', 'response': f'获取失败 {_error}'}

    def homepage_request(self, url,proxies=None):
        """
        请求主页链接
        :param url:主页链接
        :return:
        """
        try:
            resp = request.get(url,proxies=proxies)
            return resp

        except Exception as _error:
            return f'获取失败 {_error}'

    def homepage_collection(self, url,proxies=None):
        """
        采集主页信息
        :param url:主页链接
        :return:
        """
        resp = self.homepage_request(url,proxies=proxies)
        data = {}
        try:
            data['url'] = resp.url
            uid = re.findall(r'profile%2F(\w+)|vendor/(\w+)', resp.url)
            for i in uid:
                for j in list(i):
                    if j != '':
                        data['uid'] = j

            return {'code': 0, 'data': data}

        except Exception as _error:
            return f'获取失败 {_error}'
