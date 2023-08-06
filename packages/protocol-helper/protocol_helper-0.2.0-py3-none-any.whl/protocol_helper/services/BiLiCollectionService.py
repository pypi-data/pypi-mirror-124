#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : BiLiCollectionService.py
# @Time : 2021/6/25 15:12
import re
from protocol_helper.utils import request


class BiLiCollectionService:
    def __init__(self):
        super(BiLiCollectionService, self).__init__()

    """文章"""
    URL_STATUS_READ = 'read'
    """用户"""
    URL_STATUS_USER = 'space'
    """视频"""
    URL_STATUS_VIDEO = 'video'
    """番剧"""
    URL_STATUS_PLAY = 'paly'
    """未定义"""
    URL_STATUS_ERROR = 'error'

    URL_STATUS_LABEL = {
        URL_STATUS_READ: '文章',
        URL_STATUS_USER: '用户主页',
        URL_STATUS_VIDEO: '视频',
        URL_STATUS_PLAY: '番剧',
        URL_STATUS_ERROR: '未定义'
    }
    HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 2AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36",
    }
    TIMEOUT = 60
    URL_TYPE_STATUS = None

    def bili_request(self, share_url,proxies=None):
        """
        # 请求链接，得到数据
        :param share_url: 提交的链接
        :return:
        """
        if 'https' in share_url or 'http' in share_url:
            res = request.get(url = share_url, headers = self.HEADERS, verify = False, timeout = self.TIMEOUT,proxies=None)
            validate_url = res.url
            if validate_url.find('space') > -1:
                share_id = re.findall(r'bilibili.com/([0-9.]+)', validate_url)[0]
                res = request.get(url = f'https://api.bilibili.com/x/space/acc/info?mid={share_id}&jsonp=jsonp',
                               headers = self.HEADERS, verify = False, timeout = self.TIMEOUT,proxies=proxies).json()
            elif validate_url.find('read') > -1:
                share_id = re.findall(r'cv([0-9.]+)', validate_url)[0]
                res = request.get(
                        url = f'https://api.bilibili.com/x/article/viewinfo?id={share_id}&jsonp=jsonp').json()

        elif 'www' in share_url:
            validate_url = share_url
            if validate_url.find('video') > -1:
                res = request.get(url = f'https://{share_url}', headers = self.HEADERS, verify = False,
                               timeout = self.TIMEOUT,proxies=proxies)
            elif validate_url.find('space') > -1:
                share_id = re.findall(r'bilibili.com/([0-9.]+)', validate_url)[0]
                res = request.get(url = f'https://api.bilibili.com/x/space/acc/info?mid={share_id}&jsonp=jsonp').json()

            elif validate_url.find('read') > -1:
                share_id = re.findall(r'cv([0-9.]+)', validate_url)[0]
                res = request.get(url = f'https://api.bilibili.com/x/article/viewinfo?id={share_id}&jsonp=jsonp').json()
            elif validate_url.find('play') > -1:
                res = request.get(url = f'https://{share_url}', headers = self.HEADERS, verify = False,
                               timeout = self.TIMEOUT,proxies=proxies)
            else:
                return '未定义类型。目前支持视频，主页链接'

        elif share_url.startswith('BV'):
            url = f"https://www.bilibili.com/video/{share_url}"
            res = request.get(url = url, headers = self.HEADERS, verify = False, timeout = self.TIMEOUT,proxies=proxies)

        elif share_url.startswith('cv'):
            share_id = re.findall(r'cv([0-9.]+)', share_url)[0]
            res = request.get(url = f'https://api.bilibili.com/x/article/viewinfo?id={share_id}&jsonp=jsonp').json()

        else:
            share_id = share_url
            res = request.get(url = f'https://api.bilibili.com/x/space/acc/info?mid={share_id}&jsonp=jsonp',proxies=proxies).json()
            if res['code'] == 0:
                return res
            else:
                return '未定义类型。目数前支持主页字id'

        return res

    def bili_collection(self, res, share_url,proxies=None):
        share_url = res.url
        if share_url.find('video') > -1 or share_url.startswith('BV'):
            status = self.URL_STATUS_VIDEO
            if share_url.startswith('BV'):
                share_id = share_url
            else:
                share_id = re.findall(r'video/([a-zA-Z0-9.]+)', share_url)[0]
            bili_name = re.findall(r'name="author" content="(.*?)"', res.text)[0]
            introduction = re.findall(r'name="title" content="(.*?)"', res.text)[0]
            data = {
                'bili_name': bili_name,
                'introduction': introduction
            }
        elif share_url.find('space') > -1:
            share_id = re.findall(r'bilibili.com/([0-9.]+)', share_url)[0]
            if res['code'] == 0:
                status = self.URL_STATUS_USER
                data = {
                    'bili_name': res['data']['name'],
                    'introduction': res['data']['sign'],
                    'content': res['data']
                }
        elif share_url.find('read') > -1 or share_url.startswith('cv'):
            share_id = re.findall(r'cv([0-9.]+)', share_url)[0]
            if res['code'] == 0:
                status = self.URL_STATUS_READ
                data = {
                    'bili_name': res['data']['author_name'],
                    'introduction': res['data']['title'],
                    'content': res['data']
                }
        elif share_url.find('play') > -1:
            status = self.URL_STATUS_PLAY
            share_id = share_url.split('/')[5]
            bili_name = re.findall(r'<title>(.*?)</title>', res.text)[0]
            data = {
                'bili_name': bili_name,
                'introduction': bili_name
            }
        else:
            share_id = share_url
            if res['code'] == 0:
                status = self.URL_STATUS_USER
                data = {
                    'bili_name': res['data']['name'],
                    'introduction': res['data']['sign'],
                    'content': res['data']
                }

        return {"id": share_id,
                "type": status,
                "data": data,
                }
