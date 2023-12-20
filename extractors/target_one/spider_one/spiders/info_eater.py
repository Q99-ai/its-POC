import scrapy
from spider_one.items import ArticleItem



'''

TARGETS:

gaming-page/
seguridad-page/
cloud-page/
inteligencia-artificial-page/
fintech-page/
conectividad-y-networking-page/

...


'''

targets = ['gaming-page','seguridad-page','cloud-page','inteligencia-artificial-page','fintech-page','conectividad-y-networking-pag']


class InfoEaterSpider(scrapy.Spider):
    name = "info_eater"
    allowed_domains = ["www.itsitio.com"]
    #page/page/2/
    start_urls = [f"https://www.itsitio.com/{targets[1]}/page/%d/"% i for i in range(1,10)]



    def parse(self, response):
        title_xpath = './/h2[@class="post-title"]/a/text()'
        date_xpath = './/span[@class="date meta-item tie-icon"]/text()'
        author_xpath = './/span[@class="meta-author"]/a/text()'
        url_xpath ='.//h2[@class="post-title"]/a/@href'
        
    
        # Extracción de los títulos
        for article in  response.xpath('//div[@class="post-details"]'):
            item = ArticleItem()
            
            item['title'] = article.xpath(title_xpath).get()
            item['date'] = article.xpath(date_xpath).get()
            item['author'] = article.xpath(author_xpath).get()
            item['url'] = article.xpath(url_xpath).get()
            
            if item['url']:
                request = scrapy.Request(item['url'], callback=self.parse_article)
                request.meta['item'] = item  # Pasar el item actual al siguiente método
                
                yield request       
            
            
            
    def parse_article(self, response):
        item = response.meta['item']
        
        for text in response.xpath('//*[@class="entry-content entry clearfix"]'):
            item['content'] = text.xpath('.//p').getall()
        
        

        yield item