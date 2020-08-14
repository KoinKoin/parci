import scrapy
from scrapy.spiders import CrawlSpider, Request
import requests
import json
import os

import time

import datetime



class parciScrap(CrawlSpider):
    name = 'scraper_parci'
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 12,
        'RETRY_TIMES': 1,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 400, 308],

        # 'PROXY': 'http://127.0.0.1:8888/?noconnect',
        # 'API_SCRAPOXY': 'http://127.0.0.1:8889/api',
        # 'API_SCRAPOXY_PASSWORD': '***',

        'PROXY_LIST': 'http_proxies.txt',
        'PROXY_MODE': 0,

        'HTTPCACHE_ENABLED': False,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [404, 500, 407, 504],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        #        'ITEM_PIPELINES': {
        # 'myscraper.pipelines.MyscraperCaractRap': 400,
        # 'myscraper.pipelines.MyscraperPartant': 500
        #        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 100,
            # 'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 101,
            # 'scrapoxy.downloadmiddlewares.scale.ScaleMiddleware': 102,
            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            # 'scrapoxy.downloadmiddlewares.blacklist.BlacklistDownloaderMiddleware': 950,

            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy_proxies.RandomProxy': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,

        }
    }

    def start_requests(self):
        try:
            self.tagdate
        except:
            self.tagdate = datetime.datetime.now().date()
            # self.tagdate -= datetime.timedelta(days=1)
            self.tagdate = str(self.tagdate.strftime('%d/%m/%Y'))
        try:
            self.i
        except:
            self.i = 3
        
        try:
            self.reu
            url_reunion = 'http://parci.free.fr/include/prixListe.php?idReunion=' + self.reu
            yield scrapy.Request(
                url_reunion,
                meta={
                    'jour': '01/01/2000',
                    'idReunion': self.reu
                },
                callback=self.parse_reunion)
            raise SystemExit(0)
        except:
            pass
        try:
            self.prix
            url_course = 'http://parci.free.fr/include/prixId.php?id=' + self.prix
            yield scrapy.Request(
                url_course,
                meta={
                    'jour': '01/01/2000',
                    'idPrix': self.prix
                },
                callback=self.parse_course)
            raise SystemExit(0)
        except:
            pass
        
        # base = datetime.datetime.today() - datetime.timedelta(days=1)
        # date_list = [(base - datetime.timedelta(days=x)).strftime('%d/%m/%Y')
        #      for x in range(2414)]
        self.logger.info('tagdate==========> %s', self.tagdate)
        self.date = datetime.datetime.strptime(self.tagdate, '%d/%m/%Y')
        self.logger.info('date==========> %s', self.date.strftime('%d/%m/%Y'))
        
        # for date in date_list:
        for x in range(1, int(self.i) + 1):
            # print('http://parci.free.fr/include/reunions.php?date=' + date)
            yield scrapy.Request(
                'http://parci.free.fr/include/reunions.php?date=' + self.date.strftime('%d/%m/%Y'),
                meta={
                    'jour': self.date.strftime('%d/%m/%Y'),
                },
                callback=self.parse_programme)

            self.date -= datetime.timedelta(days=1)

    
    def parse_programme(self, response):
        json_res = json.loads(response.text)
        date = response.meta['jour']
        filename = 'data/%s/prog/%s.json' % (date.split('/')[2], date.replace('/', ''))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_res, f)

        for result in json_res['results']:
            url_reunion = 'http://parci.free.fr/include/prixListe.php?idReunion=' + result['idReunion']
            yield scrapy.Request(
                url_reunion,
                meta={
                    'jour': date,
                    'idReunion': result['idReunion']
                },
                callback=self.parse_reunion)
            # time.sleep(1)
            # with open('data/%s-%s.json' % (date.replace('/', ''), result['idReunion']), 'w', encoding='utf-8') as f:
            #     json_reunion_res = json.loads(r_reunion.text)
            #     json.dump(json_reunion_res, f)

    def parse_reunion(self, response):
        json_reunion_res = json.loads(response.text)
        date = response.meta['jour']
        idReunion = response.meta['idReunion']
        # print(json_reunion_res)
        filename = 'data/%s/reunions/%s.json' % (date.split('/')[2], idReunion)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_reunion_res, f)
        for result in json_reunion_res['results']:
            url_course = 'http://parci.free.fr/include/prixId.php?id=' + result['idPrix']
            yield scrapy.Request(
                url_course,
                meta={
                    'jour': date,
                    'idPrix': result['idPrix']
                },
                callback=self.parse_course)


    def parse_course(self, response):
        json_course_res = json.loads(response.text)
        date = response.meta['jour']
        idPrix = response.meta['idPrix']
        # print(json_reunion_res)
        filename = 'data/%s/courses/%s.json' % (date.split('/')[2], idPrix)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_course_res, f)


