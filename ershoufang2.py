#!/usr/bin/python
# -*- coding: UTF-8 -*-
#By yichi1
#Mail: yichi1@staff.sina.com.cn

import re
import requests
from bs4 import BeautifulSoup
import os
import web

db = web.database(dbn='mysql', host='127.0.0.1', user='root', pw='my123456', db='test')
url = 'https://bj.lianjia.com/chengjiao/changping/pg1p1p2p3p4/'

class lianjia:
    #def __init__(self):
    #    self.url = url

    #def _geturl(self):
    #    for url_next in range(1,2):
    #        yield url.format(url_next)
    def _geturl(self):
        self.url = url

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
            n = db.insert('testtable',house=dcit_fang['房源'],price=dcit_fang['成交价'])
            #print dcit_fang['房源'],dcit_fang['成交价']

    def _fang(self):
        for l in [u for u in self._getallurl(url)]:
            self._open_url(l) 

if __name__ == '__main__':    
    lj=lianjia()
    lj._fang()
