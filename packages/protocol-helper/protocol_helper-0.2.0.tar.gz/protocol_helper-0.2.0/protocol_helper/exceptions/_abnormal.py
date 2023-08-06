#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021/9/30 10:19
# software: PyCharm


class BaseExceptions(Exception):
    MESSAGE = "Error base class"


class NotSetDirectory(BaseExceptions):
    MESSAGE = "未设置项目目录"


class DefaultException(BaseExceptions):
    MESSAGE = "默认异常,用于不重要的异常"


class RequestTimeout(BaseExceptions):
    TITLE = "请求超时"


class NeedToLogin(BaseExceptions):
    TITLE = "需要登录才可查看"


class WeiBoUrlError(BaseExceptions):
    TITLE = "微博地址异常"


class URLErrorAbnormal(BaseExceptions):
    TITLE = "账号链接异常"


class NotTakeOverException(BaseExceptions):
    TITLE = "未接管的异常"
