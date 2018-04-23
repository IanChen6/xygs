# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""
import base64
import hashlib
import json
import logging
import random
import time
import pymssql
import os
from suds.client import Client
import suds
import re
import execjs
import redis
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import ui
from urllib3 import Retry
from guoshui import guoshui
from get_db import get_db, job_finish
import sys
from log_ging.log_01 import create_logger
from urllib.parse import quote, urlparse, parse_qs

szxinyong = {}


class gscredit(guoshui):
    def __init__(self, user, pwd, batchid, companyid, customerid, logger,companyname):
        # self.logger = create_logger(path=os.path.basename(__file__) + str(customerid))
        self.logger = logger
        self.user = user
        self.pwd = pwd
        self.batchid = batchid
        self.companyid = companyid
        self.customerid = customerid
        self.host, self.port, self.db = get_db(companyid)
        self.companyname=companyname

    def get_js(self):
        # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
        f = open("/home/mycode/localcredit/cdata.js", 'r', encoding='UTF-8')
        # f = open("cdata.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def login(self):
        # try_times = 0
        # while try_times <= 14:
        #     self.logger.info('customerid:{},开始尝试登陆'.format(self.customerid))
        #     try_times += 1
        #     if try_times>10:
        #         time.sleep(1)
        #     session = requests.session()
        #     #设置代理
        #     proxy_list = [
        #         {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
        #         {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
        #         {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
        #         {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
        #         {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
        #         {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
        #         {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
        #         {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
        #         {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
        #         {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
        #         {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
        #         {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
        #         {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
        #         {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
        #         {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
        #     ]
        #     proxy = proxy_list[random.randint(0, 14)]
        #     session.proxies = proxy
        #     retry = Retry(connect=3, backoff_factor=1)
        #     adapter = HTTPAdapter(max_retries=retry)
        #     session.mount('http://', adapter)
        #     session.mount('https://', adapter)
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        #         'Accept': 'application/json, text/javascript, */*; q=0.01',
        #         'Accept-Encoding': 'gzip,deflate',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'Connection': 'keep-alive',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Host': 'dzswj.szgs.gov.cn',
        #         'Referer': 'http://dzswj.szgs.gov.cn / BsfwtWeb / apps / views / login / login.html',
        #         'X-Requested-With': 'XMLHttpRequest'
        #     }
        #     # proxy_list = get_all_proxie()
        #     # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
        #     # try:
        #     #     self.logger.info(type(sys.argv[1]))
        #     #     proxy = sys.argv[1].replace("'", '"')
        #     #     self.logger.info(proxy)
        #     #     proxy = json.loads(proxy)
        #     #     session.proxies = proxy
        #     # except:
        #     #     self.logger.info("未传代理参数，启用本机IP")
        #     for s in range(5):
        #         try:
        #             add = session.get(
        #                 "http://dzswj.szgs.gov.cn/api/auth/queryTxUrl?json&_={}".format(str(int(time.time() * 1000))),
        #                 headers=headers, timeout=10)
        #             break
        #         except Exception as e:
        #             self.logger.info("滑动验证码获取失败")
        #             self.logger.info(headers)
        #             time.sleep(5)
        #             self.logger.info(e)
        #             continue
        #     query = urlparse(add.json()['data']).query
        #     d = dict([(k, v[0]) for k, v in parse_qs(query).items()])
        #     sess_url = "https://captcha.guard.qcloud.com/cap_union_prehandle?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&collect=xV6XnEXCTYbfMkq3nBXtS0c%2FV5AAZtsYtOqYjNBVDwvu0DT8YIl0%2BdlKp2UjKu0nw9G%2FTRvlmFAxGhorC%2BMq4MBMdkhfEnITqxh7Bad0q7e0ffClmuKkyX15QuZqT42Ej1RCgowaxr6ltGKYPgkVX6Fx%2B9pf6brr%2FIXbyp5trWz5UYDqJQ%2B%2B%2But2YkbKEwsE7%2BazqQ7y1qM9HHGC28%2Bz0iWZ6bjExtUYlbSH1g7zqEuq1FbFd1O%2B6xFztsvzI8lPuYhqwh0zUf4%2Fitr4PxPMGPo7MwUy%2BiJzaG%2F7bPCPvGB%2F9hGrC5V6V9e0uad0iK0FDDhPn0Ge%2F8mMlN7BoJzFAXkNrG1Iax2r0YqqLCffVwuDr1pHyhpq8wySNEYl70BeaVWdeDhT5QQd9Sujkg4EeDp5AEKDKrcvEhfcXrmKVFsH35s0XsFRr67VOyfKi%2BGDuJz4xCXH66ySt2BTycTC55FdfQ0Ef5uTuNFLkPgki2x09ePD7cHJXV7T86%2FkP%2Fi9GSEXBOy31%2B%2BZuLYInfEeiZRbuNEBMwyPa1MNrIMnUun4Dk5m7qP3aaga3UV24bZEhNWE0rYX3XrKLCgcw1JyD%2BF%2B%2F%2BUwcrewMBKzWcceZULq033o9HCRVaDzWxeyUNc%2FYLoGmJBCAhKRuKI35yAcYPZvtfEb6s29jqgMRTNkxSvJfIEHvAdBFYs44%2Fkf0P%2FdwiIHol1TITJVsbmlNehuFt39dXR15aOxbd4L8rv6YxW2j3rxBkWhaZwhgFUR066icYpz6%2FYgcsYbCoSt1Vxaz%2Fu8Wm06dmvyElvOFW2gdQbQYez1ju5x%2FfPFRZR%2B%2FCgOGa7nu8iMQHabdKlwoCRFN5ZHmqRcs01mA4iFQg6MB10aI%2FeuwB4JmHufAT1l5gCWfs1HqJBMRt5flx9KOY0uRi7usyloLQXzXnnCkK%2BRx78gP5n7Ex0ciAVivXjqaxpQKpmgv94IplHxliSNfglULAYvzpr9kSS5saFYSNjP7w0HCyrbRbl6%2B2STCU1MKzRS8UxJ2anCrkyC4vfUeXZY6CIoGVsW9BloXO%2BD7ZSLBgZkPscWv%2FOt8TFywebfHm7YtMfjvCaWCnkT5MtkVrbTUp3vaycuMKB7z%2Fen7yfTP2vkEfmPWxQQtNDKjIKEGtno0EA0SSihw6pfk1hZHD%2BeOji0oQ4IHr2EjvXtibIvKLIOCLRMrMAlSxl%2Fy48utVt4LJa6%2BBLZhNzkuvbgoJL9ss1NZdIt7GIEOhY3HV%2FVnRbMv8zs7pKKqx5Mx%2BjQ61yCjmFHO6ldQrNuKb%2BMYKAennyD9XXd4hFguk13iFcb8luOyJvwg4%2BobY3X5lY975qsxK%2BYZfEwqNE7EatDGCqHCJnM23GdfMKq4ibSTMQe%2FOLziUHKZtI3x%2FvroZ4Fue0ygY5Lmt0cZCK7ik2Xu5U6jcxh1aegAFFzZh18aQPVyGL1Z%2B4Ugg4A0WDgkk0T%2Fzy6FRo8TWf0b%2BbN8Y6HEzty2HaRtU6y2SfifxTmo81uwqAV4GXhzwwNr2zJWoAFnL8pV1119CSXEcXeDxmTDnD4qMmgcBezHWthydUcK66XhZXIlwNQ6yoCTBS75ifUCD%2FImJfYPdClKurBU6MTIvHTIvhb5daodgCEJM%2BwQWPAGOs%2FjRrs7o2%2BopVMQLLDBqcyrDdJrI%2B1XM69Z5qXVxdhTVNayG22R545iv2tvafQr7Z4SAqJr6P7EYupMfgVTCuHyOMJEG0SJd4f3d4arqF%2Bg0gY5drdpJMp94P06X5YovTwldW3t8fIB2QhAqjSRCCr&firstvrytype=1&random=0.017271072963999323&_=1522664696316".format(
        #         d['asig'])
        #     headers_capt = {
        #         'Host': 'captcha.guard.qcloud.com',
        #         'Accept': 'application/json, text/javascript, */*; q=0.01',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         # 'Referer': vsig_url,
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        #         'X-Requested-With': 'XMLHttpRequest',
        #     }
        #     for s in range(5):
        #         try:
        #             sess = session.get(sess_url, headers=headers_capt, timeout=10)
        #             break
        #         except Exception as e:
        #             self.logger.info(e)
        #             self.logger.info(sess_url)
        #             time.sleep(5)
        #             continue
        #     vsig_url = "https://captcha.guard.qcloud.com/cap_union_new_show?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point".format(
        #         d['asig'], sess.json()["sess"])
        #     for s in range(5):
        #         try:
        #             vsig_r = session.get(vsig_url, headers=headers_capt, timeout=10)
        #             break
        #         except Exception as e:
        #             self.logger.info(e)
        #             time.sleep(5)
        #             self.logger.info(vsig_url)
        #             continue
        #     ad = re.search("Q=\"(.*?)\"", vsig_r.text)
        #     websig = re.search("websig\:\"(.*?)\"", vsig_r.text)
        #     websig = websig.group(1)
        #     et = re.search("et=\"(.*?)\"", vsig_r.text)
        #     et = et.group(1)
        #     vsig = ad.group(1)
        #     jsstr = self.get_js()
        #     ctx = execjs.compile(jsstr)
        #     cdat = ctx.call('cdata', et)
        #     image_url = "https://captcha.guard.qcloud.com/cap_union_new_getcapbysig?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point&rand=0.5730110856415294&vsig={}&img_index=1".format(
        #         d['asig'], sess.json()["sess"], vsig)
        #     y_locte = re.search("Z=Number\(\"(.*?)\"", vsig_r.text)
        #     y_locte = int(y_locte.group(1))
        #     post_url = "https://captcha.guard.qcloud.com/template/new_placeholder.html?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=102579&forcestyle=undefined".format(
        #         d['asig'])
        #     for s in range(5):
        #         try:
        #             holder = session.get(post_url, headers=headers_capt, timeout=10)
        #             if "tdc.js" in holder.text or "TDC.js" in holder.text:
        #                 ase = False
        #             else:
        #                 ase = True
        #             break
        #         except Exception as e:
        #             self.logger.info(e)
        #             self.logger.info(post_url)
        #             time.sleep(5)
        #             continue
        #     client = suds.client.Client(url="http://39.108.112.203:8023/yzmmove.asmx?wsdl")
        #     # client = suds.client.Client(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl")
        #     for s in range(5):
        #         try:
        #             resp = session.get(image_url)
        #             break
        #         except Exception as e:
        #             self.logger.info(e)
        #             self.logger.info(image_url)
        #             time.sleep(5)
        #             continue
        #     con = str(base64.b64encode(resp.content))[2:-1]
        #     auto = client.service.GetYZCodeForDll(con)
        #     try:
        #         x_locate = int(auto)
        #     except:
        #         x_locate = 475
        #     client = suds.client.Client(url="http://120.79.184.213:8023/yzmmove.asmx?wsdl")
        #     # x_locate = client.service.GetTackXForDll(image_url, y_locte)
        #     track = client.service.GetTackDataForDll(int(x_locate), cdat, ase)
        #     track = json.loads(track)["Data"]
        #     time_l = str(int(time.time() * 1000))
        #     ticket_url = 'https://captcha.guard.qcloud.com/cap_union_new_verify?random={}'.format(time_l)
        #     login_data = 'aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=846062&forcestyle=undefined&rand=0.388811798088319&sess={}&firstvrytype=1&showtype=point&subcapclass=10&vsig={}&ans={},{};&cdata=68&badbdd={}&websig={}&fpinfo=undefined&tlg=1&vlg=0_0_0&vmtime=_&vmData='.format(
        #         d['asig'], sess.json()["sess"], vsig, x_locate, y_locte, track, websig)
        #     session = requests.session()
        #     retry = Retry(connect=3, backoff_factor=1)
        #     adapter = HTTPAdapter(max_retries=retry)
        #     session.mount('http://', adapter)
        #     session.mount('https://', adapter)
        #     headers = {
        #         'Host': 'captcha.guard.qcloud.com',
        #         'Accept': 'application/json, text/javascript, */*; q=0.01',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         'Referer': vsig_url,
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        #         'X-Requested-With': 'XMLHttpRequest',
        #         'Origin': 'https://captcha.guard.qcloud.com'}
        #     for s in range(5):
        #         try:
        #             tickek = session.post(ticket_url, data=login_data, headers=headers, timeout=10)
        #             break
        #         except Exception as e:
        #             self.logger.info(e)
        #             self.logger.info(ticket_url)
        #             time.sleep(5)
        #             continue
        #     tickek = json.loads(tickek.text)["ticket"]
        #     self.logger.info("ticket:{}".format(tickek))
        #     if not tickek:
        #         jyjg = False
        #     else:
        #         jyjg = True
        #     headers = {'Host': 'captcha.guard.qcloud.com',
        #                'Accept': 'application/json, text/javascript, */*; q=0.01',
        #                'Accept-Language': 'zh-CN,zh;q=0.9',
        #                'Content-Type': 'application/json; charset=UTF-8',
        #                'Accept-Encoding': 'gzip, deflate',
        #                'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
        #                'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        #                'X-Requested-With': 'XMLHttpRequest',
        #                'x-form-id': 'mobile-signin-form',
        #                'Origin': 'http://dzswj.szgs.gov.cn'}
        #     time_l = time.localtime(int(time.time()))
        #     time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
        #     login_data = '{"nsrsbh":"%s","nsrpwd":"%s","tagger":"%s","redirectURL":"","time":"%s"}' % (
        #         self.user, self.jiami(), tickek, time_l)
        #     self.logger.info(login_data)
        #     login_url = 'http://dzswj.szgs.gov.cn/api/auth/txClientWt'
        #     for s in range(3):
        #         try:
        #             resp = session.post(login_url, data=login_data, timeout=25)
        #             break
        #         except:
        #             self.logger.info(login_url)
        #             continue
        #     self.logger.info("customerid:{},成功post数据".format(self.customerid))
        #     try:
        #         if jyjg:
        #             if "登录成功" in resp.json()['message']:
        #                 print('登录成功')
        #                 self.logger.info('customerid:{}pass'.format(self.customerid))
        #                 cookies = {}
        #                 for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
        #                     cookies[k] = v
        #                 return cookies,session
        #             elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in \
        #                     resp.json()['message']:
        #                 self.logger.info("密码有误，尝试更换账号")
        #                 print('账号和密码不匹配')
        #                 self.logger.info('customerid:{}账号和密码不匹配'.format(self.customerid))
        #                 status = "账号和密码不匹配"
        #                 return status,session
        #             else:
        #                 time.sleep(3)
        #     except Exception as e:
        #         self.logger.warn("customerid:{}登录失败".format(self.customerid))
        #     self.logger.warn("customerid:{}登录失败,开始重试".format(self.customerid))
        # self.logger.warn("{}登陆失败".format(self.customerid))
        # return False
        try_times = 0
        user = self.user
        have_backup = True
        while try_times <= 20:
            self.logger.info('customerid:{},开始尝试登陆'.format(self.customerid))
            try_times += 1
            if try_times > 10:
                time.sleep(2)
            session = requests.session()
            # proxy_list = get_all_proxie()
            # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            proxy_list = [
                {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
                {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
                {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
                {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
                {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
                {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
                {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
                {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
                {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
                {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
                {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
                {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
                {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
                {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
                {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
            ]
            proxy = proxy_list[random.randint(0, 14)]
            session.proxies = proxy
            headers = {'Host': 'dzswj.szgs.gov.cn',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Content-Type': 'application/json; charset=UTF-8',
                       'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                       'x-form-id': 'mobile-signin-form',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Origin': 'http://dzswj.szgs.gov.cn'}
            session.get("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html", headers=headers)
            captcha_url = 'http://dzswj.szgs.gov.cn/tipCaptcha'
            tupian_resp = session.get(url=captcha_url, timeout=10)
            tupian_resp.encoding = 'utf8'
            tupian = tupian_resp.json()
            image = tupian['image']
            tipmessage = tupian["tipMessage"]
            tupian = json.dumps(tupian, ensure_ascii=False)
            m = hashlib.md5()
            tupian1 = tupian.encode(encoding='utf8')
            m.update(tupian1)
            md = m.hexdigest()
            print(md)
            # logger.info("customerid:{},:{}".format(self.customerid,tupian))
            tag = self.tagger(tupian, md)
            self.logger.info("customerid:{}，获取验证码为：{}".format(self.customerid, tag))
            if tag is None:
                continue
            jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
            self.logger.info("customerid:{}，验证验证码{}".format(self.customerid, tag))
            time_l = time.localtime(int(time.time()))
            time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
            self.logger.info("customerid:{}，转换tag".format(self.customerid))
            tag = json.dumps(tag)
            self.logger.info("customerid:{}，转换tag完成".format(self.customerid))
            self.logger.info("customerid:{}，{},{},{},{}".format(self.customerid, self.user, self.jiami(), tag, time_l))
            login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
                user, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
            self.logger.info(login_data)
            self.logger.info("customerid:{},成功post数据".format(self.customerid))
            # panduan=resp.json()['message']
            # self.logger(panduan)
            try:
                if "验证码正确" in jyjg.json()['message']:
                    if "登录成功" in resp.json()['message']:
                        print('登录成功')
                        self.logger.info('customerid:{}pass'.format(self.customerid))
                        cookies = {}
                        for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                            cookies[k] = v
                        return cookies,session
                    elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in \
                            resp.json()['message']:
                        print('账号和密码不匹配')
                        self.logger.info('customerid:{}账号和密码不匹配'.format(self.customerid))
                        status = "账号和密码不匹配"
                        return status,session
                    else:
                        time.sleep(3)
            except Exception as e:
                self.logger.warn("customerid:{}登录失败".format(self.customerid))
            self.logger.warn("customerid:{}登录失败,开始重试".format(self.customerid))
        self.logger.warn("{}登陆失败".format(self.customerid))
        return False
    def gssfzrd(self, browser):
        wait = ui.WebDriverWait(browser, 10)
        browser.find_element_by_css_selector('#zsxm input').send_keys("全部")
        browser.find_element_by_css_selector("#stepnext").click()
        time.sleep(3)
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="mini-grid-table-bodysfz-grid"]/tbody/tr')
        sfz = {}
        for i in select[1:]:
            dt = {}
            shuizhong = i.xpath('.//text()')
            dt['税种'] = shuizhong[1]
            dt['税目'] = shuizhong[2]
            dt['有效期起'] = shuizhong[3]
            dt['有效期止'] = shuizhong[4]
            dt['申报期限'] = shuizhong[5]
            sfz[shuizhong[0]] = dt
        # sfz=json.dumps(sfz,ensure_ascii=False)
        self.logger.info("customerid{}税费种信息{}:".format(self.customerid, sfz))
        return sfz

    def gsjbxx(self, browser, session):
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//div[@class="user-info1"]//div')
        nsrxx = {}
        for i in select[1:]:
            shuizhong = i.xpath('.//text()')
            if len(shuizhong)==2:
                nsrxx[shuizhong[0]] = shuizhong[1]
            elif len(shuizhong)==1:
                nsrxx[shuizhong[0]]=""
        jbxx = session.get("http://dzswj.szgs.gov.cn/gzcx/gzcxAction_queryNsrxxBynsrsbh.do").json()
        jbxx = jbxx["data"]
        data = jbxx[0]
        shxydm = data['shxydm']
        nsrmc = data['nsrmc']
        szxinyong['xydm'] = shxydm
        szxinyong['cn'] = nsrmc
        jcsj = {}
        jcsj["jcxx"] = nsrxx
        self.logger.info("customerid:{},基础信息{}".format(self.customerid, jcsj["jcxx"]))
        jcsj['xxxx'] = jbxx
        self.logger.info("customerid:{},详细信息{}".format(self.customerid, jcsj['xxxx']))

        # 资格查询
        browser.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sscx/nsrzgxxcx/nsrzgrdxxcx.html')
        browser.find_element_by_xpath('//input[@id="nsrsbh$text"]').send_keys(self.user)
        browser.find_element_by_css_selector("#stepnext").click()
        time.sleep(2)
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="mini-grid-table-bodyzgrdxxGrid"]/tbody/tr')
        gszgcx = {}
        for i in select[1:]:
            tiaomu = {}
            zgtb = i.xpath('.//text()')
            title = ['序号', '纳税人资格认定名称', '认定日期', '有效期起', '有效期止']
            for j in range(len(zgtb)):
                tiaomu[title[j]] = zgtb[j]
            gszgcx[zgtb[0]] = tiaomu

        jcsj['纳税人资格查询'] = gszgcx
        # jcsj=json.dumps(jcsj,ensure_ascii=False)
        self.logger.info("customerid:{},json信息{}".format(self.customerid, jcsj))
        return jcsj

    # 前往地税
    def qwdishui(self, browser):
        try_times = 0
        while try_times <= 3:
            ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
            browser.get(url=ds_url)
            self.logger.info("customerid:{}开始登录地税".format(self.customerid))
            wait = ui.WebDriverWait(browser, 10)
            try:
                wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
                browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
            except:
                print("无该弹窗")
            try:
                browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
            except:
                print("无该弹窗")
            browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
            try:
                dsdjxx, dssfz = self.dishui(browser)
                return dsdjxx, dssfz
            except Exception as e:
                self.logger.warn(e)
                pg = browser.page_source
                if "抱歉" in pg:
                    browser.find_element_by_xpath('//button[@type="button"]').click()
                browser.get("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
                try_times += 1
                if try_times > 3:
                    return {}, {}

    def dishui(self, browser):
        self.logger.info("customerid:{}截取地税登记信息".format(self.customerid))
        time.sleep(2)
        windows = browser.window_handles
        window1 = browser.current_window_handle
        for c_window in windows:
            if c_window != window1:
                browser.close()
                browser.switch_to_window(c_window)
        wait = ui.WebDriverWait(browser, 10)
        wait.until(
            lambda browser: browser.find_element_by_css_selector("#layui-layer1 div.layui-layer-btn a"))  # timeout
        browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
        browser.find_element_by_css_selector('#menu_110000_110109').click()
        time.sleep(2)
        browser.switch_to_frame('qyIndex')
        browser.switch_to_frame('qymain')
        time.sleep(2)  # 容易timeout
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//div[@id="content"]//tbody/tr')
        dsdjxx = {}
        a = 0
        for i in select:
            dsdjxx1 = {}
            a += 1
            dsdjtb = i.xpath('.//text()')
            l = map(lambda x: x.strip(), dsdjtb)
            l = list(l)
            dsdjtb = list(filter(lambda x: x.strip(), l))
            for j in range(0, len(dsdjtb), 2):
                if j + 1 == len(dsdjtb):
                    dsdjxx1[dsdjtb[j]] = ""
                else:
                    dsdjxx1[dsdjtb[j]] = dsdjtb[j + 1]
                end = j + 1
                endflag = len(dsdjtb) - 1
                if end >= endflag:
                    dsdjxx[a] = dsdjxx1
                    break
        # 地税税费种认定信息
        browser.switch_to_default_content()
        browser.switch_to_frame('qyIndex')
        browser.find_element_by_css_selector('#menu3_4_110101').click()
        browser.switch_to_frame('qymain')
        wait.until(
            lambda browser: browser.find_element_by_css_selector("#btn_query"))  # timeout
        browser.find_element_by_css_selector('#btn_query').click()
        time.sleep(2)
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="dataTab"]/tbody/tr')
        dssfz = {}
        for i in select:
            tiaomu = {}
            dssfztb = i.xpath('.//text()')
            title = ['序号', '征收项目', '征收品目', '申报期限', '纳税期限', '税率', '征收代理方式', '有效期起', '有效期止']
            for j in range(len(dssfztb)):
                tiaomu[title[j]] = dssfztb[j]
            dssfz[dssfztb[0]] = tiaomu
        return dsdjxx, dssfz

    def excute_spider(self):
        try:
            cookies, session = self.login()
            self.logger.info("customerid:{}获取cookies".format(self.customerid))
            jsoncookies = json.dumps(cookies, ensure_ascii=False)
            if "账号和密码不匹配" in jsoncookies:
                self.logger.warn("customerid:{}账号和密码不匹配".format(self.customerid))
                job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-2',
                           "账号和密码不匹配")
                return
            with open('cookies/{}cookies.json'.format(self.batchid), 'w') as f:  # 将login后的cookies提取出来
                f.write(jsoncookies)
                f.close()
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn("customerid:{}登陆失败".format(self.customerid))
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "登录失败")
            return False
        try:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
            dcap["phantomjs.page.settings.loadImages"] = True
            service_args = []
            service_args.append('--webdriver=szgs')
            # browser = webdriver.PhantomJS(
            #     executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
            #     desired_capabilities=dcap,service_args=service_args)
            browser = webdriver.PhantomJS(
                executable_path='/home/tool/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                desired_capabilities=dcap)
            browser.implicitly_wait(10)
            browser.set_script_timeout(20)
            browser.set_page_load_timeout(60)
            browser.viewportSize = {'width': 2200, 'height': 2200}
            browser.set_window_size(1400, 1600)  # Chrome无法使用这功能
            # options = webdriver.ChromeOptions()
            # options.add_argument('disable-infobars')
            # options.add_argument("--start-maximized")
            # browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe',chrome_options=options)  # 添加driver的路径
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn("浏览器启动失败")
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "浏览器启动失败")
            return False
        try:
            index_url = "http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html"
            browser.get(url=index_url)
            browser.delete_all_cookies()
            with open('cookies/{}cookies.json'.format(self.batchid), 'r', encoding='utf8') as f:
                cookielist = json.loads(f.read())
            for (k, v) in cookielist.items():
                browser.add_cookie({
                    'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
                    'name': k,
                    'value': v,
                    'path': '/',
                    'expires': None})
            shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sscx/nsrsfzrdxxcx/nsrsfzrdxxcx.html'
            browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
            browser.get(url=shenbao_url)
            time.sleep(3)
            sfzrd = self.gssfzrd(browser)
            self.logger.info("customerid{}税费种信息{}:".format(self.customerid, sfzrd))
        except Exception as e:
            self.logger.info("customerid:{}SFZ出错".format(self.customerid))
            self.logger.warn(e)
            self.logger.info("SFZ查询失败")
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "SFZ查询失败")
            browser.quit()
            return False
        try:
            # JBXXCX
            jk_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sscx/nsrjbxxcx/nsrjbxxcx.html'
            browser.get(url=jk_url)
            try:
                jbxx = self.gsjbxx(browser, session)
            except Exception as e:
                self.logger.info(e)
                self.logger.info("国税基本查询失败")
                job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1',
                           "gs查询失败")
                browser.quit()
                return False
            if self.companyname!=szxinyong['cn'] and self.companyname:
                browser.quit()
                return False
            try:
                dsdjxx, dssfz = self.qwdishui(browser)
            except Exception as e:
                self.logger.warn(e)
                self.logger.info("地税失败")
            dsxiangqing = {}
            gsxiangqing = {}
            gsxiangqing["国税信息"] = jbxx
            dsxiangqing["地税信息"] = dsdjxx
            gsshuifei = {}
            dsshuifei = {}
            gsshuifei["国税税费种信息"] = sfzrd
            dsshuifei["地税税费种信息"] = dssfz
            gsxiangqing["账号详情"] = {'账号': self.user, '密码': self.pwd}
            dsxiangqing = json.dumps(dsxiangqing, ensure_ascii=False)
            dsshuifei = json.dumps(dsshuifei, ensure_ascii=False)
            gsxiangqing = json.dumps(gsxiangqing, ensure_ascii=False)
            gsshuifei = json.dumps(gsshuifei, ensure_ascii=False)
            params = (
            self.batchid, "0", "0", self.companyid, self.customerid, gsxiangqing, gsshuifei, dsxiangqing, dsshuifei)
            self.logger.info(params)
            try:
                self.insert_db("[dbo].[Python_Serivce_GSTaxInfo_Add]", params)
            except Exception as e:
                self.logger.info("数据库插入失败")
                self.logger.warn(e)
                job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1',
                           "数据库插入失败")
                browser.quit()
                return False
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '1', '成功爬取')
            print("爬取完成")
            self.logger.info("customerid:{}全部爬取完成".format(self.customerid))
            browser.quit()
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn("数据异常")
            job_finish(self.host, self.port, self.db, self.batchid, self.companyid, self.customerid, '-1', "数据异常")
            browser.quit()


class szcredit(object):
    def __init__(self, cn, sID, batchid, companyid, customerid, logger):
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Host': 'www.szcredit.org.cn',
                        'Cookie': 'UM_distinctid=160a1f738438cb-047baf52e99fc4-e323462-232800-160a1f73844679; ASP.NET_SessionId=4bxqhcptbvetxqintxwgshll',
                        'Origin': 'https://www.szcredit.org.cn',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Referer': 'https://www.szcredit.org.cn/web/gspt/newGSPTList.aspx?keyword=%u534E%u88D4&codeR=28',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        }
        self.logger = logger
        self.batchid = batchid
        self.cn = cn
        self.sID = sID
        self.companyid = companyid
        self.customerid = customerid
        self.query = [sID, cn]
        self.host, self.port, self.db = get_db(companyid)

    def insert_db(self, sql, params):
        conn = pymssql.connect(host=self.host, port=self.port, user='Python', password='pl,okmPL<OKM',
                               database=self.db, charset='utf8')
        cur = conn.cursor()
        if not cur:
            raise Exception("数据库连接失败")
        # cur.callproc('[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
        len(params)
        cur.callproc(sql, params)
        conn.commit()
        cur.close()

    def login(self):
        for t in range(3):
            session = requests.session()
            proxy_list = [
                {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
                {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
                {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
                {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
                {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
                {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
                {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
                {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
                {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
                {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
                {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
                {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
                {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
                {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
                {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
            ]
            proxy = proxy_list[random.randint(0, 14)]
            session.proxies = proxy
            yzm_url = 'https://www.szcredit.org.cn/web/WebPages/Member/CheckCode.aspx?'
            yzm = session.get(url=yzm_url, headers=self.headers)
            for q in self.query:
                # 处理验证码
                try:
                    if not q.strip():
                        self.logger.info(q)
                        continue
                except:
                    self.logger.info(q)
                # with open("{}yzm.jpg".format(self.batchid), "wb") as f:
                #     f.write(yzm.content)
                #     f.close()
                # with open("{}yzm.jpg".format(self.batchid), 'rb') as f:
                base64_data = str(base64.b64encode(yzm.content))
                base64_data = "data:image/jpg;base64," + base64_data[2:-1]
                post_data = {"a": 2, "b": base64_data}
                post_data = json.dumps({"a": 2, "b": base64_data})
                res = session.post(url="http://39.108.112.203:8002/mycode.ashx", data=post_data)
                    # print(res.text)
                    # f.close()
                postdata = {'action': 'GetEntList',
                            'keyword': q,
                            'type': 'query',
                            'ckfull': 'false',
                            'yzmResult': res.text
                            }
                resp1 = session.post(url='https://www.szcredit.org.cn/web/AJax/Ajax.ashx', headers=self.headers,
                                     data=postdata)
                self.logger.info(resp1.text)
                resp = resp1.json()
                try:
                    result = resp['resultlist']
                except Exception as e:
                    self.logger.warn(e)
                    self.logger.info(resp)
                    self.logger.info("网络连接失败")
                    sleep_time = [5.2, 4.7, 5.8, 4.5, 5, 4.1, 5.5, 5.7, 5.3, 6.6]
                    time.sleep(sleep_time[random.randint(0, 9)])
                    continue
                if resp1 is not None and resp1.status_code == 200 and result:
                    result_dict = result[0]
                    print(result_dict["RecordID"])  # 获取ID
                    detai_url = 'https://www.szcredit.org.cn/web/gspt/newGSPTDetail3.aspx?ID={}'.format(
                        result_dict["RecordID"])
                    session = requests.session()
                    proxy_list = [
                        {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
                        {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
                        {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
                        {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
                        {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
                        {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
                        {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
                        {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
                        {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
                        {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
                        {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
                        {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
                        {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
                        {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
                        {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
                    ]
                    proxy = proxy_list[random.randint(0, 14)]
                    session.proxies = proxy
                    detail = session.get(url=detai_url, headers=self.headers, timeout=30)
                    for i in range(3):
                        if self.cn not in detail.text:
                            self.logger.info("您的查询过于频繁，请稍候再查")
                            sleep_time = [13, 14, 13.5, 14.5, 13.2, 13.8, 13.1, 13.7, 13.3, 13.6]
                            time.sleep(sleep_time[random.randint(0, 9)])
                            session = requests.session()
                            proxy_list = [
                                {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
                                {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
                                {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
                                {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
                                {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
                                {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
                                {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
                                {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
                                {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
                                {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
                                {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
                                {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
                                {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
                                {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
                                {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
                            ]
                            proxy = proxy_list[random.randint(0, 14)]
                            session.proxies = proxy
                            detail=session.get(detai_url,headers=self.headers,timeout=30)
                            if self.cn in detail.text:
                                break
                            else:
                                return 4
                    detail.encoding = detail.apparent_encoding
                    root = etree.HTML(detail.text)  # 将request.content 转化为 Element
                    self.parse(root)
                return

    def parse(self, root):
        title = root.xpath('//*[@id="Table31"]//li[@class="current"]')
        t_list = []
        for t in title:
            tt = t.xpath(".//a[1]/text()")
            print(tt[0])
            t_list.append(tt[0])

        tb_list = []
        tb = root.xpath('//*[@id="Table31"]//table')  # 抓取table31
        for i in tb:
            data_json = []
            tb_detail = i.xpath(".//tr")
            for j in tb_detail:
                t = j.xpath('./td//text()')
                data_json.append(t)
                # data_json[t[0]]=t[1]
            # data_json=json.dumps(data_json,ensure_ascii=False)
            # print(data_json)
            tb_list.append(data_json)

        data_dict = {}
        for i in range(len(t_list)):
            data_dict[t_list[i]] = tb_list[i]
        print(data_dict)

        if "登记备案信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["登记备案信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["登记备案信息"] = d1
            # dm = {}
            # dm["登记备案信息"] = d1
            # print(dm)

        if "股东登记信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["股东登记信息"]
            d2 = {}
            for i in get_data[1:]:
                d3 = {}
                d3['出资额'] = i[4]
                d3['出资比例'] = i[5]
                d2[i[0]] = d3
            d1['股东名称'] = d2
            data_dict["股东登记信息"] = d1
            dm = {}
            dm["股东登记信息"] = d1
            print(dm)

        if "成员登记信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["成员登记信息"]
            for i in get_data[1:]:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["成员登记信息"] = d1
            # dm = {}
            # dm["成员登记信息"] = d1
            # print(dm)

        if "税务登记信息(国税)" in data_dict.keys():
            d1 = {}
            get_data = data_dict["税务登记信息(国税)"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["税务登记信息(国税)"] = d1
            # dm = {}
            # dm["税务登记信息(国税)"] = d1
            # print(dm)

        if "税务登记信息(地税)" in data_dict.keys():
            d1 = {}
            get_data = data_dict["税务登记信息(地税)"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["税务登记信息(地税)"] = d1
            # dm = {}
            # dm["税务登记信息(地税)"] = d1
            # print(dm)

        if "机构代码信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["机构代码信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["机构代码信息"] = d1
            # dm = {}
            # dm["机构代码信息"] = d1
            # print(dm)

        if "印章备案信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["印章备案信息"]
            d2 = {}
            for i in get_data[1:]:
                d3 = {}
                d3['印章编码'] = i[1]
                d3['审批日期'] = i[2]
                d3['备案日期'] = i[3]
                d3['备案情况'] = i[4]
                d3['详情'] = i[5]
                d2[i[0]] = d3
            d1['印章名称'] = d2
            data_dict["印章备案信息"] = d1
            # dm = {}
            # dm["印章备案信息"] = d1
            # print(dm)

        if "企业参保信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["企业参保信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["企业参保信息"] = d1
            # dm = {}
            # dm["企业参保信息"] = d1
            # print(dm)

        if "海关企业基本登记信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["海关企业基本登记信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["海关企业基本登记信息"] = d1
            # dm = {}
            # dm["海关企业基本登记信息"] = d1
            # print(dm)

        if "高新技术企业认定信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["高新技术企业认定信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["高新技术企业认定信息"] = d1
            # dm = {}
            # dm["高新技术企业认定信息"] = d1
            # print(dm)

        if "对外贸易经营者备案登记资料" in data_dict.keys():
            d1 = {}
            get_data = data_dict["对外贸易经营者备案登记资料"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["对外贸易经营者备案登记资料"] = d1
            # dm = {}
            # dm["对外贸易经营者备案登记资料"] = d1
            # print(dm)

        if "住房公积金缴存数据表" in data_dict.keys():
            d1 = {}
            get_data = data_dict["住房公积金缴存数据表"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["住房公积金缴存数据表"] = d1
            # dm = {}
            # dm["住房公积金缴存数据表"] = d1
            # print(dm)

        if "电子商务认证企业信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["电子商务认证企业信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["电子商务认证企业信息"] = d1
            # dm = {}
            # dm["电子商务认证企业信息"] = d1
            # print(dm)

        if "电子商务认证企业网站信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["电子商务认证企业网站信息"]
            for i in get_data:
                try:
                    d1[i[0]] = i[1]
                except:
                    d1[i[0]] = ""
            data_dict["电子商务认证企业网站信息"] = d1
            # dm = {}
            # dm["电子商务认证企业网站信息"] = d1
            # print(dm)

        if "企业年报信息" in data_dict.keys():
            get_data = data_dict["企业年报信息"]
            d2 = {}
            for i in range(int(len(get_data) / 2)):
                d3 = {}
                d3['报送年度'] = get_data[i * 2][1]
                d3['发布日期'] = get_data[i * 2 + 1][1]
                d2[i + 1] = d3
            data_dict["企业年报信息"] = d1
            # dm = {}
            # dm["企业年报信息"] = d2
            # print(dm)

        # 企业变更信息
        try:
            title = root.xpath('//*[@id="Table123"]//li[@class="current"]')
            t_list = []
            for t in title:
                tt = t.xpath("./text()")
                print(tt[0])
                t_list.append(tt[0])

            tb_list = []
            tb = root.xpath('//*[@id="Table123"]//table')  # 抓取table31

            for i in tb:
                data_json = []
                tb_detail = i.xpath(".//tr")
                for j in tb_detail:
                    t = j.xpath('./td//text()')
                    data_json.append(t)
                    # data_json[t[0]]=t[1]
                # data_json=json.dumps(data_json,ensure_ascii=False)
                # print(data_json)
                tb_list.append(data_json)

            for i in range(len(t_list)):
                data_dict[t_list[i]] = tb_list[i]

            if "企业变更信息" in data_dict.keys():
                d1 = {}
                get_data = data_dict["企业变更信息"]
                d2 = {}

                for i in get_data[1:]:
                    d2['变更日期'] = i[1]
                    d2['变更事项'] = i[2]
                    d1[i[0]] = d2
                data_dict["企业变更信息"] = d1
        except:
            print("No exist")

        all_urls = []
        all_gd = []
        gdjg = {}
        gdxx = root.xpath('//*[@id="tb_1"]//tr')
        for i in gdxx[1:]:
            lianjie = i.xpath('.//@href')[0]
            lianjie = lianjie.strip()
            gdm = i.xpath('./td[1]/text()')[0]
            print(lianjie)
            all_urls.append(lianjie)
            all_gd.append(gdm)
        for j in range(len(all_urls)):
            clean_dict = {}
            gd_url = "https://www.szcredit.org.cn/web/gspt/{}".format(all_urls[j])
            gd_resp = requests.get(url=gd_url, headers=self.headers)
            gd_resp.encoding = gd_resp.apparent_encoding
            root = etree.HTML(gd_resp.text)
            gdxq = root.xpath('//table[@class="list"]//tr')
            a = 1
            for xq in gdxq[1:21]:
                sb = {}
                xx = xq.xpath('.//text()')
                clean = []
                for s in xx:
                    s = s.strip()
                    if s.strip and s is not "":
                        clean.append(s)
                print(clean)
                sb["企业名称"] = clean[0]
                sb["企业注册号"] = clean[1]
                sb["企业类型"] = clean[2]
                sb["成立日期"] = clean[3]
                clean_dict["{}".format(a)] = sb
                a += 1
            gdjg[all_gd[j]] = clean_dict
        print(gdjg)

        print(data_dict)
        data_dict["关联公司信息"] = gdjg
        infojson = json.dumps(data_dict, ensure_ascii=False)
        self.logger.info(infojson)
        params = (
            self.batchid, self.companyid, self.customerid, self.cn, self.sID, infojson
        )
        self.insert_db("[dbo].[Python_Serivce_WXWebShenZhen_Add]", params)

    def ssdjp(self):
        ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://app02.szmqs.gov.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'x-form-id': 'mobile-signin-form',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://app02.szmqs.gov.cn/outer/entSelect/gs.html',
            'X-Forwarded-For': ip[random.randint(0, 2)]
            # 'Cookie': 'Hm_lvt_5a517db11da5b1952c8edc36c230a5d6=1516416114; Hm_lpvt_5a517db11da5b1952c8edc36c230a5d6=1516416114; JSESSIONID=0000H--QDbjRJc2YKjpIYc_K3bw:-1'
        }
        session = requests.session()
        proxy_list = [
            {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
            {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
            {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
            {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
            {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
            {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
            {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
            {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
            {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
            {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
            {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
            {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
            {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
            {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
            {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
        ]
        proxy = proxy_list[random.randint(0, 14)]
        session.proxies = proxy
        # name='unifsocicrediden=&entname={}&flag=1'
        # postdata='unifsocicrediden=&entname={}&flag=1'.format()
        s = self.sID
        if s.strip():
            print('not null')
            postdata = 'unifsocicrediden={}&entname=&flag=1'.format(s)
            resp = session.post('https://app02.szmqs.gov.cn/outer/entEnt/detail.do', headers=headers, data=postdata,
                                timeout=30)
            self.logger.info(resp.text)
            gswsj = resp.json()
            gswsj = gswsj['data']
            gswsj = gswsj[0]
            gswsj = gswsj['data']
            jbxx = gswsj[0]
            if 'opto' in jbxx.keys():
                if jbxx['opto'] == "5000-01-01" or jbxx['opto'] == "1900-01-01" or jbxx['opto'].strip():
                    jbxx['营业期限'] = "永续经营"
                else:
                    jbxx['营业期限'] = "自" + jbxx['opfrom'] + "起至" + jbxx['opto'] + "止"
            else:
                jbxx['营业期限'] = "永续经营"

            index_dict = gswsj[0]
            id = index_dict['id']
            regno = index_dict['regno']
            opetype = index_dict['opetype']
            unifsocicrediden = index_dict['unifsocicrediden']
            pripid = index_dict['entflag']
            header2 = {
                'Origin': 'https://app02.szmqs.gov.cn',
                # 'Cookie': 'Hm_lvt_5a517db11da5b1952c8edc36c230a5d6=1516416114,1516590080; Hm_lpvt_5a517db11da5b1952c8edc36c230a5d6=1516590080; JSESSIONID=0000CgpyMFWxBHU8MWpcnjFhHx6:-1',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://app02.szmqs.gov.cn/outer/entSelect/gs.html',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive'
            }
            xqlist = ['许可经营信息',
                      '股东信息',
                      '成员信息',
                      '变更信息',
                      '股权质押信息',
                      '动产抵押信息',
                      '法院冻结信息',
                      '经营异常信息',
                      '严重违法失信信息']
            tagid = 1
            djxx = {}
            postdata = 'pripid={}&opetype={}'.format(pripid, opetype)
            nbresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/nb.do', headers=header2, data=postdata)
            if nbresp.status_code == 200:
                nb = nbresp.json()
                nb = nb['data']
                nb = nb[0]
                nb = nb['data']
                if len(nb) != 0:
                    yearnb = ''
                    for n in nb:
                        yearnb += "" + n['ancheyear'] + "年报已公示、"
                else:
                    yearnb = "无年报信息"
            jbxx["年报情况"] = yearnb
            djxx["基本信息"] = jbxx

            for i in xqlist:
                postdata = 'flag=1&tagId={}&id={}&regno={}&unifsocicrediden={}&opetype={}'.format(tagid, id, regno,
                                                                                                  unifsocicrediden,
                                                                                                  opetype)
                dtresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/tag.do', headers=header2, data=postdata)
                if dtresp.status_code == 200:
                    dt = dtresp.json()
                    dt = dt['data']
                    dt = dt[0]
                    dt = dt['data']
                    djxx[i] = dt
                tagid += 1
            djxx = json.dumps(djxx, ensure_ascii=False)
            params = (self.batchid, self.companyid, self.customerid, self.cn, self.sID, djxx)
            self.logger.info(params)
            self.insert_db('[dbo].[Python_Serivce_GSWebShenZhen_Add]', params)
        else:
            name = self.cn
            urlname = quote(name)
            postdata = 'unifsocicrediden=&entname={}&flag=1'.format(urlname)
            resp = session.post('https://app02.szmqs.gov.cn/outer/entEnt/detail.do', headers=headers, data=postdata)
            self.logger.info(resp.text)
            gswsj = resp.json()
            gswsj = gswsj['data']
            gswsj = gswsj[0]
            gswsj = gswsj['data']
            jbxx = gswsj[0]
            if 'opto' in jbxx.keys():
                if jbxx['opto'] == "5000-01-01" or jbxx['opto'] == "1900-01-01" or jbxx['opto'].strip():
                    jbxx['营业期限'] = "永续经营"
                else:
                    jbxx['营业期限'] = "自" + jbxx['opfrom'] + "起至" + jbxx['opto'] + "止"
            else:
                jbxx['营业期限'] = "永续经营"

            index_dict = gswsj[0]
            id = index_dict['id']
            regno = index_dict['regno']
            opetype = index_dict['opetype']
            unifsocicrediden = index_dict['unifsocicrediden']
            pripid = index_dict['entflag']
            header2 = {
                'Origin': 'https://app02.szmqs.gov.cn',
                # 'Cookie': 'Hm_lvt_5a517db11da5b1952c8edc36c230a5d6=1516416114,1516590080; Hm_lpvt_5a517db11da5b1952c8edc36c230a5d6=1516590080; JSESSIONID=0000CgpyMFWxBHU8MWpcnjFhHx6:-1',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://app02.szmqs.gov.cn/outer/entSelect/gs.html',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive'
            }
            xqlist = ['许可经营信息',
                      '股东信息',
                      '成员信息',
                      '变更信息',
                      '股权质押信息',
                      '动产抵押信息',
                      '法院冻结信息',
                      '经营异常信息',
                      '严重违法失信信息']
            tagid = 1
            djxx = {}
            postdata = 'pripid={}&opetype={}'.format(pripid, opetype)
            nbresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/nb.do', headers=header2, data=postdata)
            if nbresp.status_code == 200:
                nb = nbresp.json()
                nb = nb['data']
                nb = nb[0]
                nb = nb['data']
                if len(nb) != 0:
                    yearnb = ''
                    for n in nb:
                        yearnb += "" + n['ancheyear'] + "年报已公示、"
                else:
                    yearnb = "无年报信息"
            jbxx["年报情况"] = yearnb
            djxx["基本信息"] = jbxx

            for i in xqlist:
                postdata = 'flag=1&tagId={}&id={}&regno={}&unifsocicrediden={}&opetype={}'.format(tagid, id, regno,
                                                                                                  unifsocicrediden,
                                                                                                  opetype)
                dtresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/tag.do', headers=header2, data=postdata)
                if dtresp.status_code == 200:
                    dt = dtresp.json()
                    dt = dt['data']
                    dt = dt[0]
                    dt = dt['data']
                    djxx[i] = dt
                tagid += 1
            djxx = json.dumps(djxx, ensure_ascii=False)
            params = (self.batchid, self.companyid, self.customerid, self.cn, self.sID, djxx)
            self.logger.info(params)
            self.insert_db('[dbo].[Python_Serivce_GSWebShenZhen_Add]', params)


logger = create_logger(path=os.path.dirname(sys.argv[0]).split('/')[-1])
redis_cli = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


def run_test(user, pwd, batchid, companyid, customerid):
    print("++++++++++++++++++++++++++++++++++++")
    print('jobs[ts_id=%s] running....' % batchid)
    time.sleep(5)
    try:
        szxinyong.clear()
        cd = gscredit(user, pwd, batchid, companyid, customerid, logger,sd["9"])
        browser = cd.excute_spider()
        cn = szxinyong['cn']
        if sd['9'] !=cn and sd["9"]:
            job_finish(sd["6"], sd["7"], sd["8"], sd["3"], sd["4"], sd["5"], '-3', '公司信息和账号不一致')
            return False
        sID = szxinyong['xydm']
        credit = szcredit(cn=cn, sID=sID, batchid=batchid, companyid=companyid, customerid=customerid, logger=logger)
        try:
            credit.ssdjp()
        except Exception as e:
            logger.warn(e)
            logger.warn("工商网爬取失败")
            goshng_dict = {"1": cn, "2": sID, "3": batchid, "4": companyid,
                         "5": customerid, "6": sd["6"], "7": sd["7"], "8": sd["8"]}
            pjson = json.dumps(goshng_dict,ensure_ascii=False)
            redis_cli.lpush("gongshang",pjson)
        try:
            credit.login()
        except Exception as e:
            logger.info("信用网爬取失败")
            logger.info(e)
            xinyong_dict = {"1": cn, "2": sID, "3": batchid, "4": companyid,
                         "5": customerid, "6": sd["6"], "7": sd["7"], "8": sd["8"]}
            pjson = json.dumps(xinyong_dict,ensure_ascii=False)
            redis_cli.lpush("xinyong",pjson)
        job_finish(sd["6"], sd["7"], sd["8"], sd["3"], sd["4"], sd["5"], '1', '成功爬取')
        logger.info("深圳企业信用网信息抓取完成")
    except Exception as e:
        logger.error(e)
        # job_finish(sd["6"], sd["7"], sd["8"], sd["3"], sd["4"], sd["5"], '-1', 'error')
    print('jobs[ts_id=%s] done' % batchid)
    result = True
    return result


while True:
    # ss=redis_cli.lindex("list",0)
    ss = redis_cli.lpop("sz_credit_list")
    sleep_time = [3, 2, 5, 7, 9, 10, 1, 4, 8, 6]
    time.sleep(sleep_time[random.randint(0, 9)])
    if ss is not None:
        # print(redis_cli.lpop("list"))
        sd = json.loads(ss)
        run_test(sd["1"], sd["2"], sd["3"], sd["4"], sd["5"])
    else:
        time.sleep(10)
        print("no task waited")
