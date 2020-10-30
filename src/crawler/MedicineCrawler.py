import scrapy,re
import string,sys
from lxml import html
import requests
seen = set()

class WebMdSpider(scrapy.Spider):
    name = 'webmd_crawler'
    download_delay = 0.3
    custom_settings = {'DEPTH_PRIORITY' :1,
    'SCHEDULER_DISK_QUEUE ': 'scrapy.squeues.PickleFifoDiskQueue',
    'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
    'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter'}

    def start_requests(self):
        start_url = "https://www.webmd.com/drugs/2/alpha/{}"
        url = []
        s = string.ascii_lowercase[:26]
        for c in s:
            url.append(start_url.format(c))


        for u in url:
            yield scrapy.Request(url=u,callback=self.sr_parse)

    def sr_parse(self,response):

        try:
            to_parse_list = []
            if response.status == 200:
                base_url = 'https://www.webmd.com'
                links = response.xpath('//*[@id="ContentPane30"]//div[@class="drugs-browse-subbox"]/ul/li/a/@href').extract()
                for l in links:
                    if '0-9' in l:
                        continue
                    to_parse_list.append(base_url+l)


            for p in to_parse_list:

                yield scrapy.Request(url=p,callback=self.temp_parse)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    #
    def temp_parse(self,response):
        base_url = 'https://www.webmd.com'

        links = response.xpath('//*[@id="ContentPane30"]//div[@class="drug-list-container"]/ul/li/a/@href').extract()
        #print(links)

        for l in links:
            a = base_url +l

            yield scrapy.Request(url=a,callback=self.parse)


    def parse(self,response):
        name = response.xpath('//*[@id="ContentPane29"]//div[@class="drug-names"]/h1/text()').get().strip()
        if len(name.split()) > 1 and name.split()[0].lower() not in seen:
            seen.add(name.split()[0].lower())
        else:
            return

        #print(len(seen))

        generic_name = response.xpath('//*[@id="ContentPane29"]//div[@class="drug-names"]/p//text()').get()
        regex = r"(\s*)G(\s*)E(\s*)N(\s*)E(\s*)R(\s*)I(\s*)C(\s*)N(\s*)A(\s*)M(\s*)E(\s*)\(s\)(s*)\:(s*)"
        generic_name = re.sub(regex,'',generic_name,flags=re.IGNORECASE).strip()
        side_effects = ''.join(response.xpath('//*[@id="tab-2"]//div[@class="inner-content"]//p//text()').getall()).strip()
        usage =  ''.join(response.xpath('//*[@id="tab-1"]//div[@class="inner-content"]//p//text()').getall()).strip()
        url = response.url
        yield {"url":url,"name":name,"generic_name":generic_name,"side_effects":side_effects,"usage":usage}








































