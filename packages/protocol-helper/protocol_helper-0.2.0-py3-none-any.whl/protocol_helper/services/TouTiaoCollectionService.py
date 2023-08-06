#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : TouTiaoCollectionService.py
# @Time : 2021/7/6 10:03
import json
from protocol_helper.utils import request


class TouTiaoCollectionService:
    def __init__(self):
        super(TouTiaoCollectionService, self).__init__()

    HEADERS = {
        'User-Agent': 'com.ss.android.article.news/7500 (Nexus 6)',

    }
    TIMEOUT = 60
    URL_TYPE_STATUS = None

    def works_request(self, url,proxies=None):
        """
        今日头条作品信息请求
        :param url:
        :return:
        """
        import re
        if 'm.toutiao.com' in url:
            res = request.get(url)
            url_list = re.findall(r'(\d{16,19})', res.url)
            mid = url_list[0]
            url = 'https://www.toutiao.com/article/v2/tab_comments/?aid=24&app_name=toutiao_web&offset=0&count=20' \
                  '&group_id={}&item_id={}'.format(
                    mid, mid)
            info = request.get(url, proxies = proxies)
            return {'info': info, 'mid': mid}
        url_list = re.findall(r'(\d{16,19})', url)
        if not url_list:
            try:
                res = request.get(url)
                _url = res["url"]
                url_list = re.findall(r'group_id=(\d{16,19})', _url)
            except Exception as e:
                return f'网址格式不支持,需要有19位数字ID：{url}'
            if not url_list:
                return f'网址格式不支持,需要有19位数字ID：{url}'
        mid = url_list[0]
        url = 'https://www.toutiao.com/article/v2/tab_comments/?aid=24&app_name=toutiao_web&offset=0&count=20' \
              '&group_id={}&item_id={}'.format(
                mid, mid)
        try:
            info = request.get(url,proxies=proxies)
            return {'info': info, 'mid': mid}

        except Exception as _error:
            return f'获取异常 {_error}'

    def works_collection(self, url,proxies=None):
        """
        采集作品信息
        :param url:
        :return:
        """
        data_info = self.works_request(url,proxies = proxies)
        try:
            info_ = json.loads(data_info['info'].text)
            if info_.get('message', '') != 'success':
                return f'获取头条失败：{info_}'
            data = {}
            data['mid'] = data_info['mid']
            data['text'] = info_['repost_params'].get('title', '')
            data['uid'] = info_['repost_params'].get('fw_user_id', '')
            data['nickname'] = info_['group'].get('user_name', '')
            data['comment_count'] = info_.get('total_number', 0)  # 评论数
            data['share_count'] = info_.get('post_count', 0)  # 分享数
            data['like_count'] = info_.get('like_count', 0)  # 点赞数
            data['read_count'] = info_.get('read_count', 0)  # 阅读量
            data['video_read_count'] = info_.get('video_watch_count', None)  # 视频播放数
            data['user'] = info_.get('group', 0)  # 作者信息
            data_list = []
            for i in info_['data']:
                data_list.append(i['comment']['text'])
            data['comments'] = data_list  # 评论内容
            return {'code': 0, 'data': data}
        except Exception as _error:
            return f'获取异常 {_error}'

    def homepage_request(self, url,proxies=None):
        """
        主页作品请求
        :param url: 主页链接
        :return:
        """
        import re
        url_list = url.split('/')[6]
        if not url_list:
            return f'网址格式不支持,需要有token的：{url}'

        url = f'https://www.toutiao.com/c/user/token/{url_list}/'

        self.HEADERS = {
            'authority': 'ttwid.bytedance.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.toutiao.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.toutiao.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        data = '{"aid":24,"service":"www.toutiao.com","region":"cn","union":true,"needFid":false}'

        response = request.post('https://ttwid.bytedance.com/ttwid/union/register/', headers = self.HEADERS,
                                data = data,proxies=proxies)
        Set_Cookie = response.headers['Set-Cookie']
        ttwid = re.findall(r'ttwid=(.*?);', Set_Cookie)[0]

        self.HEADERS = {
            'authority': 'www.toutiao.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.toutiao.com/w/a1699192093136972/',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'ttwid=' + ttwid,
        }
        params = (
            ('source', 'weitoutiao_detail'),
        )
        try:
            info = request.get(url, self.HEADERS, data = params)
            data_param = {
                'token': url_list
            }
            info_data = request.post('https://www.toutiao.com/api/pc/user/fans_stat', data = data_param)
            return {'info': info, 'info_data': info_data, 'url_list': url_list}
        except Exception as _error:
            return f'获取异常 {_error}'

    def homepage_collection(self, url,proxies=None):
        """
        主页信息采集
        :param url:
        :return:
        """
        from lxml import etree
        data_info = self.homepage_request(url,proxies = proxies)
        data = {}
        try:
            page_data = etree.HTML(data_info['info'].text)
            data['nickname'] = page_data.xpath('//div/a/span[@class="name"]/text()')[0]  # 用户名称
            data['verified_agency'] = page_data.xpath('//a[@class="des"]/text()')  # 认证机构
            data['text'] = page_data.xpath('//p[@class="intro-info"]/text()')[1]  # 简介
            info_ = json.loads(data_info['info_data'].text)
            data['uid'] = data_info['url_list']
            data['fans_count'] = info_['data'].get('fans', 0)  # 粉丝数
            data['publish_count'] = info_['data'].get('digg_count', 0)  # 作品数量
            data['followings_count'] = info_['data'].get('following', 0)  # 关注数
            return {'code': 0, 'data': data}
        except Exception as _error:
            return f'获取异常 {_error}'
