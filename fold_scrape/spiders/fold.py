import scrapy,json
import os,requests

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
    
    def check_file_in_folder(self,folder, file):
        # Check if the file exists in the given folder
        if os.path.exists(os.path.join(folder,file)):
            return True
        else:
            return False

    def save_image(self, temp_images,folder="Image"):
        for url in temp_images:
            abs_url = url
            if not os.path.exists(folder):
                        os.makedirs(folder)
            file_exits = self.check_file_in_folder(folder, url)
            if  file_exits:
                continue
            file_name = url.split('/')[-1]
            filepath = os.path.join(folder,file_name)
            
            response = requests.get(abs_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                    print(f"Image saved as {filepath}")
            else:
                print(f"Failed to download image from {filepath}")   
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
 

        Size = response.xpath('//p//text()[contains(.,"Tamaño:")]').get()
        if not Size:
            Size = response.xpath('//strong[contains(.,"Tamaño")]/following-sibling::text()').get()
        Weight = response.xpath('//p//text()[contains(.,"Peso:")]').get()
        if not Weight:
            Weight = response.xpath('//strong[contains(.,"Peso")]/following-sibling::text()').get()
        Capacity = response.xpath('//p//text()[contains(.,"Capacidad:")]').get()
        if not Capacity:
            Capacity = response.xpath('//strong[contains(.,"Capacidad")]/following-sibling::text()').get()
        color = response.xpath('//p//text()[contains(.,"Color:")]').get()
        if not color:
            color = response.xpath('//strong[contains(.,"Color")]/following-sibling::text()').get()
        Material = response.xpath('//p//text()[contains(.,"Material:")]').get()
        if not Material:
            Material = response.xpath('//strong[contains(.,"Material")]/following-sibling::text()').get()
        Non_slip_legs = response.xpath('//p//text()[contains(.,"Non-slip legs:")]').get()
        if not Non_slip_legs:    
            Non_slip_legs = response.xpath('//strong[contains(.,"Non-slip legs")]/following-sibling::text()').get()
        tube_diameter = response.xpath('//p//text()[contains(.,"Diámetro Tubo:")]').get()
        if not tube_diameter:    
            tube_diameter = response.xpath('//strong[contains(.,"Diámetro Tubo")]/following-sibling::text()').get()
        maximum_height  = response.xpath('//p//text()[contains(.,"Altura MáximaBase:")]').get()
        if not maximum_height:    
            maximum_height = response.xpath('//strong[contains(.,"Altura Máxima")]/following-sibling::text()').get()
        Base= response.xpath('//p//text()[contains(.,"Base:")]').get()
        if not Base:    
            Base = response.xpath('//strong[contains(.,"Base")]/following-sibling::text()').get()

        images = json_data.get('image')

        category = response.xpath('//*[@class="breadcrumb-item"]/a//text()').extract()[-1]
        if category:
            category = category.strip()
        self.save_image(images)
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
            'tube_diameter':clean_text(tube_diameter),
            'maximum_height':clean_text(maximum_height),
            'base':clean_text(Base),
            'color':clean_text(color)
            
        }    

        yield item