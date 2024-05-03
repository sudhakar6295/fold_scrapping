# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fold_scrape.models import Image,Product


class FoldScrapePipeline:
    def  __init__(self):
        engine = create_engine('mariadb+mariadbconnector://fold:XLqV6yPnwklZvNVL@170.239.84.29:22222/fold')
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
       
        # Create a session
        session = self.Session()

        try:
            # Query the database for the record you want to update
            record = session.query(Product).filter_by(sku=item['sku']).first()

            # Update the record if found
            if record:
                record.price = item['price']
                record.name = item['name']
                # Commit the changes to the database
                session.commit()
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
                category = item['category'],)
                
                # Add more columns and values as needed
            
                # Add the new record to the session
                session.add(new_record)
                
                # Commit the changes to the database
                session.commit()
                spider.logger.info("New record created successfully.")
        except Exception as e:
            # Rollback the changes in case of an error
            session.rollback()
            spider.logger.error("Failed to update record:", e)
        

        images = item['images']
        try:
            for image in images:
                img_record = session.query(Image).filter_by(image_url=image).first()
                if not img_record:
                    image_record = Image(image_url = image, sku = item['sku'])
                    session.add(image_record)
                    session.commit()
                    spider.logger.info("Image record created successfully.")
        except Exception as e:
            session.rollback()
            spider.logger.error("Failed to create image record:", e)    
        finally:
            # Close the session
            session.close()
        

        return item

