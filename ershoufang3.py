#!/usr/local/python3/bin/python3
# -*- coding: UTF-8 -*-
#By yichi1
#Mail: yichi1@staff.sina.com.cn

import re
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

url = 'https://bj.lianjia.com/chengjiao/changping/pg{}p1p2p3p4/'
#url = 'https://bj.lianjia.com/chengjiao/fangshan/pg{}p1p2p3/'

class lianjia:
    def __init__(self):
        self.url = url
        self.aa = 1
        self.bb = 1
        self.title = [u'房源描述',u'成交价格']
        self.workbook = xlsxwriter.Workbook('fang.xlsx')
        self.worksheet = self.workbook.add_worksheet('fang')
        self.bold = self.workbook.add_format({'bold': True})
        self.bold.set_align('center')
        self.worksheet.set_column('A:A', 80)
        self.worksheet.set_column('B:B', 20)   
        self.worksheet.write_row('A1',self.title,self.bold)

    def _geturl(self):
        for url_next in range(1,2):
            yield url.format(url_next)

    def _getallurl(self,_geturl):
        get_url = requests.get(_geturl, 'lxml')
        if get_url.status_code == 200:
            re_set = re.compile('<li.*?<a.*?class="img.*?".*?href="(.*?)"')
            re_get = re.findall(re_set, get_url.text)
            return re_get

    def _open_url(self,re_get):
        res = requests.get(re_get)
        if res.status_code == 200:
            dcit_fang = {}
            soup = BeautifulSoup(res.text, 'lxml')
            dcit_fang['房源'] = soup.select('.house-title')[0].text
            dcit_fang['成交价'] = soup.select('.price')[0].text
            self.worksheet.write(self.aa,0,dcit_fang['房源'],self.bold)
            self.worksheet.write(self.bb,1,dcit_fang['成交价'],self.bold)
            self.aa += 1
            self.bb += 1
    def _smtp(self):
        self.my_sender='zhanganing2006@163.com'      
        self.my_pass = '2653522'
        self.my_user=['yichi1@staff.sina.com.cn','571235502@qq.com']
        msg=MIMEMultipart()
        msgtext=MIMEText('最近链家成交房源，请见附件','plain','utf-8')
        attach=MIMEApplication(open('fang.xlsx','rb').read())
        attach.add_header('Content-Disposition','attachment',filename='fang.xlsx')
        msg.attach(msgtext)
        msg.attach(attach)
        msg['From']=self.my_sender
        msg['To']=','.join(self.my_user)
        msg['Subject']="最新链家成交房源"
        server=smtplib.SMTP("smtp.163.com", 25)
        server.starttls()
        server.login(self.my_sender,self.my_pass)
        server.sendmail(self.my_sender,self.my_user,msg.as_string())
        server.quit()

    def _fang(self):
        for i in self._geturl():
            for l in [u for u in self._getallurl(i)]:
                self._open_url(l) 
        self.workbook.close()
        self._smtp()
if __name__ == '__main__':    
    lj=lianjia()
    lj._fang()
