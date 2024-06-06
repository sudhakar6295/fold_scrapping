from sqlalchemy import create_engine, Column, String, ForeignKey, Integer,DECIMAL,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    sku = Column(String(50), primary_key=True)
    url = Column(String(255))
    name = Column(String(255))
    price = Column(DECIMAL(10, 2))
    original_price = Column(DECIMAL(10, 2))
    description = Column(Text)
    Size = Column(String(50))
    Weight = Column(String(50))
    tube_diameter = Column(String(50))
    maximum_height = Column(String(50))
    base = Column(String(50))
    Capacity = Column(String(50))
    Material = Column(String(100))
    Non_slip_legs = Column(String(5))
    category = Column(String(100))
    LastScrappeddate = Column(DateTime, onupdate=func.now())
    Updateddate = Column(DateTime, onupdate=func.now())
    Createddate = Column(DateTime, default=func.now())
    Status = Column(String(50))
    color = Column(String(50))
    main_image_url = Column(String(255))
    Seat_Height = Column(String(50))
    Contains = Column(Text)

class Image(Base):
    __tablename__ = 'images'

    image_url = Column(String(255), primary_key=True)
    sku = Column(String(50), ForeignKey('product.sku'))
  

# Define your database connection
engine = create_engine('mariadb+mariadbconnector://fold:XLqV6yPnwklZvNVL@localhost/fold')
#engine = create_engine("mysql+pymysql://fold:XLqV6yPnwklZvNVL@170.239.84.29:22222/fold?charset=utf8mb4")


# Create the tables
Base.metadata.create_all(engine)