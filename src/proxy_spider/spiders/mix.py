# -*- coding: utf-8 -*-

"""

for some little spiders
"""
import json

from scrapy import Request

from proxy_spider.spiders import _BaseSpider


class MixSpider(_BaseSpider):
    name = 'mix'
    # allowed_domains = ['coderbusy.com']
    # custom_settings = {
    #     "DOWNLOAD_TIMEOUT": 20,
    # }

    def start_requests(self):
        # ip181
        url_181 = 'http://www.ip181.com/'
        yield Request(url_181, dont_filter=True, callback=self.parse_ip181)

        # iphai
        for url in [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp',
        ]:
            yield Request(url, dont_filter=True, callback=self.parse_iphai)


    def parse_iphai(self, response):
        data = response.xpath(
            '//table[@class="table table-bordered table-striped table-hover"]/tr')

        if data:
            for x in data[1:]:
                info = x.xpath('td/text()').extract()
                ip = info[0].strip()
                scheme = info[3].strip()
                port = info[1].strip()
                yield self.build_check_recipient(ip, port, scheme)

    def parse_ip181(self, response):
        if response.text:
            j = json.loads(response.text)
            for i in j['RESULT']:
                ip = i.get('ip')
                port = i.get('port')
                if ip and port:
                    for scheme in ('http', 'https'):
                        yield self.build_check_recipient(ip, port, scheme)
