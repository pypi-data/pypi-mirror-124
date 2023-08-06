#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: xiaoli
# @Software: PyCharm
# @File : QuanMingCollectionService.py
# @Time : 2021/7/6 19:02
from protocol_helper.utils import request


class QuanMingCollectionService:
    def __init__(self):
        super(QuanMingCollectionService, self).__init__()

    """全民"""
    URL_STATUS_KGE = '全民'
    """未定义"""
    URL_STATUS_ERROR = 'error'

    URL_STATUS_LABEL = {
        URL_STATUS_KGE: '全民',
        URL_STATUS_ERROR: '未定义'
    }

    TIMEOUT = 30
    URL_TYPE_STATUS = None

    def get_request(self, share_url,proxies=None):
        """

        Args:
            share_url:

        Returns:

        """
        try:
            if 'https' in share_url or 'http' in share_url:
                res = request.get(url = share_url, timeout = self.TIMEOUT,proxies = proxies)
                return res
            import re
            if re.findall(r'(\S+)', share_url)[0]:
                res = request.get(url = f'https://kg3.qq.com/node/67n7o63p4Z/play_v2?s={share_url}',
                                  timeout = self.TIMEOUT, proxies = proxies)
                return res
        except Exception as _error:
            return f'获取异常 {_error}'

    def collection_information(self, url,proxies=None):
        """
        采集信息
        :param url:
        :return:
        """
        import re
        data = self.get_request(url,proxies = proxies)
        try:
            if data is None:
                share_id = url
            else:
                share_id = re.findall(r's=(\w+([-+.]\w+)*)', data.url)[0][0]

            status = self.URL_STATUS_KGE
            return {"code": 0, "id": share_id, "type": status}

        except Exception as _error:
            return f'获取异常 {_error}'
