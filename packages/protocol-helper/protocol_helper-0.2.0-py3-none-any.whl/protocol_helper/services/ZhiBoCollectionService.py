#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : ZhiBoCollectionService.py
# @Time : 2021/7/7 10:23
from lxml import etree
from protocol_helper.utils import request


class ZhiBoCollectionService:
    def __init__(self):
        super(ZhiBoCollectionService, self).__init__()

    """直播中"""
    URL_STATUS_LIVE = '直播中'

    URL_STATUS_LABEL = {
        URL_STATUS_LIVE: '直播中', }

    def get_memberid(self, id,proxies=None):
        """
        获取直播id
        :param id:
        :return:
        """
        url = "https://www.yizhibo.com/member/so_h5api/search_member?p_from=Phome_search"
        _headers = {
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = {
            'key': id,
            'page': 1,
            'limit': 20
        }
        response = request.post(url, data = data, headers = _headers,proxies=proxies).json()
        msg = response.get("msg", "")
        if msg != "":
            return str(response)
        user_list = response['data']['list']
        if len(user_list) == 0:
            return str(response)
        else:
            for user in user_list:
                fans_count = str(user['fans_count'])
                if "万" in fans_count:
                    fans_count = float(fans_count.replace("万", "").replace(".", "")) * 1000
                else:
                    fans_count = int(fans_count)
                level = user['level']
                nickname = user['nickname']
                scid = user.get("scid", "")
                memberid = user['memberid']
                data = {
                    'fans_count': fans_count,
                    'level': level,
                    'nickname': nickname,
                    'scid': scid,
                    'memberid': memberid
                }
        return data

    def Live_broadcast(self, id,proxies=None):
        """
        采集数据
        :param id:
        :return:
        """
        data = self.get_memberid(id,proxies=proxies)
        if not isinstance(data, dict):
            print("主播不存在")
            return {'code': 0, 'msg': '没有这个用户', 'response': str(data)}
        data['id'] = id
        id = data['memberid']
        response = request.get(url = f"https://www.yizhibo.com/member/personel/user_works?memberid={id}", )
        html = etree.HTML(response.text)
        uls = html.xpath("//ul[@class='index_all index_all_all cf']//li")

        for ul in uls:
            status = "".join(ul.xpath(".//div[@class='index_state pa tc']//text()")).strip()
            live_url = "https://www.yizhibo.com" + "".join(
                    ul.xpath(".//a[@class='index_img_hover pa dn']/@href")).strip()
            maxonline = "".join(html.xpath(".//div[@class='index_num fl']//text()")).strip().replace("人", "")
            if status == "直播中":
                data.update({
                    'status': self.URL_STATUS_LIVE,
                    'Live_url': live_url,
                    'heat': maxonline
                })
        if data.get("status", "") == "":
            return {'code': 0, 'msg': '没有正在直播', 'response': str(response.text)}
        return {'code': 0, 'data': data, 'response': str(response.text)}
