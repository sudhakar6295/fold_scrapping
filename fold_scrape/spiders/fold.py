import scrapy,json
import os,requests
import logging

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
        products_url = response.xpath('//*[@class="grid__item"]')
        for products in products_url:
            product_url = products.xpath('.//*[@class="bs-collection__product-title"]/a/@href').get()
            original_price = products.xpath('.//*[@class="bs-collection__product-old-price"]/text()[contains(.,"$")]').get()
            abs_url = "https://www.fold.cl"+product_url
            
            yield scrapy.Request(abs_url, callback=self.parse_product,meta={'original_price':original_price})

        #Pagination
        next_page_url = response.xpath('//li[@class="page-item active"]/following-sibling::li/a/@href').get()
        if next_page_url:
            next_abs_url = "https://www.fold.cl"+next_page_url
            yield scrapy.Request(next_abs_url, callback=self.parse_category)
    
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

        try:

            original_price = response.meta.get('original_price')
            if original_price:
                # Remove '$' and '.' from the string
                try:
                    original_price = original_price.replace('$', '').replace('.', '')
                    original_price = int(original_price)
                except:
                    original_price = None

            json_str = response.xpath('//*[@data-schema="Product"]/text()').get()
            json_data = json.loads(json_str)

            name = response.xpath('//*[@class="bs-product__title"]/text()').extract_first()
            #original_price = response.xpath('//*[@class="bs-product__original-price"]//text()[contains(.,"$")]').get()
            price = response.xpath('//*[@class="bs-product__final-price"]/text()').extract()  
            description = json_data.get('description')
            sku = json_data.get('sku')
            price = json_data.get('offers').get('price')
            try:
                json_str1 = response.xpath(".//script[contains(.,'\"stock\":')]/text()").get()
                if json_str1:
                    json_str1 = json_str1.strip()
                json_datas1 = json.loads(json_str1)

                stock = None
                for json_data1 in json_datas1:
                    stock = json_data1.get('stock')[0].get('quantity')
                    if stock:
                        break
            except Exception as e:
                stock = None

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
            if not Size:
                Size = response.xpath('//td[contains(.,"Tamaño")]/following-sibling::td/text()').get()
            if not Size:
                Size = response.xpath('//li[contains(.,"Talla")]/text()').get()

            Weight = response.xpath('//p//text()[contains(.,"Peso:")]').get()
            if not Weight:
                Weight = response.xpath('//strong[contains(.,"Peso")]/following-sibling::text()').get()
            if not Weight:
                Weight = response.xpath('//li[contains(.,"Peso")]/text()').get()
            if not Weight:
                Weight = response.xpath('//td[contains(.,"Peso:")]/following-sibling::td/text()').get()
            if not Weight:
                Weight = response.xpath('//p//text()[contains(.,"Rellena:")]').get()



            Capacity = response.xpath('//p//text()[contains(.,"Capacidad:")]').get()
            if not Capacity:
                Capacity = response.xpath('//strong[contains(.,"Capacidad")]/following-sibling::text()').get()
            color = response.xpath('//p//text()[contains(.,"Color:")]').get()
            if not color:
                color = response.xpath('//strong[contains(.,"Color")]/following-sibling::text()').get()
            if not color:
                color = response.xpath('//p//text()[contains(.,"Colores")]').get()

            Material = response.xpath('//p//text()[contains(.,"Material:")]').get()
            if not Material:
                Material = response.xpath('//strong[contains(.,"Material")]/following-sibling::text()').get()
            if not Material:
                Material = response.xpath('//td[contains(.,"Material")]/following-sibling::td//text()').get()
            if not Material:
                Material = response.xpath('//td[contains(.,"Material:")]/following-sibling::td/text()').get()

            Height = response.xpath('//strong[contains(.,"Altura")]/following-sibling::text()').get()
            if not Height:
                Height = response.xpath('//p//text()[contains(.,"Altura:")]').get()



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
            if not Base:
                Base = response.xpath('//li[contains(.,"Bases :")]/text()').get()

            Seat_Height = response.xpath('//li[contains(.,"Altura De Asiento")]/text()').get()

            Contains = response.xpath('//td[contains(.,"Contiene")]/following-sibling::td//text()').get()

            Packing = response.xpath('//td[contains(.,"Empaque:")]/following-sibling::td/text()').get()

            #stock =  response.xpath('//*[@class="bs-collection__stock"]/text()').get()
            Observations  = response.xpath('//p//text()[contains(.,"Observaciones")]').get()


            images = json_data.get('image')

            category = response.xpath('//*[@class="breadcrumb-item"]/a//text()').extract()[-1]
            if category:
                category = category.strip()
            self.save_image(images)

            spec_rows = response.xpath('//*[@data-parent="#bs-product-description"]//table//tr')
            spec = {}
            for spec_row in spec_rows:
                spec_values = spec_row.xpath('.//td/text()').extract()
                if len(spec_values) == 2:
                    spec[spec_values[0].replace(':','')] = spec_values[-1]

            spec_rows1 = response.xpath('//*[@data-parent="#bs-product-description"]//p')

            for spec_row1 in spec_rows1:
                spec_value1 = spec_row1.xpath('.//text()').get()
                if spec_value1 and ':' in spec_value1:
                    spec_values1 = spec_value1.split(':')
                    if len(spec_values1) == 2:
                        spec[spec_values1[0].replace(':','')] = spec_values1[-1]

            item = {
                'url': response.url,
                'name': name,
                'price': price,
                'original_price': original_price,   
                'description': description,
                'sku': sku,
                'Size': clean_text(Size),
                'Weight': clean_text(Weight),
                'Capacity': clean_text(Capacity),
                'Material': clean_text(Material),
                'Non_slip_legs': clean_text(Non_slip_legs),
                'Contains':clean_text(Contains),
                'images': images,
                'category': category,
                'tube_diameter':clean_text(tube_diameter),
                'maximum_height':clean_text(maximum_height),
                'base':clean_text(Base),
                'color':clean_text(color),
                'Seat_Height':clean_text(Seat_Height),
                'stock':clean_text(stock),
                'Height':clean_text(Height),
                'Packing':clean_text(Packing),
                'Observations':clean_text(Observations),
                'Specification':spec

                
            }    

            yield item
        except Exception as e:
            self.logger.error(f"Scrapping error{e}")