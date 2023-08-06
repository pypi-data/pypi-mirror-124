#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:  Boge
# @software: pycharm
# @file: DouYinPcCollectionService.py
# @time: 2021/6/15 9:50
from protocol_helper.exceptions import DefaultException
from protocol_helper.utils import request
import re
from lxml import etree
from protocol_helper.services import eoms
from protocol_helper.setting import SURVEILLANCE_SYSTEM_TOKEN

class DouYinPcCollectionService:
    def __init__(self):
        super(DouYinPcCollectionService, self).__init__()
        self.old_header = self.HEADERS
        self.eoms = eoms()
        self._header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 2AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        }
        self._headers = {
            'Authorization': f'Token {SURVEILLANCE_SYSTEM_TOKEN}',
        }

    """直播"""
    URL_STATUS_LIVE = 'live'
    """用户"""
    URL_STATUS_USER = 'user'
    """视频"""
    URL_STATUS_VIDEO = 'video'
    """未定义"""
    URL_STATUS_ERROR = 'error'

    URL_STATUS_LABEL = {
        URL_STATUS_LIVE: '分享',
        URL_STATUS_USER: '主页分享',
        URL_STATUS_VIDEO: '视频分享',
        URL_STATUS_ERROR: '未定义'
    }
    HEADERS = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 2AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.93 Safari/537.36",
    }
    TIMEOUT = 30
    URL_TYPE_STATUS = None
    PROXY = None

    def get_user_void(self, _url, typer = None, mode = None, judge_type = None):
        """

        Args:
            _url:
            typer:
            mode:
            judge_type:

        Returns:

        """

        if typer is None:
            response = request.get(_url,proxies=self.PROXY,headers=self._header)
            url = response.url
            if url.find("404?from_url") != -1:
                return "不是主页或者是视频链接"
        else:
            url = _url
        # 如果是视频链接则走下面这个方法
        if url.find(mode) == -1 and judge_type:
            return "链接类型错误"
        if url.find("video") != -1:
            data = self.url_to_id(_url)
            if isinstance(data, str):
                return data
            return data['response']
        elif url.find("user") != -1:
            # 如果是主页链接去sec_uid
            if "sec_uid" not in url and url.find("www.douyin.com") == -1:
                return "主页链接错误"
            sec, uid = self.get_user(url, sec_uid = url)
            if isinstance(sec, str):
                return sec
            if uid is None or len(uid) == 0:
                uid = url.split("?")[0].split("/")
                if len(uid) == 0:
                    sec_uid = re.findall(r'sec_uid=(.*?)&', url)[0]
                else:
                    sec_uid = uid[0]
            else:
                sec_uid = uid
            # 走接口计算加密
            signature = self.eoms.get_dy_sign(url, uid, self._headers)
            sign = signature.json()['data'] if signature.json().get("data", "") != "" and signature.json().get("url",
                                                                                                               "") != "" else ""
            if not sign:
                raise DefaultException(f'请求加密接口错误{uid} 链接：{_url}')
            url = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={sec_uid}&count=21&max_cursor=0&aid=1128&_signature={sign}"
            response = request.get(url,proxies=self.PROXY)
            return {
                'video': response,
                'user': sec
            }
        else:
            return "不支持此类型"

    def get_user(self, url, sec_uid = None):
        try:
            if sec_uid is None:
                response = request.get(url,proxies=self.PROXY,header=self._header)
                if response.status_code == 200:
                    url_id = re.findall(r'&sec_uid=(.*?)&', response.url)[0]
                else:
                    url_id = ""
            else:
                url_id = re.findall(r'&sec_uid=(.*?)&', sec_uid)
                if len(url_id) == 0:
                    url_id = re.findall(r'\?sec_uid=(.*?)&', sec_uid)
                if len(url_id) == 0:
                    url_id = sec_uid.split("?")[0].split("/")[-1]
                if len(url_id) != 0 and isinstance(url_id, list):
                    url_id = url_id[0]
                if len(url_id) == 0:
                    return "主页链接错误"
            resp = request.get("https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={}".format(url_id))
            return resp, url_id
        except Exception as _error:
            return "转换sec错误", {'code': 107, 'msg': '取用户ID错误', 'response': str(resp.text)}

    def url_to_id(self, url):
        """

        Args:
            url:

        Returns:

        """
        resp = request.get(url,proxies=self.PROXY,headers=self._header)
        status = "error"

        if resp.url.find('/live') > -1:
            status = "live"

        if resp.url.find('/user') > -1:
            status = "user"
            return {"code": 0, "id": re.findall(r'user/(.+)\?', resp.url)[0], "type": status, "item_list": [],
                    "sec_uid": resp.url.split("sec_uid=")[-1].split("&")[0]}

        if resp.url.find('/video') > -1:
            status = "video"
            # if "视频找不到了，看看其他精彩作品吧！" in resp.text:
            #     status = URL_STATUS_VIDEO_DEL
        if resp.url.find('webcast') > -1:
            status = "webcast"

        id_ = re.findall(r'/(\d+)', resp.url)[0]
        info = request.get(f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={id_}',headers=self._header)
        if info.json().get("item_list", None) in [[], None]:
            data = self.get_dy_pc_data(
                    url = f"/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={id_}&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F91.0.4472.124+Safari%2F537.36&browser_online=true")
            print(data.text)
            if not data.json()['status_code'] in ['0', 0]:
                return "视频链接错误"
            else:
                info = data
                item_list = data.json()['aweme_detail']
        else:
            item_list = info.json()["item_list"]
        return {"code": 0, "id": id_, "type": status, "user": item_list, 'response': info}

    def judge_url_type(self, url, flag = None):
        if url.find("www.iesdouyin.com") != -1 or url.find("www.douyin.com") != -1:
            return True
        return None

    def get_dy_user(self, url, flag = False):
        """

        :param url: 主页链接
        :param flag: 如果只视频链接只获取视频链接信息，则传入Ture，否则就会去获取。
        :return: 返回response对象
        """
        typer = self.judge_url_type(url)
        self.HEADERS = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 2AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36",
        }
        try:
            return self.get_user_void(url, typer, self.URL_STATUS_USER, flag)
        except Exception as _error:
            raise Exception(f"未知错误，信息：{_error}")

    def get_dy_video(self, url, flag = False):
        """
        获取视频链信息方法
        :param url: 视频链接
        :param flag: 如果只视频链接只获取视频链接信息，则传入Ture，否则就会去获取。
        :return:返回response对象
        """
        typer = self.judge_url_type(url)
        try:
            return self.get_user_void(url, typer, self.URL_STATUS_VIDEO, flag)
        except Exception as _error:
            raise Exception(f"未知错误，信息：{_error}")

    def get_url_type(self, url):
        data = self.url_to_id(url)
        if isinstance(data, dict):
            return data['type']
        else:
            return data

    def request_processing(self, url):
        """
        判断是否为作品链接
        :param url: 作品链接
        :return:
        """
        type = url.split('/')[3]
        if type == "video" or type == 'user':
            response = request.get(url,proxies=self.PROXY,headers=self._header)
            return {'data': response.text, 'type': type}
        else:
            return '非作品链接或主页链接'

    def conversion_unit(self, interim_list):
        """
        转化单位
        :param interim_list: 需要转化单位的列表
        :return: 返回转化后的列表
        """
        storage_list = []  # 存储 storage
        for num in interim_list:
            if num[-1] == 'w':
                num = round(float(num[:-1]), 1) * 10000  # 转换一下单位3w=30000
                storage_list.append(num)
            else:
                storage_list.append(int(num))
        return storage_list

    def collect_work_information(self, url):
        """
        采集作品信息
        :param url: 作品链接
        :return:
        """
        interim_list = []  # 临时 interim
        response_data = self.request_processing(url)
        try:
            if response_data == '非作品链接或主页链接':
                return '非抖音作品链接或主页链接'
            if response_data['type'] == 'video':
                html_response = etree.HTML(response_data['data'])
                title = html_response.xpath('//h1[@class="_0101d0dac9513f32356fa89903cf7f4e-scss"]//text()')[0]  # 视频标题
                release_date = \
                    html_response.xpath('//div[@class="_3f5a4457e19c10aae6f40f4448fd9cb6-scss"]/span/text()')[
                        0]  # 发布时间
                name = html_response.xpath('//div[@class="_976c31c5a089c1b1b6d8809f82aa9a7a-scss"]/a//span/text()')[
                    0]  # 作者名称
                interim_list.append(
                        html_response.xpath('//div[@class="_976c31c5a089c1b1b6d8809f82aa9a7a-scss"]/p//span/text()')[
                            1])  # 粉丝
                interim_list.append(
                        html_response.xpath('//div[@class="_976c31c5a089c1b1b6d8809f82aa9a7a-scss"]/p//span/text()')[
                            3])  # 总获赞
                interim_list.append(
                        html_response.xpath('//span[@class="_63f39b0bbf80afa98948f5dc199307f7-scss"]/text()')[
                            0])  # 视频点赞喜欢数
                interim_list.append(
                        html_response.xpath('//span[@class="_63f39b0bbf80afa98948f5dc199307f7-scss"]/text()')[
                            1])  # 视频评论数
                storage_list = self.conversion_unit(interim_list)

                data = {
                    'nickname': name,
                    'fans': storage_list[0],  # 粉丝
                    'great': storage_list[1],  # 所有作品获赞数
                    'title': title,
                    'like_num': storage_list[2],  # 视频点赞喜欢数
                    'comment_num': storage_list[3],  # 视频评论数
                    'date': release_date,
                }
                return data
            return '不是作品链接'

        except Exception as _error:
            return f"未知错误，信息：{_error}"

    def collect_homepage_information(self, url):
        """
        采集主页信息
        :param url: 主页链接
        :return:
        """
        response_data = self.request_processing(url)
        try:
            if response_data == '非作品链接或主页链接':
                return '非抖音作品链接或主页链接'
            if response_data['type'] == 'user':
                user_data = self.get_dy_user(url)['user'].json()
                data = user_data['user_info']

                return data
            return '不是主页链接'

        except Exception as _error:
            return f"未知错误，信息：{_error}"

    def get_dy_cookie(self):
        headers = {
            'authority': 'www.douyin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        response = request.get('https://www.douyin.com/', headers = headers)
        set_cookie = response.headers['Set-Cookie']
        ttwid = re.findall(r'ttwid=(.*?);', set_cookie)[0]
        return f"ttwid={ttwid};"

    def get_dy_pc_data(self, url, update_cookie = False):
        self.HEADERS = self.old_header
        url = self.eoms.get_dy_pc_sign(url).json()['data']
        headers = {
            'authority': 'www.douyin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': 'application/json, text/plain, */*',
            'withcredentials': 'true',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
                          'Chrome/17.0.963.56 Safari/535.11',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.douyin.com/user/MS4wLjABAAAAzVHVkE2JKdrH6RJ3UdCNuvIiQ5MuYPv743M00nALqtU'
                       '?extra_params=%7B%22search_id%22%3A%22202107141010580102111730885C3FE97B%22%2C'
                       '%22search_result_id%22%3A%2261010172016%22%2C%22search_keyword%22%3A%2217703813%22%2C'
                       '%22search_type%22%3A%22video%22%7D&enter_method=search_result&enter_from=search_result',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': ''
        }
        self.HEADERS = headers
        if headers['cookie'] == "" or update_cookie:
            headers['cookie'] = self.get_dy_cookie()
        url = url if str(url).startswith("http") else "https://www.douyin.com" + url
        return request.get(url, headers = headers)
