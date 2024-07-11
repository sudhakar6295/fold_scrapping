# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fold_scrape.models import Image,Product
import logging



class FoldScrapePipeline:
    def  __init__(self):

        self.logger = logging.getLogger('scrapy.pipelines')
        engine = create_engine('mariadb+mariadbconnector://fold:XLqV6yPnwklZvNVL@localhost/fold')
        #engine = create_engine('mysql://root:sudhakar@localhost/fold')
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        # Create a session
        session = self.Session()
        try:
            main_image_url = item['images'][0].split('/')[-1]
        except Exception as e:
            main_image_url = None
        try:
            # Query the database for the record you want to update
            record = session.query(Product).filter_by(sku=item['sku']).first()

            # Update the record if found
            if record:
                record.price = item['price']
                record.name = item['name']
                record.category = item['category']
                record.description = item['description']
                record.url = item['url']
                record.tube_diameter = item['tube_diameter']
                record.maximum_height = item['maximum_height']
                record.base = item['base']
                record.Size = item['Size']
                record.Weight = item['Weight']
                record.Capacity = item['Capacity']
                record.Material = item['Material']
                record.Non_slip_legs = item['Non_slip_legs']
                record.main_image_url = main_image_url
                record.color = item['color']
                record.Contains = item['Contains']
                record.stock = item['stock']
                record.original_price = item['original_price']
                record.Seat_Height = item['Seat_Height']
                record.Height = item['Height']
                record.Packing = item['Packing']
                record.Observations = item['Observations']
                record.Specification = item['Specification']
                # Commit the changes to the database
                try:
                    session.commit()
                except Exception as e:
                    self.logger.error(f'update failure{e}')
                spider.logger.info("Record updated successfully.")
            else:
                new_record = Product(
                sku = item['sku'],
                url = item['url'],
                name = item['name'],
                price = item['price'],
                description = item['description'],
                Size = item['Size'],
                Weight = item['Weight'],
                Capacity = item['Capacity'],
                Material = item['Material'],
                Non_slip_legs = item['Non_slip_legs'],
                category = item['category'],
                main_image_url = main_image_url,
                tube_diameter = item['tube_diameter'],
                maximum_height = item['maximum_height'],
                base = item['base'],
                color = item['color'],
                Contains = item['Contains'],
                original_price = item['original_price'],
                Seat_Height = item['Seat_Height'],
                Height = item['Height'],
                Packing = item['Packing'],
                stock = item['stock'],
                Observations = item['Observations'],
                Specification = item['Specification'],)
                
                # Add more columns and values as needed
                try:
                    # Add the new record to the session
                    session.add(new_record)
                    
                    # Commit the changes to the database
                    session.commit()
                except Exception as e:
                    self.logger.error(f'New failure{e}')
                spider.logger.info("New record created successfully.")
        except Exception as e:
            # Rollback the changes in case of an error
            session.rollback()
            spider.logger.error("Failed to update record:", e)
        

        images = item['images']
        try:
            for image in images:
                image_value = image.split('/')[-1]
                img_record = session.query(Image).filter_by(image_url = image_value).first()
                if not img_record:
                    image_record = Image(image_url = image_value, sku = item['sku'])
                    session.add(image_record)
                    session.commit()
                    spider.logger.info("Image record created successfully.")
                else:
                    img_record.image_url = image_value
                    session.add(img_record)
                    session.commit()
                    spider.logger.info("Image updated.")
        except Exception as e:
            session.rollback()
            spider.logger.error("Failed to create image record:", e)    
        finally:
            # Close the session
            session.close()
        

        return item

