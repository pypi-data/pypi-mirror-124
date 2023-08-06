# -*- coding: utf-8 -*-
# @Time    : 2021/6/30 9:23
# @Author  : sunfukai
# @Email   : zcshiyonghao@163.com
# @File    : WeChatVoteService.py
# @Software: PyCharm
import re
import json
from protocol_helper.utils import request


class WeChatService:
    def __init__(self):
        super(WeChatService, self).__init__()

    """投票"""
    URL_STATUS_VOTE = "vote"

    URL_STATUS_LABEL = {
        URL_STATUS_VOTE: '投票',
    }
    HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 2AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36",
    }
    TIMEOUT = 30
    URL_TYPE_STATUS = None

    def get_mpvote_link(self, url,proxies=None):
        """
        获取投票链接的部分参数
        :param url:
        :return:
        """
        resp = request.get(url,proxies=proxies)
        if '该内容已被发布者删除' in resp.text:
            return '该内容已被发布者删除'
        supervoteid = re.findall(r"supervoteid=(\d+)&amp;", resp.text)[0]
        biz = re.findall(r"__biz=(.*?)==", resp.text)[0]
        mpvote_link = f'https://mp.weixin.qq.com/mp/newappmsgvote?action=show&__biz={biz}==&supervoteid={supervoteid}'
        return mpvote_link

    def get_mpvote_json(self, url,proxies=None):
        """
        获取投票信息json格式
        :param url:
        :return:
        """
        mpvote_link = self.get_mpvote_link(url,proxies = proxies)
        resp = request.get(mpvote_link)
        mpvote_json = re.findall(r"var voteInfo = (.*?)};", resp.text)[0]
        mpvote_json = json.loads(mpvote_json + '}')
        return mpvote_json

    def wx_request(self, url,proxies=None):
        """
        请求操作
        :param url: 微信链接
        :return:  返回请求数据
        """
        try:
            res = request.get(url, headers = self.HEADERS, timeout = self.TIMEOUT,proxies = proxies)
            return res
        except Exception as e:
            print(e)

    def wx_collection(self, url,proxies=None):
        """
        获取微信开始数内容
        :param url: 微信链接
        :return:
        """
        try:
            res = self.wx_request(url,proxies = proxies)
            if '参数错误' in res.text:
                return False
            content_list = re.findall(r"var msg_title = '(.*?)'\.html", res.text, re.S)
            nickname = re.findall(r'var nickname = "(.*?)";', res.text, re.S)
            if len(nickname) != 0:
                nickname = nickname[0]
            else:
                nickname = re.findall(r"window\.nickname = '(.*?)'", res.text, re.S)
                if len(nickname) != 0:
                    nickname = nickname[0]
                else:
                    re_str = r"d\.nick_name = xml \? getXmlValue\('nick_name\.DATA'\) : '(.*?)';"
                    nickname = re.findall(re_str, res.text, re.S)
                    if nickname:
                        nickname = nickname[0]
                    else:
                        nickname = ''
            mid = re.findall(r'var user_name = "([\S.]+)"', res.text)
            if content_list:
                content_title = content_list[0]
            else:
                content_list = re.findall(r"window.msg_title = '(.*?)'", res.text, re.S)
                if len(content_list) != 0:
                    content_title = content_list[0]
                else:
                    re_str = r"d\.title = xml \? getXmlValue\('title\.DATA'\) : '(.*?)';"
                    content_list = re.findall(re_str, res.text, re.S)
                    if content_list:
                        content_title = content_list[0]
                    else:
                        content_title = ''
            mid = re.findall(r'var user_name = "([\S.]+)"', res.text)
            if len(mid) != 0:
                mid = mid[0]
            else:
                re_str = r"d.user_name = getXmlValue\('user_name.DATA'\) \|\| '(.*?)';"
                mid = re.findall(re_str, res.text, re.S)
                if not mid:
                    re_str = r"d\.user_name = xml \? getXmlValue\('user_name\.DATA'\) : '(.*?)';"
                    mid = re.findall(re_str, res.text, re.S)
                mid = mid[0]
            content = re.findall(r'var msg_desc = "(.*?)"', res.text, re.S)
            if content:
                content = content[0]
            else:
                content = re.findall(r"window.msg_desc = '(.*?)'", res.text, re.S)
                if len(content) != 0:
                    content = content[0]
                else:
                    content = ''
            user_name = re.findall(r'profile_meta_value\">([a-zA-Z][-_a-zA-Z0-9]{5,19})</', res.text)
            if len(user_name) <= 0:
                user_name = ['']
            if mid and content_title:
                data = {
                    'code': 0,
                    'mid': mid,  # 用户id
                    'user_name': user_name[0],  # 微信公众号名称
                    'content': content,  # 文章内容
                    'content_title': content_title,  # 标题
                    'nickname': nickname,  # 用户昵称
                    'url': res.url
                }
                return data
            else:
                return False
        except Exception as e:
            print(e)
