import scrapy,json


class FoldSpider(scrapy.Spider):
    name = "fold"
    #allowed_domains = ["www.fold.cl"]
    start_urls = ["https://www.fold.cl/"]

    def parse(self, response):
        categorys=response.xpath('//*[@class="bs-menu__lv2"]/@href').extract()
        for category in categorys:
            abs_url = "https://www.fold.cl"+category
            
            yield scrapy.Request(abs_url, callback=self.parse_category)

    def parse_category(self, response):
        products_url = response.xpath('//*[@class="bs-collection__product-title"]/a/@href').extract()
        for product_url in products_url:
            abs_url = "https://www.fold.cl"+product_url
            
            yield scrapy.Request(abs_url, callback=self.parse_product)
    
    def parse_product(self, response):

        
        json_str = response.xpath('//*[@data-schema="Product"]/text()').get()
        json_data = json.loads(json_str)

        name = response.xpath('//*[@class="bs-product__title"]/text()').extract_first()
        price = response.xpath('//*[@class="bs-product__final-price"]/text()').extract()  
        description = json_data.get('description')
        sku = json_data.get('sku')
        price = json_data.get('offers').get('price')

        def clean_text(text):
            try:
                if text:
                    text = text.split(':')[-1].strip()
                return text
            except:
                return text
 

        Size = response.xpath('//p//text()[contains(.,"Size:")]').get()
        Weight = response.xpath('//p//text()[contains(.,"Weight:")]').get()
        Capacity = response.xpath('//p//text()[contains(.,"Capacity:")]').get()
        Material = response.xpath('//p//text()[contains(.,"Material:")]').get()
        Non_slip_legs = response.xpath('//p//text()[contains(.,"Non-slip legs:")]').get()
        images = json_data.get('image')
        category = response.xpath('//*[@class="breadcrumb-item"]/a//text()').extract()[-1]

        item = {
            'url': response.url,
            'name': name,
            'price': price,
            'description': description,
            'sku': sku,
            'Size': clean_text(Size),
            'Weight': clean_text(Weight),
            'Capacity': clean_text(Capacity),
            'Material': clean_text(Material),
            'Non_slip_legs': clean_text(Non_slip_legs),
            'images': images,
            'category': category,
            
        }    

        yield item