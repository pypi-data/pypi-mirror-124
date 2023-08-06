#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:00
# software: PyCharm
import requests as res

from protocol_helper.exceptions import (RequestException, WeiBoRequestIPLimit, WeiBoRequestTouristClosed)


def __upload_request(**kwargs):
    """
    Updating the customized configuration file takes effect globally
    Args:
        **kwargs:

    Returns:

    """
    if kwargs.get('timeout', None) is None:
        kwargs.setdefault('timeout', 60)

    if kwargs.get('headers', None) is None:
        kwargs.setdefault('headers', {})
    return kwargs


def put(url, data = None, json = None, **kwargs):
    """

    Args:
        url:
        data:
        json:
        **kwargs:

    Returns:

    """
    kwargs = __upload_request(**kwargs)
    resp = res.put(url, data = data, json = json, **kwargs)
    if resp.status_code != 200:
        raise RequestException(resp)
    return resp


def post(url, data = None, json = None, **kwargs):
    """

    Args:
        url:
        data:
        json:
        **kwargs:

    Returns:

    """
    kwargs = __upload_request(**kwargs)
    resp = res.post(url, data = data, json = json, **kwargs)
    if resp.status_code != 200:
        raise RequestException(resp)
    return resp


def get(url, params = None, **kwargs):
    """

    Args:
        url:
        params:
        **kwargs:

    Returns:

    """
    kwargs = __upload_request(**kwargs)
    kwargs.setdefault('allow_redirects', True)

    resp = res.get(url, params = params, **kwargs)
    if resp.status_code in [418]:
        raise WeiBoRequestIPLimit(resp)

    if resp.status_code in [403]:
        raise WeiBoRequestIPLimit(resp)

    if resp.status_code in [427]:
        raise WeiBoRequestTouristClosed(resp)

    if resp.status_code != 200:
        raise RequestException(resp)
    return resp
