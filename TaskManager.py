#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import QQFinderConfig
import os

class TaskManager:
    '''
        爬虫任务管理器
    '''

    def __init__(self):
        self.status = 0
        self.file = QQFinderConfig.TASK_FILE
        if os.path.exists(self.file):
            f = open(self.file)
            con = f.readline()
            try:
                self.status = int(con)
            except Exception, e:
                pass
            finally:
                f.close()

    def save(self):
        f = open(self.file, 'w+')
        f.write(str(self.status))
        f.close()


def test():
    taskManager = TaskManager()
    taskManager.status = 342
    taskManager.save()


if __name__ == '__main__':
    test()