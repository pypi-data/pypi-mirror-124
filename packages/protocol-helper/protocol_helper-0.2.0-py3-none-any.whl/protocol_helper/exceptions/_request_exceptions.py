#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021/9/30 10:20
# software: PyCharm

class RequestBaseException(Exception):
    TITLE = "请求错误基类"

    def __init__(self, resp, message = "请求非正常响应"):
        """

        Args:
            resp:
            message:
        """
        self.status_code = resp.status_code
        self.message = message
        self.response = resp.text
        self.resp = resp

    def __str__(self):
        return self.TITLE


class RequestException(RequestBaseException):
    TITLE = "请求常用错误基类"


class WeiBoRequestIPLimit(RequestBaseException):
    TITLE = "微博出现418IP限制"


class WeiBoRequestTouristClosed(RequestBaseException):
    TITLE = "微博出现 427 表示游客通道暂时关闭"


class WeiBoH5SideRestrictions(RequestBaseException):
    TITLE = "微博H5 无法查看数据"


class CollectedDataError(RequestBaseException):
    TITLE = "采集数据组错误"


class NotExistError(RequestBaseException):
    TITLE = "页面不存在"

