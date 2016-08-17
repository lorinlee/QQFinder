# -*- coding: UTF-8 -*-

'''
    查找QQ用户信息
    暂时未完成用户认证部分，因此目前需要
    1. 自己的QQ号
        qq
    2. skey值
        手动登录QQ空间等，查看网络记录的cookie即可获得
    3. ldw
        意义未知，可以先登录QQ空间，保证cookie中有值，再进入http://find.qq.com进行一次用户查询，查看HTTP的数据段即可获得
    4. 所要查询的用户QQ号
        keyword
'''

import urllib
import urllib2
import json
import QQFinderConfig

class QQUserFinder():
    '''
        查找用户QQ用户类
    '''
    url = 'http://cgi.find.qq.com/qqfind/buddy/search_v3'

    def __init__(self, qq, skey, ldw, keyword = 0):
        self.headers = {
            'Host': 'cgi.find.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://find.qq.com/',
            'origin': 'http://find.qq.com',
            'Cookie': 'uin=o0%d; skey=%s;'%(qq, skey)
        }
        self.post_data = {
            'num': 20,
            'page': 0,
            'sessionid': 0,
            'keyword': keyword,
            'agerg': 0,
            'sex': 0,
            'firston': 1,
            'video': 0,
            'country': 1,
            'province': 61,
            'city': 1,
            'district': 0,
            'hcountry': 1,
            'hprovince': 0,
            'hcity': 0,
            'hdistrict': 0,
            'online': 1,
            'ldw': ldw
        }

    # def setLdw(self, ldw = 0):
    #     self.post_data['ldw'] = ldw

    # TODO 自由定制选项

    def setKeyword(self, keyword = 0):
        self.post_data['keyword'] = keyword

    # def setSkey(self, skey = ''):
    #     self.headers['Cookie'] = 'skey=%s;'%(skey)

    def setUserAgent(self, ua):
        self.headers['User-Agent'] = ua

    def fetchInfo(self):
        # TODO 异常判断
        post_data = urllib.urlencode(self.post_data)
        request = urllib2.Request(QQUserFinder.url, post_data, self.headers)
        ret = None
        try:
            response = urllib2.urlopen(request)
            ret = response.read()
        except Exception, e:
            print '[Error] Query: %d, ErrorMsg: %d %s' % (self.post_data['keyword'], e.args[0], e.args[1])
        finally:
            return ret

    def getUser(self, fmt='dict'):
        # TODO 异常判断
        info_json = self.fetchInfo()
        ret = None
        try:
            info = json.loads(info_json)
            user_dict = info['result']['buddy']['info_list'][0]
            user_dict['birthday_year'] = user_dict['birthday']['year']
            user_dict['birthday_month'] = user_dict['birthday']['month']
            user_dict['birthday_day'] = user_dict['birthday']['day']
            del user_dict['birthday']
            if fmt == 'dict':
                ret = user_dict
            elif fmt == 'json':
                user_json = json.dumps(user_dict)
                ret = user_json
            # TODO User解析
            elif fmt == 'xml':
                ret = ''
            elif fmt == 'user':
                ret = ''
        except Exception, e:
            print '[Error] getUser Failed, ErrorMsg: %s' % (e)
        finally:
            return ret

def test():
    myUser = QQUserFinder(qq=QQFinderConfig.QQ, skey=QQFinderConfig.SKEY, ldw=QQFinderConfig.LDW)
    myUser.setKeyword(QQFinderConfig.QQ)
    print myUser.getUser('json')


if __name__ == '__main__':
    test()
