# -*- coding: utf-8 -*-
# import scrapy
#
#
# class JdbookSpider(scrapy.Spider):
#     name = 'jdbook'
#     allowed_domains = ['https://book.jd.com/booksort.html']
#     start_urls = ['http://https://book.jd.com/booksort.html/']
#
#     def parse(self, response):
#         pass
import scrapy
# 导入item

import json


# 改成分布式
# 1------导入类
from scrapy_redis.spiders import RedisSpider

# 2------修改继承
from JD_Redis.items import JdRedisItem

# 非分布式做法
# class BookSpider(RedisSpider):
#     name = 'jdbook'
#     # 'p.3.cn' 为解析图书列表允许的列名
#     allowed_domains = ['jd.com', 'p.3.cn']
#     # allowed_domains = ['http://www.hongniang.com', 'p.3.cn']
#     # start_urls = ['https://book.jd.com/booksort.html']
#     # 3------定义redis_key
#     redis_key = 'jdbooks:start_urls'
#
#     def parse(self, response):
#         big_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
#         print('大节点', len(big_list))
#         for big in big_list:
#             # 获取到大分类的节点链接、节点名称
#             big_list_url = 'https:' + big.xpath('./@href').extract_first()
#             big_category = big.xpath('./text()').extract_first()
#             # 小分类的节点列表
#             small_list = big.xpath('../following-sibling::dd[1]/em/a')
#             # 遍历小分类的节点列表,获取到小分类名称、url
#             for small in small_list:
#                 temp = {}
#                 temp['big_list_url'] = big_list_url
#                 temp['big_category'] = big_category
#                 temp['small_category'] = small.xpath('./text()').extract_first()
#                 temp['small_category_url'] = 'https:' + small.xpath('./@href').extract_first()
#                 # print(temp)
#             # 构造请求,返回小分类的url
#                 yield scrapy.Request(
#                     temp['small_category_url'],
#                     callback=self.parse_book_list,
#                     meta={'meta1': temp}
#                  )
#
#     # 解析图片列表信息
#     def parse_book_list(self,response):
#         # 接受parse方法返回的meta数据
#         temp = response.meta['meta1']
#         # 获取图片列表节点
#         book_list = response.xpath('//*[@id="plist"]/ul/li/div')
#         # 遍历图书列表
#         for book in book_list:
#             # 实例化item
#             item = JdRedisItem()
#             # 书名信息、分类信息
#             item['name'] = book.xpath('./div[3]/a/em/text()').extract_first().strip()
#             item['big_category'] = temp['big_category']
#             item['big_category_url'] = temp['big_list_url']
#             item['small_category'] = temp['small_category']
#             item['small_category_url'] = temp['small_category_url']
#             # /div[1]/a/img/@src
#             try:
#                 item['cover_url'] = 'https:' + book.xpath('./div[1]/a/img/@src').extract_first()
#             except:
#                 item['cover_url'] = None
#             try:
#                 item['detail_url'] = 'https:' + book.xpath('./div[3]/a/@href').extract_first()
#             except:
#                 item['detail_url'] = None
#             item['author'] = book.xpath('./div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span[@class="author_type_1"]/a/text()').extract_first()
#             item['publisher'] = book.xpath('./div[@class="p-bookdetails"]/span[2]/a/text()').extract_first()
#             item['pub_date'] = book.xpath('./div[@class="p-bookdetails"]/span[3]/text()').extract_first().strip()
#             # 获取价格的url
#             # https://p.3.cn/prices/mgets?skuIds=J_11757834%2CJ_10367073%2CJ_11711801%2CJ_12090377%2CJ_10199768%2CJ_11711801%2CJ_12018031%2CJ_10019917%2CJ_11711801%2CJ_10162899%2CJ_11081695%2CJ_12114139%2CJ_12010088%2CJ_12161302%2CJ_11779454%2CJ_11939717%2CJ_12026957%2CJ_12184621%2CJ_12115244%2CJ_11930113%2CJ_10937943%2CJ_12192773%2CJ_12073030%2CJ_12098764%2CJ_11138599%2CJ_11165561%2CJ_11920855%2CJ_11682924%2CJ_11682923%2CJ_11892139&pduid=1523432585886562677791
#             skuid = book.xpath('./@data-sku').extract_first()
#             # print(skuid)
#             pduid = '&pduid=1523432585886562677791'
#             print(item)
#             # 再次发送请求，获取价格信息
#             if skuid is not None:
#                 url = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuid + pduid
#                 yield scrapy.Request(
#                     url,
#                     callback=self.parse_price,
#                     meta={'meta2': item}
#                 )
#
#     # 解析价格
#     def parse_price(self,response):
#         item = response.meta['meta2']
#         data = json.loads(response.body)
#         print(data)
#         item['price'] = data[0]['op']
#         # print (item)
#         yield item


class BookSpider(RedisSpider):
    name = 'jdbook'
    allowed_domains = ['hongniang.com',]
    # start_urls = ['https://book.jd.com/booksort.html']
    # 3------定义redis_key
    redis_key = 'jdbooks:start_urls'

    def parse(self, response):
        big_list = response.xpath('/html/body/div[4]/div[3]/div[1]/ul/li')
        print('列表', len(big_list))
        item = JdRedisItem()
        for big in big_list:
            item['pic'] = big.xpath('./div[1]/a/img/@src').extract_first()
            item['name'] = big.xpath('./div[2]/a/text()').extract_first()
            item['age'] = big.xpath('./div[3]/span[1]/text()').extract_first()
            item['place'] = big.xpath('./div[3]/span[2]/text()').extract_first()
            item['span'] = big.xpath('./div[3]/span[3]/text()').extract_first()
            item['height'] = big.xpath('./div[3]/span[4]/text()').extract_first()
            item['thought'] = big.xpath('./div[4]/text()').extract_first()
            yield item
            # scrapy runspider jdbook.py
            # lpush jdbooks:start_urls http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=1&province=0&city=0&marriage=1&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0














