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
import redis
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import ui
from guoshui import guoshui
from get_db import get_db, job_finish
import sys
from log_ging.log_01 import create_logger
from urllib.parse import quote

szxinyong = {}


class gscredit(guoshui):
    def __init__(self, user, pwd, batchid, companyid, customerid, logger):
        # self.logger = create_logger(path=os.path.basename(__file__) + str(customerid))
        self.logger = logger
        self.user = user
        self.pwd = pwd
        self.batchid = batchid
        self.companyid = companyid
        self.customerid = customerid
        self.host, self.port, self.db = get_db(companyid)

    def login(self):
        try_times = 0
        while try_times <= 14:
            self.logger.info('customerid:{},开始尝试登陆'.format(self.customerid))
            try_times += 1
            if try_times > 10:
                time.sleep(1)
            session = requests.session()
            # proxy_list = get_all_proxie()
            # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            try:
                session.proxies = sys.argv[1]

            except:
                self.logger.info("未传代理参数，启用本机IP")
            # session.proxies = {'https': 'http://116.22.211.55:6897', 'http': 'http://116.22.211.55:6897'}
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
                self.user, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
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
                        return cookies, session
                    elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in \
                            resp.json()['message']:
                        print('账号和密码不匹配')
                        self.logger.info('customerid:{}账号和密码不匹配'.format(self.customerid))
                        status = "账号和密码不匹配"
                        return status, session
                    else:
                        time.sleep(3)
            except Exception as e:
                self.logger.warn("customerid:{}登录失败".format(self.customerid))
            self.logger.warn("customerid:{}登录失败,开始重试".format(self.customerid))
        try_handed = 0
        while try_handed <= 3:
            self.logger.info("customerid:{}手动登陆".format())
            try_handed += 1
            session = requests.session()
            # proxy_list = get_all_proxie()
            # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            try:
                session.proxies = sys.argv[1]
            except:
                print("未传入代理参数")
            # session.proxies = {'https': 'http://116.22.211.55:6897', 'http': 'http://116.22.211.55:6897'}
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
            tag = self.taggertwo(tupian, md)
            jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
            time_l = time.localtime(int(time.time()))
            time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
            tag = json.dumps(tag)
            login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
                self.user, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
            panduan = resp.json()['message']
            if "验证码正确" in jyjg.json()['message']:
                if "登录成功" in resp.json()['message']:
                    print('登录成功')
                    cookies = {}
                    for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                        cookies[k] = v
                    return cookies, session
                elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in resp.json()[
                    'message']:
                    print('账号和密码不匹配')
                    self.logger.info('customerid:{}账号和密码不匹配'.format(self.customerid))
                    status = "账号和密码不匹配"
                    return status, session
                else:
                    time.sleep(3)
            else:
                self.logger.warn("customerid:{}登录失败,重试".format(self.customerid))
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
            nsrxx[shuizhong[0]] = shuizhong[1]
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
            try:
                session.proxies = sys.argv[1]
            except:
                self.logger.info("未传代理参数，启用本机IP")
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
                    sleep_time = [3, 4, 3.5, 4.5, 3.2, 3.8, 3.1, 3.7, 3.3, 3.6]
                    time.sleep(sleep_time[random.randint(0, 9)])
                    continue
                if resp1 is not None and resp1.status_code == 200 and result:
                    result_dict = result[0]
                    print(result_dict["RecordID"])  # 获取ID
                    detai_url = 'https://www.szcredit.org.cn/web/gspt/newGSPTDetail3.aspx?ID={}'.format(
                        result_dict["RecordID"])
                    detail = session.get(url=detai_url, headers=self.headers, timeout=30)
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
        try:
            session.proxies = sys.argv[1]
        except:
            self.logger.info("未传代理参数，启用本机IP")
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
        cd = gscredit(user, pwd, batchid, companyid, customerid, logger)
        browser = cd.excute_spider()
        cn = szxinyong['cn']
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
