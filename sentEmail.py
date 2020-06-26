# -*- coding: utf-8 -*-
# @Time    : 2020/6/3 17:54
# @Author  : ding
# @File    : sentEmail.py

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Msg(object):
    def __init__(self, zhuangtai, from_addr, to_addrs, data_temp):
        self.zhuangtai = zhuangtai
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.data_temp = data_temp

    def creat_msg(self):
        if self.zhuangtai == '失败':
            msg = MIMEText(str(self.data_temp), 'plain', 'utf-8')
            msg['From'] = Header(self.from_addr)
            msg['TO'] = Header(",".join(self.to_addrs))
            msg['Subject'] = Header(self.zhuangtai)
        else:
            msg = MIMEText('%s数据入库情况：河道水文站: %s，水库水文站: %s，雨量站: %s' %
                           (self.data_temp[3], self.data_temp[1], self.data_temp[0], self.data_temp[2]), 'plain', 'utf-8')
            msg['From'] = Header(self.from_addr)
            msg['TO'] = Header(",".join(self.to_addrs))
            msg['Subject'] = Header('%s数据入库情况：河道水文站: %s，水库水文站: %s，雨量站: %s' %
                           (self.data_temp[3], self.data_temp[1], self.data_temp[0], self.data_temp[2]))
        return msg


class EmailServer():
    def __init__(self):
        f = open(r'info.txt', 'r')
        self.data_temp = []
        for i in f:
           self.data_temp.append(i)
        f.close()

    @staticmethod
    def config_server():
        # Configure mailbox
        config = dict()
        config['send_email'] = '**********@qq.com'
        config['passwd'] = 'jhsvuvkeorogbbjd'

        config['smtp_server'] = 'smtp.qq.com'  # 设置服务器
        config['target_email'] = ['*********@qq.com']
        return config

    def send_email(self):
        config = self.config_server()
        if len(self.data_temp) != 4:
            # 异常
            # crawl.star()
            msg1 = Msg(zhuangtai='失败', from_addr=config['send_email'], to_addrs=config['target_email'], data_temp=self.data_temp)
            msg = msg1.creat_msg()
        else:
            msg1 = Msg(zhuangtai='成功', from_addr=config['send_email'], to_addrs=config['target_email'], data_temp=self.data_temp)
            msg = msg1.creat_msg()

        server = smtplib.SMTP_SSL(host=config['smtp_server'])
        server.connect(host=config['smtp_server'], port=465)
        server.login(user=config['send_email'], password=config['passwd'])
        server.set_debuglevel(True)

        try:
            server.sendmail(config['send_email'],
                            config['target_email'],
                            msg.as_string())
        finally:
            server.quit()


if __name__ == '__main__':
    # cmdline.execute("scrapy crawl hydro_search".split())
    emailServer = EmailServer()
    emailServer.send_email()
