import scrapy

class ProductSpider(scrapy.Spider):
    name = 'aio_spider'
    start_urls = ['https://villman.com/Category/Desktop-PCs']

    def start_requests(self):
        headers = {
            'Referer': 'https://www.google.com/'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        # Extracting product details
        for product in response.css('div.prod_contain'):
            yield {
                'product_name': product.css('div.prod_name a.prod_link::text').get(),
                'product_link': product.css('a.prod_link::attr(href)').get(),
                'product_desc': product.css('div.prod_desc::text').get(),
                'product_price': product.css('div.prod_price::text').get(),
            }
        
        # Handling pagination
        current_page = response.css('div.paging_num span.current::text').get()
        next_page = response.css(f'div.paging_num a[href="/Category/Desktop-PCs/{int(current_page) + 1}"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
