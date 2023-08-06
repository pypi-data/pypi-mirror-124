#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:34
# software: PyCharm
from abc import ABC
from protocol_helper.exceptions import (RequestException, NeedToLogin, DefaultException, URLErrorAbnormal,
                                        NotTakeOverException)
from protocol_helper.utils import request
from protocol_helper.services import WeiBoBaseService,eoms


def clothes(func):
    def wear(*args, **kwargs):
        cls = args[0]
        _res = func(*args, **kwargs)
        cls.reduction_tourist()
        return _res
    return wear


class WeiBoAppCollectionService(WeiBoBaseService, ABC):

    def __init__(self, uid=None, gsid=None, aid=None, s=None, comment_s = None):
        super(WeiBoAppCollectionService, self).__init__()

        # 默认访问
        self.uid = uid
        self.gsid = gsid
        self.aid = aid
        self.s = s
        self.comment_s = comment_s

        # 登录账号
        self.logged_uid = uid
        self.logged_gsid = gsid
        self.logged_aid = aid
        self.logged_s = s
        self.logged_comment_s = comment_s

        # 游客登录账号
        self.tourist_uid = None
        self.tourist_gsid = None
        self.tourist_aid = None
        self.tourist_s = None
        self.tourist_comment_s = None

        self.ua = "BLA-AL00_6.0.1_WeiboIntlAndroid_3660"
        self.is_login = False
        self.eoms = eoms()

    def update_tourist(self, uid, gsid, aid, s, comment_s = None, login_status=False):
        """
        login_status 登录状态：True 游客登录：False
        """
        self.uid = uid
        self.gsid = gsid
        self.aid = aid
        self.s = s
        self.comment_s = comment_s
        if login_status:
            self.logged_uid = uid
            self.logged_gsid = gsid
            self.logged_aid = aid
            self.logged_s = s
            self.logged_comment_s = comment_s
        else:
            self.tourist_uid = uid
            self.tourist_gsid = gsid
            self.tourist_aid = aid
            self.tourist_s = s
            self.tourist_comment_s = comment_s

    def reduction_tourist(self):
        if self.uid == self.logged_uid and self.s == self.logged_s and self.aid == self.logged_aid:
            print("还原设置")
            self.uid = self.tourist_uid
            self.gsid = self.tourist_gsid
            self.aid = self.tourist_aid
            self.s = self.tourist_s
            self.comment_s = self.tourist_comment_s

    @clothes
    def get_topics(self, title, proxies = None,**kwargs):
        """
        获取话题数据
        Args:
            title:话题内容
            custom_login: 是否使用自定义登录
        Returns:

        """
        params = {
            "v_f":         "2",
            "s":           self.s,
            "source":      "4215535043",
            "wm":          "2468_1001",
            "gsid":        self.gsid,
            "count":       "20",
            "containerid": f"231522type%3D1%26q%3D{title}",
            "from":        "1299295010",
            "i":           "4366450",
            "c":           "weicoabroad",
            "ua":          self.ua,
            "lang":        "zh_CN",
            "page":        "1",
            "aid":         self.aid,
            "v_p":         "72"
        }
        return request.get('https://api.weibo.cn/2/cardlist', params = params, proxies = proxies,**kwargs).json()

    @clothes
    def get_article(self, mid, proxies = None,**kwargs):
        """
        获取文章数据
        Args:
            mid: 只支持 4646504838991322
            custom_login: 是否使用自定义登录
        Returns:

        """
        params = {
            "s":             self.s,
            "source":        "4215535043",
            "c":             "weicoabroad",
            "id":            mid,
            "wm":            "2468_1001",
            "gsid":          self.gsid,
            "isGetLongText": "1",
            "ua":            self.ua,
            "lang":          "zh_CN",
            "from":          "1299295010",
            "aid":           self.aid
        }
        data = request.get('https://api.weibo.cn/2/statuses/show', params = params, proxies = proxies,**kwargs).json()
        if data.get('errmsg', "").find('login user in official client/website!') >= 0:
            raise NeedToLogin(data.get('errmsg', data))

        if data.get('errmsg', None) is not None:
            raise DefaultException(data.get('errmsg', data))

        return data

    @clothes
    def get_comment_mid(self, rid, flow = "1", max_id = "0", proxies = None,**kwargs):
        """
        获取评论id数据
        Args:
            rid:评论id
            flow:排序规则 1:时间排序  0：热度排序
            max_id:翻页
            custom_login:是否使用自定义登录
        Returns:

        """
        if self.comment_s == None:
            raise DefaultException("评论comments为空")
        params = {
            "s":                self.comment_s,
            "source":           "4215535043",
            "wm":               "2468_1001",
            "gsid":             self.gsid,
            "count":            "20",
            "from":             "1081095010",
            "is_reload":        "1",
            "c":                "weicoabroad",
            "id":               rid,
            "ua":               self.ua,
            "lang":             "zh_CN",
            "is_show_bulletin": "2",
            "aid":              self.aid,
            "flow":             str(flow),
            "v_p":              "72",
            "max_id":           str(max_id)
        }
        return request.get('https://api.weibo.cn/2/comments/build_comments', params = params, proxies = proxies,**kwargs).json()

    @clothes
    def get_fans(self, uid = None, screen_name = None, proxies = None,**kwargs):
        """
        获取粉丝数据 两者只能存在一个
        Args:
            uid:
            screen_name:
            custom_login: 是否使用自定义登录
        Returns:

        """
        params = {
            "s":           self.s,
            "screen_name": screen_name,
            "source":      "4215535043",
            "c":           "weicoabroad",
            "wm":          "2468_1001",
            "gsid":        self.gsid,
            "ua":          self.ua,
            "lang":        "zh_CN",
            "uid":         uid,
            "from":        "1299295010",
            "aid":         self.aid,
        }
        resp = request.get('https://api.weibo.cn/2/users/show', params = params, proxies = proxies,**kwargs).json()
        print(resp)
        if resp.get('errmsg', "").find('客户端身份校验失败') >= 0:
            raise NeedToLogin(resp.get('errmsg', resp))
        if resp.get("errmsg", None) in ['该用户不存在', '你的帐号存在异常，暂时无法发博、发评论、加关注等，请先验证身份解除异常。']:
            raise URLErrorAbnormal(resp.get('errmsg', resp))
        if resp.get('errmsg', None) is not None:
            raise DefaultException(resp.get('errmsg', resp))
        return resp

    @clothes
    def get_user_profile_statuses(self, uid, page = 1, proxies = None,**kwargs):
        """
        获取主页博文
        Args:
            uid:
            page:
            custom_login:

        Returns:

        """
        params = {
            "need_new_pop":    "0",
            "v_f":             "2",
            "s":               self.s,
            "source":          "4215535043",
            "wm":              "2468_1001",
            "gsid":            self.gsid,
            "fid":             f"107603{uid}_-_WEIBO_SECOND_PROFILE_WEIBO",
            "need_head_cards": "0",
            "count":           "20",
            "containerid":     f"107603{uid}_-_WEIBO_SECOND_PROFILE_WEIBO",
            "from":            "1299295010",
            "c":               "weicoabroad",
            "ua":              self.ua,
            "lang":            "zh_CN",
            "uid":             uid,
            "page":            page,
            "aid":             self.aid,
            "v_p":             "82"
        }
        resp = request.get('https://api.weibo.cn/2/profile/statuses', params = params, proxies = proxies,**kwargs).json()
        if resp.get('errmsg', "").find('客户端身份校验失败') >= 0:
            raise NeedToLogin(resp.get('errmsg', resp))
        if resp.get('errmsg', None) is not None:
            raise DefaultException(resp.get('errmsg', resp))
        return resp

    @clothes
    def get_topic_id(self, topic_id, proxies = None,**kwargs):
        """
        获取超话数据
        Args:
            topic_id:
            custom_login:

        Returns:

        """
        params = {
            "since_id":    "0",
            "s":           self.s,
            "source":      "4215535043",
            "c":           "weicoabroad",
            "wm":          "2468_1001",
            "gsid":        self.gsid,
            "ua":          self.ua,
            "lang":        "zh_CN",
            "count":       "20",
            "containerid": topic_id,
            "from":        "1299295010",
            "aid":         self.aid,
            "v_p":         "72"
        }
        resp = request.get('https://api.weibo.cn/2/page', params = params, proxies = proxies,**kwargs)
        return resp.json()

    @clothes
    def get_user_follower_and_fans(self, uid, followers_or_fans = 'followers', page = 1,
                                   proxies = None,**kwargs):
        if followers_or_fans == 'followers':
            page_type = 'page'
        else:
            page_type = 'since_id'
        _headers = {
            'User-Agent':   'letv x500_5.1.1_weibo_7.5.2_android',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        param = {
            "since_id":    "2",
            "v_f":         "2",
            "s":           self.s,
            "source":      "4215535043",
            "wm":          "2468_1001",
            "gsid":        self.gsid,
            "count":       "20",
            "containerid": f"231051_-_{followers_or_fans}_-_{uid}",
            "from":        "1299295010",
            "i":           "59a20e4",
            "c":           "weicoabroad",
            "ua":          self.ua,
            "lang":        "zh_CN",
            "aid":         self.aid,
            page_type:     page
        }
        resp = request.get('https://api.weibo.cn/2/cardlist', params = param, headers = _headers, proxies = proxies,**kwargs)
        return resp

    def guest_login(self,proxies=None,**kwargs):
        """

        Returns:

        """

        # 获取设备
        try:
            self.PROXIES = None
            resp = self.eoms.get_weibo_registered_equipment()
        except RequestException as error:
            raise error
        except Exception as error:
            raise NotTakeOverException(error)
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':         'api.weibo.cn',
                'User-Agent':   'okhttp/3.12.1'
        }
        # 注册设备可用
        data = resp['data']['equipment']
        resp = request.post('https://api.weibo.cn/2/guest/login', data = data, headers = headers, proxies = proxies,**kwargs)
        if resp.status_code != 200:
            raise RequestException(resp)
        data = resp.json()
        if data.get('errmsg', None):
            return data.get('errmsg', None)
        self.tourist_uid = data['uid']
        self.tourist_gsid = data['gsid']
        self.tourist_aid = data['aid']
        data = self.eoms.get_weibo_s(self.tourist_uid)
        if data.get('status_code', None) != 0:
            return "获取 s 加密错误"
        self.tourist_s = data['data']['s']
        self.tourist_comment_s = data['data']['comment_s']
        return "success"

    @clothes
    def like_show(self, mid, proxies = None,**kwargs):
        params = {
            "s":      self.s,
            "source": "4215535043",
            "c":      "weicoabroad",
            "id":     mid,
            "wm":     "2468_1001",
            "gsid":   self.gsid,
            "ua":     self.ua,
            "lang":   "zh_CN",
            "count":  "100",
            "from":   "1299295010",
            "aid":    self.aid
        }
        resp = request.get("https://api.weibo.cn/2/like/show", params = params, proxies = proxies,**kwargs)
        return resp

    @clothes
    def get_likes(self, uid, page, proxies = None,**kwargs):
        params = {
            "s":           self.s,
            "source":      "4215535043",
            "c":           "weicoabroad",
            "wm":          "2468_1001",
            "gsid":        self.gsid,
            "ua":          self.ua,
            "lang":        "zh_CN",
            "count":       "20",
            "containerid": f"230869{uid}_-_mix",
            "from":        "1299295010",
            "page":        page,
            "aid":         self.aid
        }
        resp = request.get("https://api.weibo.cn/2/cardlist", params = params, proxies = proxies,**kwargs)
        return resp.json()
