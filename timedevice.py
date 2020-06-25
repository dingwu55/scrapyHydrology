# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 11:14
# @Author  : ding
# @File    : timedevice.py

import threading
from datetime import datetime

curTime = datetime.now().strftime("%Y-%m-%d")  # 记录当前时间
print(curTime)
execF = False
ncount = 0


def execTask():
    # 具体任务执行内容
    import begin
    import sentEmail
    begin.main()
    emailServer = sentEmail.EmailServer()
    emailServer.send_email()


def timerTask():
    global execF
    global curTime
    global ncount
    if execF is False:
        execTask()  # 判断任务是否执行过，没有执行就执行
        execF = True
    else:  # 任务执行过，判断时间是否新的一天。如果是就执行任务
        desTime = datetime.now().strftime("%Y-%m-%d")
        if desTime > curTime:
            print(desTime, curTime)
            execF = False  # 任务执行执行置值为
            curTime = desTime
    ncount = ncount + 1
    '''
    第一个参数: 延迟多长时间执行任务(单位: 秒)
    第二个参数: 要执行的任务, 即函数
    第三个参数: 调用函数的参数(tuple)
    '''
    timer = threading.Timer(5, timerTask)
    timer.start()
    print("定时器执行%d次" % (ncount))


if __name__ == '__main__':
    timer = threading.Timer(5, timerTask)
    timer.start()
