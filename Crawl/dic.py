# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dictionary.items import DictionaryItem


class DictionarySpider(CrawlSpider):
    name = 'dic'
    allowed_domains = ['bbc.co.uk']
    start_urls = ['http://www.bbc.co.uk/food/ingredients/by/letter/a']

    rules = (   
        Rule(LinkExtractor(allow=(r'/food/ingredients/by/letter/')), callback='parse_item', follow=True),
        # Rule(LinkExtractor(deny_domains=["reviews"])),

        # Rule(SgmlLinkExtractor(allow=('recipe\.php', ), deny=('review\.php', )),follow = True),
    )

    def parse_item(self, response):
        i = DictionaryItem()
        i['name'] = response.xpath('//img[@width=\'111\']/@alt').extract()
        # i['author'] = response.xpath('//ul/li/h4/text()').extract_first()
        # i['servings'] = response.xpath('//meta[@id=\'metaRecipeServings\']/@content').extract_first()
        # i['rating'] = response.xpath('//ol/li/h4/text()').extract_first()
        # i['url'] = response.url

        # i['images'] = response.xpath('//meta[@property=\'og:image\']/@content').extract_first()

        # i['directions'] = response.xpath('//ol[@itemprop="recipeInstructions"]/li/span/text()').extract()
        # i['ingredients'] = response.xpath('//li[@class="checkList__line"]/label/span[@itemprop="ingredients"]/text()').extract()

        print i['name']
        return i







        # columns = response.xpath('//ul[contains(@class,"ingredient-wrap")]')
        # ingredients_all = {}
        # for column in columns:
        #     ingredients = column.xpath('./li[@id="liIngredient"]')
        #     for ingredient in ingredients:
        #         ingredients_all[ingredient.xpath('.//span[@id="lblIngName"]/text()').extract_first()] = \
        #             ingredient.xpath('.//span[@id="lblIngAmount"]/text()').extract_first()

        # i['ingredients'] = ingredients_all

        # directions = response.xpath('//div[@class="directions"]//li/span')
        # directions_all = {}
        # for index, direction in enumerate(directions):
        #     directions_all[index] = direction.xpath('./text()').extract_first()
        
        
        

        

 