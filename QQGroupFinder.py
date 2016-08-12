#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
    查找QQ群信息
    暂未完成用户认证部分，因此需要以下信息
    暂时未完成用户认证部分，因此目前需要
    1. 自己的QQ号
        qq
    2. skey值
        手动登录QQ空间等，查看网络记录的cookie即可获得
    3. bkn
        意义未知，可以先登录QQ空间，保证cookie中有值，再进入http://find.qq.com进行一次用户查询，查看HTTP的数据段即可获得
    4. 所要查询的QQ群号
        gc
'''

import urllib
import urllib2
import json
import QQFinderConfig

class QQGroupFinder:
    '''
        查找QQ群类
    '''
    url = 'http://qun.qq.com/cgi-bin/qun_mgr/search_group_members';
    def __init__(self, qq, skey, bkn, gc=0):
        self.headers = {
            'Host': 'qun.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://qun.qq.com/member.html',
            'Cookie': 'uin=o0%d; skey=%s;' % (qq, skey),
        }

        self.post_data = {
            'gc': gc,
            'st': -1,
            'end': -1,
            'sort': 0,
            'bkn': bkn
        }


# TODO 自由定制选项

    def setGc(self, gc = 0):
        self.post_data['gc'] = gc

    # def setSkey(self, skey = ''):
    #     self.headers['Cookie'] = 'skey=%s;'%(skey)

    def setUserAgent(self, ua):
        self.headers['User-Agent'] = ua

    def fetchInfo(self):
        # TODO 异常判断
        post_data = urllib.urlencode(self.post_data)
        request = urllib2.Request(QQGroupFinder.url, post_data, self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    def getQQGroup(self, fmt='dict'):
        # TODO 异常判断
        self.post_data['st'] = -1;
        self.post_data['end'] = -1;
        qq_group_json = self.fetchInfo()
        qq_group_dict = json.loads(qq_group_json)
        if fmt == 'dict':
            return qq_group_dict
        elif fmt == 'json':
            return qq_group_json
        # TODO QQGroup解析
        elif fmt == 'xml':
            return ''
        elif fmt == 'qqgroup':
            return ''

    def getQQGroupMember(self, fmt='dict'):
        qq_group = self.getQQGroup('dict')
        self.post_data['st'] = 0;
        self.post_data['end'] = int(qq_group['count']) - 1
        qq_group_json = self.fetchInfo()
        qq_group_dict = json.loads(qq_group_json)
        qq_group_member_dict = qq_group_dict['mems']
        if fmt == 'dict':
            return qq_group_member_dict
        elif fmt == 'json':
            return json.dumps(qq_group_member_dict)
        # TODO QQGroupMember解析
        elif fmt == 'xml':
            return ''
        elif fmt == 'qqgroup':
            return ''

def test():
    qqGroup = QQGroupFinder(qq=QQFinderConfig.QQ, skey=QQFinderConfig.SKEY, bkn=QQFinderConfig.BKN, gc=497394781)
    print qqGroup.getQQGroupMember('json')
    qqGroup.setGc( 545142869)
    print qqGroup.getQQGroupMember('json')


if __name__ == '__main__':
    test()