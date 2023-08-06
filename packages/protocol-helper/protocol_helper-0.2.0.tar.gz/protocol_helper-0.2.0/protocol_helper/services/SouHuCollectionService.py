#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : SouHuCollectionService.py
# @Time : 2021/7/7 9:35
from lxml import etree
import json
from protocol_helper.utils import request


class SouHuCollectionService:
    def __init__(self):
        super(SouHuCollectionService, self).__init__()

    def get_request(self, url, proxies = None):
        """
        请求链接 获取数据
        :param url:
        :return:
        """
        try:
            resp = request.get(url)
            return resp
        except Exception as _error:
            return {"code": 107, "msg": f'获取失败 {_error}', 'response': f'获取失败 {_error}'}

    def get_data(self, id, proxies = None):
        """
        获取部分数据：评论数，阅读量
        :param id: 请求链接需要拼接的id
        :return:
        """
        res = request.get(f'https://api.interaction.sohu.com/api/topics/count?source_ids=mp_{id}', proxies = proxies)
        res_ = request.get(f'https://v2.sohu.com/author-page-api/articles/pv?articleIds={id}', proxies = proxies)
        return {'res': res.text, 'res_': res_.text}

    def collection_information(self, url, proxies = None):
        """
        采集数据
        :param url:
        :return:
        """
        try:
            if 'https://m.sohu.com/a/' in url:
                url = url.replace('https://m.sohu.com/a/', 'https://www.sohu.com/a/')
            resp = self.get_request(url, proxies = proxies)
            if resp.url in ['https://www.sohu.com/', 'https://www.sohu.com/404.html']:
                return {'code': 107, 'data': '地址异常或文章不存在'}
            tree = etree.HTML(resp.text)
            content_title = tree.xpath('/html/head/title/text()')[0]
            text_list = tree.xpath('//*[@id="mp-editor"]//text()')
            text = ''
            for text1 in text_list:
                text += text1
            nick_name = tree.xpath('//*[@id="user-info"]/h4/a/text()')[0]
            if '?' in url:
                url = url.split("?")[0]
                uid = url.split('_')[-1]
                mp_id = url.split('_')[-2].split('/')[-1]
            else:
                uid = url.split('_')[-1]
                mp_id = url.split('_')[-2].split('/')[-1]
            num_data = self.get_data(mp_id)
            _json = json.loads(num_data['res'])
            commentCount = _json["data"][f'mp_{mp_id}']['commentCount']
            json_ = json.loads(num_data['res_'])
            readnumber = json_[f'{mp_id}']

            data = {
                    'uid':            uid,  # 作者id
                    'mid':            mp_id,  # 文章id
                    'content_title':  content_title,  # 标题
                    'name':           nick_name,  # 作者昵称
                    'comments_count': commentCount,  # 评论数
                    'read_count':     readnumber,  # 阅读量
                    'text':           text,  # 内容
            }
            return {'code': 0, 'data': data}
        except Exception as _error:
            return {"code": 107, "msg": f'获取失败 {_error}', 'response': f'获取失败 {_error}'}
