#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
    查找QQ群所有人员信息
'''

import QQUserFinder
import QQGroupFinder
import QQFinderConfig
import MySQLdb
import copy
import time
import random
import TaskManager

qq_group_number = [
    497394781,
]

def update_qq_group():
    try:
        qq_group_finder = QQGroupFinder.QQGroupFinder(QQFinderConfig.QQ, QQFinderConfig.SKEY, QQFinderConfig.BKN)
        conn = MySQLdb.connect(host=QQFinderConfig.MYSQL_HOST, user=QQFinderConfig.MYSQL_USER, passwd=QQFinderConfig.MYSQL_PASSWORD, db=QQFinderConfig.MYSQL_DB, port=QQFinderConfig.MYSQL_PORT, charset='UTF8')
        cursor = conn.cursor()
        group_sql = "INSERT INTO `qq_group`(`g`, `last_speak_time`, `tags`, `lv_point`, `qage`, `uin`, `nick`, `flag`, `role`, `lv_level`, `join_time`, `card`, `group_id`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for qq_group in qq_group_number:
            qq_group_finder.setGc(qq_group)
            qq_group_member = qq_group_finder.getQQGroupMember('dict')
            cursor.execute('DELETE FROM `qq_group` WHERE `group_id` = %s', (qq_group))
            for member in qq_group_member:
                mem = member.values()
                mem.append(qq_group)
                cursor.execute(group_sql, mem)
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        exit(0)

def update_qq_user():
    try:
        qq_user_finder = QQUserFinder.QQUserFinder(QQFinderConfig.QQ, QQFinderConfig.SKEY, QQFinderConfig.LDW)
        conn = MySQLdb.connect(host=QQFinderConfig.MYSQL_HOST, user=QQFinderConfig.MYSQL_USER,
                               passwd=QQFinderConfig.MYSQL_PASSWORD, db=QQFinderConfig.MYSQL_DB,
                               port=QQFinderConfig.MYSQL_PORT, charset='UTF8')
        uin_cursor = conn.cursor()
        user_cursor = conn.cursor()
        uins_count = uin_cursor.execute('SELECT DISTINCT `uin` FROM `qq_group`')
        task = TaskManager.TaskManager()
        for i in xrange(0, uins_count):
            uin = uin_cursor.fetchone()[0]
            if i < task.status:
                continue
            print '%d: ' % (i)
            qq_user_finder.setKeyword(uin)
            qq_user = qq_user_finder.getUser('dict')
            if qq_user != None:
                try:
                    user_cursor.execute('INSERT INTO `qq_user`(`allow`, `birthday_year`, `birthday_month`, `birthday_day`, `blood`, `cft_flag`, `city`, `college`, `constel`, `country`, `email`, `extflag`, `face`, `flag`, `gender`, `gps_flag`, `h_city`, `h_country`, `h_province`, `h_zone`, `homepage`, `lnick`, `mobile`, `nick`, `occupation`, `personal`, `phone`, `province`, `reg_type`, `s_flag`, `shengxiao`, `stat`, `uin`, `url`, `zone_id`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (qq_user['allow'], qq_user['birthday_year'], qq_user['birthday_month'], qq_user['birthday_day'], qq_user['blood'], qq_user['cft_flag'], qq_user['city'], qq_user['college'], qq_user['constel'], qq_user['country'], qq_user['email'], qq_user['extflag'], qq_user['face'], qq_user['flag'], qq_user['gender'], qq_user['gps_flag'], qq_user['h_city'], qq_user['h_country'], qq_user['h_province'], qq_user['h_zone'], qq_user['homepage'], qq_user['lnick'], qq_user['mobile'], qq_user['nick'], qq_user['occupation'], qq_user['personal'], qq_user['phone'], qq_user['province'], qq_user['reg_type'], qq_user['s_flag'], qq_user['shengxiao'], qq_user['stat'], qq_user['uin'], qq_user['url'], qq_user['zone_id']))
                except Exception, e:
                    print '[Error] Insert User Data Failed, ErrorMsg: %s' % (e)
                    break
            else:
                print '[Error] Invalid User'
                print 'uin = %s' % uin
                task.status = i
                task.save()
                break
            interval = 0
            print 'interval: %d' % (interval)
            time.sleep(interval)
            if i == uins_count-1:
                task.status = i
                task.save()
        uin_cursor.close()
        user_cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error, e:
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        exit(0)


update_qq_user()