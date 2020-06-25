# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from hydroSearch.config import get_config
from datetime import datetime
import sentEmail
import os
import time


config = get_config()

HOSTNAME = config["HOSTNAME"]
PORT = config["PORT"]
DATABASE = config["DATABASE"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]


class HydrosearchPipeline(object):
    def __init__(self):
        self.DB_URI = create_engine("mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
                               format(username=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE))
        self.DB_Session = sessionmaker(bind=self.DB_URI)
        self.session = self.DB_Session()

        # self.csv_data = pd.read_csv(r'data\ST_STBPRP_B.csv', header=1, encoding='ANSI')
        self.f = open(r'info.txt', 'w')

    def process_item(self, item, spider):

        try:
            data = item['result']['data']
            name_data = item['name']
            data_pd = pd.DataFrame(data)
            data_pd['CREATE_TIME'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(type(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            if name_data == 'Rsvr':  # 769
                #   damel	dateTime	inq	poiAddv	poiBsnm	 rvnm	rz	stcd	stnm	tm	webStlc	wl
                # 664	2020/6/3 8:00	2	新疆维吾尔自治区	内陆河湖    	克兰河   	659.14	100110	阿苇滩水库  2020/6/3 8:00
                # 新-兵团阿勒泰阿苇滩乡  	44  CREATE_TIME
                table_name = 'st_rsvr_r'
                zd = "STNM, STCD, W, INQ, RZ, TM, CREATE_TIME "
                input_index = [8, 7, 11, 2, 6, 9, -1]
                col = data_pd.columns
                self.w_sql(table_name, data_pd, zd, input_index)
                lendata = len(data_pd)
                self.f.write(str(lendata))
                return item

            elif name_data == 'River':  # 1352
                #     dateTime	poiAddv	poiBsnm	ql	rvnm	stcd	stnm	tm	webStlc	wrz	zl
                # 2020/6/4 14:00 黑龙江省 松花江 0	松花江 10701210	哈尔滨 2020/6/4 14:00	黑—哈尔滨市道里区河干街 118.1 116.3

                table_name = 'st_river_r'
                zd = "STCD, STNM, Q, Z, TM, CREATE_TIME "
                input_index = [5, 6, 3, 10, 7, -1]
                self.w_sql(table_name, data_pd, zd, input_index)
                lendata = len(data_pd)
                self.f.write("\n"+str(lendata))
                return item

            elif name_data == 'HydroInfo':  # 581
                #  dateTime	dyp	lat	lgt	poiAddv	poiBsnm	rvnm	stcd	stnm	tm	webStlc	wth
                # 2020/6/4	0	0	0	吉林省	第二松花江 汤河 10804800	松树镇 2020/6/4 14:00	吉-江源 9

                table_name = 'st_pptn_r'
                zd = "STNM, STCD, WTH, DYP, TM, CREATE_TIME "
                input_index = [8, 7, 11, 1, 9, -1]
                self.w_sql(table_name, data_pd, zd, input_index)
                lendata = len(data_pd)
                self.f.write("\n"+str(lendata))
                curTime = datetime.now().strftime("%Y-%m-%d")
                self.f.write("\n"+str(curTime))
                self.f.close()
                print("执行完成")
                self.session.commit()
                emailServer = sentEmail.EmailServer()
                emailServer.send_email()
                time.sleep(3)
                os.remove('info.txt')
                return item

        except Exception as e:
            self.f.write("\n" + "%s" % str(e))
            self.f.write(("\n" + 'have an error')*100)
            self.f.close()
            self.session.rollback()
            emailServer = sentEmail.EmailServer()
            emailServer.send_email()
            time.sleep(3)
            os.remove('info.txt')

    def w_sql(self, table_name, data, zd, input_index):
        for index, i in enumerate(data.values):
            va = ""
            for j in input_index:
                temp_val = i[j]
                if type(temp_val) != str:
                    temp_val = str(i[j])
                va += "'" + temp_val.rstrip() + "'" + ", "
            va = va[:-2]
            sql = r"""INSERT INTO %s (%s) VALUES (%s) """ % (table_name, zd[:-1], va)
            dele_sql = r"""DELETE FROM %s WHERE STCD = '%s' AND TM = '%s' """ % \
                       (table_name, data.loc[index, 'stcd'], data.loc[index, 'tm'])
            self.session.execute(dele_sql)
            self.session.execute(sql)
