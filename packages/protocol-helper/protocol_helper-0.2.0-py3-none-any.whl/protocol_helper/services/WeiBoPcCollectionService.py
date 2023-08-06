#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 17:42
# software: PyCharm
import json
import random
from abc import ABC
from bs4 import BeautifulSoup
from protocol_helper.exceptions import *
from protocol_helper.services import WeiBoBaseService
from protocol_helper.utils import request
import requests
import re

def helper(function):
    def clothes(func):
        def wear(*args, **kwargs):
            cls = args[0]
            if function == 'login_guest':
                if cls._headers.get('Cookie', None) is None:
                    cls.get_cookies_tourist()
            return func(*args, **kwargs)

        return wear

    return clothes


class WeiBoPcCollectionService(WeiBoBaseService, ABC):
    HEADERS = {
        'x-requested-with': 'XMLHttpRequest',
        'user-agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/90.0.4430.72 Safari/537.36 ',
        'accept':           'application/json, text/plain, */*',
    }

    def __init__(self):
        super(WeiBoPcCollectionService, self).__init__()

        # pc 游客权限使用
        self._headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.72 Safari/537.36 ',
        }
        self.requests = requests.Session()
        self.TIMEOUT = 10
        
    def get_topic(self, title, proxies = None,**kwargs):
        """
        微博话题
        支持格式 #吴一凡# 吴一凡

        Returns:

        """
        params = {"containerid": f"100103type=1&q={title}&t=0", "page": "1", "count": "20"}
        return request.get('https://weibo.com/ajax/search/all', params = params, proxies = proxies,**kwargs).json()

    def get_article(self, mid, proxies = None,**kwargs):
        """
        微博博文
        Args:
            mid: 微博文章mid

        Returns:

        """
        params = {'id': mid}
        return request.get('https://weibo.com/ajax/statuses/show', params = params, proxies = proxies,**kwargs).json()

    def get_fans(self, uid = None, custom = None, proxies = None,**kwargs):
        """
        微博主页

        uid 与  custom 不能同时为空

        Args:
            uid:   uid
            custom:custom

        Returns:

        """
        params = {}
        if uid is not None:
            params.update({'uid': uid})
        if custom is not None:
            params.update({'custom': custom})
        return request.get('https://weibo.com/ajax/profile/info', params = params, proxies = proxies,**kwargs).json()

    def get_user_article(self, uid, page = 1, proxies = None,**kwargs):
        """
        获取用户博文
        :param uid:     微博uid
        :param page:   获取页数
        :return:
        """
        params = {}
        if uid is not None:
            params.update({'uid': uid})
        if page is not None:
            params.update({'page': page})
        return request.get(f"https://weibo.com/ajax/statuses/mymblog", params = params, proxies = proxies,**kwargs).json()

    def get_tid_tourist(self, proxies = None,**kwargs):
        """
        获取访客信息
        Returns:

        """
        tid_url = "https://passport.weibo.com/visitor/genvisitor"
        data = {
            "cb": "gen_callback",
            "fp": {
                "os":         "3",
                "browser":    "Chrome69,0,3497,100",
                "fonts":      "undefined",
                "screenInfo": "1920*1080*24",
                "plugins":    "Portable Document Format::internal-pdf-viewer::Chrome PDF "
                              "Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF "
                              "Viewer|::internal-nacl-plugin::Native Client "
            }
        }
        resp = self.requests.post(url = tid_url, data = data, headers = self._headers, timeout = self.TIMEOUT,
                                  proxies = proxies,**kwargs)

        if resp.status_code != 200:
            raise RequestException(resp)
        content = re.findall(r'&& gen_callback\((.*?)\);', resp.text)
        if len(content) <= 0:
            return DefaultException("获取注册访客信息失败")
        data = json.loads(content[0])
        return data.get('data').get('tid')

    def get_cookies_tourist(self, proxies = None,**kwargs):
        """
        获取游客注册信息
        Returns:

        """
        tid = self.get_tid_tourist()

        cookies = {
            "tid": tid + "__095"
        }
        url = "https://passport.weibo.com/visitor/visitor"

        params = {
            "a":     "incarnate",
            "t":     tid,
            "w":     "2",
            "c":     "095",
            "gc":    "",
            "cb":    "cross_domain",
            "from":  "weibo",
            "_rand": f"0.{random.random()}"
        }
        resp = self.requests.get(url, params = params, cookies = cookies, headers = self._headers,
                                 timeout = self.TIMEOUT, proxies = proxies,**kwargs)
        if resp.status_code != 200:
            return None

        content = re.findall(r'&& cross_domain\((.*?)\);', resp.text)
        if len(content) <= 0:
            return DefaultException("注册访客信息失败")
        data = json.loads(content[0])
        if data.get('retcode', None) != 20000000:
            raise DefaultException(data.get('msg', resp.text))

        cookies = 'SUB={};SUBP={}'.format(data['data']['sub'], data['data']['subp'])
        self._headers.update({'Cookie': cookies})
        print("注册游客cookies 成功", cookies)

    @helper("login_guest")
    def get_fans_tourist(self, url, proxies = None, **kwargs):
        """
        游客权限获取用户信息
        Args:
            proxies:
            url:

        Returns:

        """
        if url.find('m.weibo.com') != -1:
            url = url.replace('m.weibo.com', 'weibo.com')

        if url.find('m.weibo.cn') != -1:
            url = url.replace('m.weibo.cn', 'weibo.com')
        if url.find('/profile') != -1:
            url = url.replace('/profile', '')
        if url.find('/follow') != -1:
            url = url[:url.find('/follow')]

        if not str(url).startswith('https'):
            uid = re.findall("^\d{6,15}$", url)[0]
            url = f'https://weibo.com/u/{uid}'

        resp = self.requests.get(url, headers = self._headers, proxies = proxies, **kwargs)
        if resp.status_code != 200:
            raise RequestException(resp)
        # 起始位置
        _bs4 = BeautifulSoup(resp.content, 'lxml')
        if _bs4.text.find('出错情况返回登录页') > 0:
            raise DefaultException('Cookies可能错误')

        if _bs4.text.find('该页面不存在') > 0:
            raise DefaultException('该页面不存在')

        user_array = re.findall(r"CONFIG\['(onick|oid)'\]='(.*?)';", resp.text)

        if user_array in [None] or len(user_array) != 2:
            raise DefaultException('获取UID失败')
        statuses_count = re.findall(r'<strong class=\\"W_f[\d]+\\">(\d+)<\\/strong><span class=\\"S_txt2\\">微博<',
                                    resp.text)
        friends_count = re.findall(r'<strong class=\\"W_f[\d]+\\">(\d+)<\\/strong><span class=\\"S_txt2\\">关注<',
                                   resp.text)
        followers_count = re.findall(r'<strong class=\\"W_f[\d]+\\">(\d+)<\\/strong><span class=\\"S_txt2\\">粉丝<',
                                     resp.text) or re.findall(r'[他|她]的粉丝\((\d+)\)', resp.text)
        if not all([statuses_count, friends_count, followers_count]):
            raise DefaultException(f'匹配数量失败', str(user_array[0][1]))

        if user_array[0][1].isdigit() not in [True]:
            raise DefaultException('识别错误')
        response = re.sub(r'(\s|\\r\\n|\\t|\\)', '', resp.text)
        verified_array = re.findall(r'<emtitle="(.*?)"class="(\w+)".*username', response)
        avatar = re.findall(r'photo_wrap"><imgsrc="(.*?)"', response)
        if len(avatar) > 0:
            avatar = avatar[0]
        else:
            avatar = 'null'
        if verified_array:
            verified_data = {
                'W_icon_co2icon_pf_approve_co': '蓝V', 'W_iconicon_pf_approve_co': '蓝V',
                'W_iconicon_pf_approve_gold':   '金V', 'W_iconicon_pf_approve': '黄V'
            }
            verified_title = verified_array[0][0]
            verified_type = verified_data.get(verified_array[0][1], '未知')
        else:
            verified_type, verified_title = None, None

        content = re.findall(r'pf_intro"title="(.*?)"', response)
        if len(content) > 0:
            content = content[0]
        else:
            content = '暂无简介'
        user = {
            'uid':             str(user_array[0][1]),
            'nick_name':       user_array[1][1],
            'name':            user_array[1][1],
            'followers_count': followers_count[0],
            'friends_count':   friends_count[0],
            'statuses_count':  statuses_count[0],
            'verified_title':  verified_title,
            'verified_type':   verified_type,
            'avatar':          avatar,
            'content':         content
        }

        return user

    @helper("login_guest")
    def get_article_tourist(self, url, proxies = None,**kwargs):
        """
        pc 游客状态访问 获取博文数据
        Args:
            proxies:
            url:

        Returns:

        """
        # PC 识别 正则提取麻烦使用 h5端获取数据
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'accept':     'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,'
                          'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie':     self._headers.get('Cookie', '')
        }

        resp = self.requests.get(url, headers = headers, timeout = self.TIMEOUT, proxies = proxies,**kwargs)

        if resp.text.find('update-desc-r">打开微博客户端，查看全文</p>') >= 0:
            raise WeiBoH5SideRestrictions(resp, "打开微博客户端，查看全文")

        if resp.text.find('微博不存在或暂无查看权限!') >= 0:
            raise WeiBoUrlError(resp, "微博不存在或暂无查看权限")

        mid = re.findall(r'"mid": "(.*?)"', resp.text)
        if len(mid) > 2 or len(mid) <= 0:
            raise DefaultException("数据格式错误")

        # 通过 h5获取数据
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept':           'application/json',
            'Cookie':           self._headers.get('Cookie', ''),
        }
        # Mid 需要是英文的 不是 18位数字需要转换
        mid = self.id2mid(mid[0])
        resp = self.requests.get(f'https://m.weibo.cn/statuses/show?id={mid}', headers = headers,
                                 timeout = self.TIMEOUT, proxies = proxies)

        if resp.status_code != 200:
            raise RequestException(resp)

        return json.loads(resp.text)

    @helper("login_guest")
    def get_likes_tourist(self, url, proxies = None,**kwargs):
        """

        Args:
            url:
            proxies:

        Returns:

        """
        headers = {
            'Cookie': self._headers.get('Cookie', '')
        }
        _res = self.requests.get(url, headers = headers, timeout = self.TIMEOUT, proxies = proxies,**kwargs)
        if _res.status_code != 200:
            return '访问code错误：{0}'.format(_res.status_code)

        if _res.text.find('博文涉及营销推广正在审核中，暂时无法传播') >= 0:
            return '博文涉及营销推广正在审核中，暂时无法传播'
        if _res.text.find('由于用户设置，你无法回复评论。') >= 0:
            return '由于用户设置，你无法回复评论。'
        if _res.text.find('以下为博主精选评论') >= 0:
            return '以下为博主精选评论'

        return _res.text

    @staticmethod
    def _unit_conversion(unit) -> int:
        """
        单位转换
        Args:
            unit:

        Returns:

        """
        if unit == '万':
            return 10000

        if unit == "亿":
            return 100000000

        return 1

    @helper("login_guest")
    def get_super_tourist(self, url, proxies = None,**kwargs):
        """

        Args:
            proxies:
            url:

        Returns:

        """
        resp = self.requests.get(url, headers = self._headers, timeout = self.TIMEOUT, proxies = proxies,**kwargs)
        if resp.status_code != 200:
            raise RequestException(resp)
        # 起始位置
        page_id = re.findall(r"\$CONFIG\['page_id'\]='(.*?)'", resp.text)
        nick_name = re.findall(r"\$CONFIG\['onick'\]='(.*?)'", resp.text)
        title_value = re.findall(r"\$CONFIG\['title_value'\]='(.*?)'", resp.text)
        counts = re.findall(r'<strong class=.*?>(.*?)<', resp.text)
        if len(counts) <= 0:
            raise DefaultException('匹配数量失败')
        # 阅读数
        if not counts[0].isdigit():
            read_count = float(counts[0].replace(counts[0][-1], ''))
        else:
            read_count = float(counts[0])
        # 文章数量
        if not counts[1].isdigit():
            article_count = float(counts[1].replace(counts[1][-1], ''))
        else:
            article_count = float(counts[1])
        # 粉丝数量
        if not counts[2].isdigit():
            fans_count = float(counts[2].replace(counts[2][-1], ''))
        else:
            fans_count = float(counts[2])
        return {
            'page_id':       page_id[0],
            'nick_name':     nick_name[0],
            'title_value':   title_value[0],
            'read_count':    int(read_count * self._unit_conversion(counts[0][-1])),
            'article_count': int(article_count * self._unit_conversion(counts[1][-1])),
            'fans_count':    int(fans_count * self._unit_conversion(counts[2][-1]))
        }

    @helper("login_guest")
    def get_user_container_tourist(self, container_id, proxies = None,**kwargs):
        """
        https://weibo.com/p/1005053841735409/home
        获取wb p格式用户信息
        :param container_id:
        :return:

        Args:
            proxies:
        """
        params = {
            "containerid": container_id
        }
        return request.get(f"https://m.weibo.cn/api/container/getIndex", params = params, proxies = proxies,**kwargs)

    def get_voting_information(self, url, cookie, proxies = None,**kwargs):
        from lxml import etree
        import json
        """
        获取微博投票信息
        Args:
            url:

        Returns:

        """
        _headers = {
            'authority':       'vote.weibo.com',
            'accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                               '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Cookie':          cookie
        }
        if 'vote.weibo.com' not in url:
            return '链接错误'
        if 'vote_id' not in url:
            return '缺少vote_id'
        reps = request.get(url, headers = _headers, proxies = proxies,**kwargs).text
        html = etree.HTML(reps)
        text = html.xpath('//script/text()')[0]
        json_text = str(text).replace('window.__DATA__ = ', '').replace(" || '';", '')
        resp_json = json.loads(json_text)
        if '当前页面内容不可见' in json_text:
            return resp_json
        info = resp_json['vote_info']
        name = info['launch_userinfo']['name']
        voting_title = info['title']
        deadline = info['end_time_str']
        show_str = info['show_str']
        participation = info['part_num']
        voting_options = info['option_list']
        if '投票已结束' in show_str:
            is_expire = True
        else:
            is_expire = False
        data = {
            'user':         name,
            'voting_title': voting_title,
            'part_num':     participation,
            'deadline':     deadline,
            'voting_list':  voting_options,
            'vote_info':    resp_json,
            'is_expire':    is_expire
        }
        return data

    @helper("login_guest")
    def get_weibolong_read(self, url, proxies = None,**kwargs):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.87 Safari/537.36 '
            }
            id_list = re.findall('\d{22}', url)
            if len(id_list) == 0:
                return {'code': 107, 'msg': '未正确获取到微博博文ID'}
            artilce_id = id_list[0]
            request_url = f'https://weibo.com/ttarticle/x/m/aj/extend?id={artilce_id}'
            header.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.87 Safari/537.36',
                'Referer':    request_url,

            })
            info = requests.get(request_url, headers = header, verify = False, proxies = proxies,**kwargs).json()
            if str(info.get("code")) == '100000':
                data = info['data']
                mid = data['mid']
                uid = data['uid']
                name = data['userinfo']['screen_name']
                title = data['title']
                content = data['content']
                data = {
                    'code':          0,
                    'mid':           mid,
                    'uid':           uid,
                    'nickname':      name,
                    'content':       content,
                    'content_title': title,
                    'info':          data
                }
            elif info.get("code") == "100098":
                # 抱歉，你需要登录微博后才可以查看文本内容
                data = {
                    'code':   0,
                    'source': info.get('msg'),
                    'mid':    artilce_id,
                    'uid':    artilce_id
                }
            else:
                # 其他错误代码返回原始数据
                data = {
                    'code':   0,
                    'source': info.get('msg'),
                    'mid':    artilce_id,
                    'uid':    artilce_id
                }
            return data
        except Exception as e:
            return {'code': 107, 'msg': f'获取失败，原因{e}'}

    def get_comments(self, mid, uid, cookie, flow = 1, max_id = 0, proxies = None,**kwargs):
        """

        Args:
            mid:
            uid:
            flow:
            max_id:
            proxies:

        Returns:

        """
        headers = {
            'accept':           'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/92.0.4515.159 Safari/537.36',
            'Cookie':           cookie
        }
        params = (
            ('flow', str(flow)),
            ('is_reload', '1'),
            ('id', str(mid)),
            ('is_show_bulletin', '2'),
            ('is_mix', '0'),
            ('max_id', str(max_id)),
            ('count', '20'),
            ('uid', str(uid)),
        )
        return request.get("https://weibo.com/ajax/statuses/buildComments", headers = headers, params = params,
                           proxies = proxies,**kwargs).json()

    def set_cookies(self,cookie):
        self._headers['Cookie'] = cookie

    def get_user_uid(self, url, cookie, proxies = None,**kwargs):
        custom = url.split("/")
        custom = [x for x in custom if len(re.findall('\d+', x)) != 0 if str(re.findall(r'\d+', x)[0]) == x]
        custom = custom[0] if len(custom) == 1 else ""
        if not custom:
            raise DefaultException(f"获取用户信息错误 {url}")
        headers = {
            'authority':        'weibo.com',
            'pragma':           'no-cache',
            'cache-control':    'no-cache',
            'sec-ch-ua':        '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'accept':           'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/92.0.4515.159 Safari/537.36',
            'Cookie':           cookie
        }
        params = (
            ('custom', custom),
        )
        data = request.get('https://weibo.com/ajax/profile/info', headers = headers, params = params,
                           proxies = proxies,**kwargs).json()
        data = data['data']
        user = data['user']
        uid = user['id']
        return {
            'data': data,
            'user': user,
            'uid':  uid
        }
