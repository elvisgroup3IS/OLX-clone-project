"""
This module defines SQLAlchemy models for user authentication,
 advertisements, and related functionalities.
"""
from typing import Union
from typing import Type
from flask_login import UserMixin
from setup import db

class User(UserMixin, db.Model):
    """
    SQLAlchemy model representing user data.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    ads = db.relationship('BaseAdd', back_populates='owner',
                        lazy='dynamic', enable_typechecks=False)
    favorite_adds = db.relationship('BaseAdd', secondary='user_favorite_adds', backref='users')

    def is_limit_by_category(self,subcategory):
        """
        Checks if the number of advertisements in a given subcategory exceeds the limit.
        """
        category_ads=[ad for ad in self.ads if ad.subcategory_type == subcategory]
        return  len(category_ads) >= 5

    def add_favorite_advert(self, add: Union['BaseAdd', 'Computer', 'RealEstateAdd','Vehicle',
                            'ElectronicDevice', 'ClothingAdd']) -> None:
        """
        Adds an advertisement to the user's list of favorite advertisements.
        """
        self.favorite_adds.append(add)
        self.save_to_db()

    def add_advert(self, add: Type['BaseAdd']) -> None:
        """
        Adds an advertisement to the user's list of advertisements.
        """
        self.ads.append(add)
        self.save_to_db()

    def save_to_db(self) -> None:
        """
        Saves the user instance to the database.
        """
        db.session.add(self)
        db.session.commit()

class BaseAdd(db.Model):
    """
    SQLAlchemy model representing base advertisement data.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    item_price = db.Column(db.Float)
    location = db.Column(db.String(50))
    contact_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    photo1=db.Column(db.String(15))
    photo2=db.Column(db.String(15))
    photo3=db.Column(db.String(15))
    condition = db.Column(db.String(10))
    delivery_action = db.Column(db.String(20))
    created_at = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id',name='fk_owner_id'), nullable=False)
    owner = db.relationship('User', back_populates='ads',
                            primaryjoin='BaseAdd.owner_id == User.id',
                            foreign_keys='BaseAdd.owner_id')
    category_type=db.Column(db.String(15))
    subcategory_type=db.Column(db.String(15))
    saves=db.Column(db.Integer)

user_favorite_adds = db.Table(
    'user_favorite_adds',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('base_add_id', db.Integer, db.ForeignKey('base_add.id'), primary_key=True)
)


class Image(db.Model):
    """
    SQLAlchemy model representing Image data.
    """
    __tablename__='images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    add_id = db.Column(db.Integer, db.ForeignKey('base_add.id'))
    add = db.relationship('BaseAdd', backref='images_add')

class RealEstateAdd(BaseAdd):
    """
    SQLAlchemy model representing real estate advertisement data.
    """
    square_meters = db.Column(db.Integer)
    construction_year = db.Column(db.Date)
    furnishing = db.Column(db.String(50))
    heating = db.Column(db.String(50))
    sale_or_rent = db.Column(db.String(1))

class ApartmentAdd(RealEstateAdd):
    """
    SQLAlchemy model representing apartment advertisement data.
    """
    __tablename__ = 'apartment_adds'
    apartment_type = db.Column(db.String(50))
    floor = db.Column(db.Integer)

class HouseAdd(RealEstateAdd):
    """
    SQLAlchemy model representing house advertisement data.
    """
    __tablename__ = 'house_adds'
    floors_height = db.Column(db.Integer)

# Vehicles
class Vehicle(BaseAdd):
    """
    SQLAlchemy model representing vehicle advertisement data.
    """
    vehicle_brand = db.Column(db.String(100))
    year = db.Column(db.Date)
    power = db.Column(db.Integer)

class Car(Vehicle):
    """
    SQLAlchemy model representing car advertisement data.
    """
    __tablename__ = 'car_adds'
    coupe = db.Column(db.String(50))
    model = db.Column(db.String(50))
    engine = db.Column(db.String(50))
    transmission = db.Column(db.String(50))

class Motorcycle(Vehicle):
    """
    SQLAlchemy model representing motorcycle advertisement data.
    """
    __tablename__ = 'motorcycle_adds'
    motor_type = db.Column(db.String(100))

# Electronics
class ElectronicDevice(BaseAdd):
    """
    Base class for electronic devices advertisement data.
    """

class Computer(ElectronicDevice):
    """
    SQLAlchemy model representing computer advertisement data.
    """
    __tablename__ = 'computer'
    pc_type = db.Column(db.String(50))

class Tablet(ElectronicDevice):
    """
    SQLAlchemy model representing tablet advertisement data.
    """
    __tablename__ = 'tablet'
    reader_type = db.Column(db.String(50))

class Phone(ElectronicDevice):
    """
    SQLAlchemy model representing phone advertisement data.
    """
    __tablename__ = 'phone'
    phone_brand = db.Column(db.String(50))

class Television(ElectronicDevice):
    """
    SQLAlchemy model representing television advertisement data.
    """
    __tablename__ = 'television'
    inches=db.Column(db.Integer)

class AudioEquipment(ElectronicDevice):
    """
    SQLAlchemy model representing audio equipment advertisement data.
    """
    __tablename__ = 'audio_equipment'
    type = db.Column(db.String(50))

class HouseholdAppliance(ElectronicDevice):
    """
    SQLAlchemy model representing household appliance advertisement data.
    """
    __tablename__ = 'household_appliance'
    house_appliance_type = db.Column(db.String(50))

# Clothing
class ClothingAdd(BaseAdd):
    """
    SQLAlchemy model representing clothing advertisement data.
    """
    __tablename__ = 'clothing_add'

class MenClothing(ClothingAdd):
    """
    SQLAlchemy model representing men's clothing advertisement data.
    """
    __tablename__ = 'men_clothing'
    male_clothing_type = db.Column(db.String(50))

class WomenClothing(ClothingAdd):
    """
    SQLAlchemy model representing women's clothing advertisement data.
    """
    __tablename__ = 'women_clothing'
    women_clothing_type = db.Column(db.String(50))

# Work
class Work(BaseAdd):
    """
    SQLAlchemy model representing work-related advertisement data.
    """
    sector=db.Column(db.String(50))
    salary=db.Column(db.Double)

class FullTime(Work):
    """
    SQLAlchemy model representing full-time work advertisement data.
    """
    __tablename__ = 'full_time'

class PartTime(Work):
    """
    SQLAlchemy model representing part-time work advertisement data.
    """
    __tablename__ = 'part_time'

class WorkFromHome(Work):
    """
    SQLAlchemy model representing work-from-home advertisement data.
    """
    __tablename__ = 'home_work'

# Sport
class SportAdd(BaseAdd):
    """
    Base class for sports-related advertisement data.
    """
    sport_type=db.Column(db.String(20))

class Fitness(SportAdd):
    """
    SQLAlchemy model representing fitness-related advertisement data.
    """
    __tablename__='fitness_add'

class SportFacilities(SportAdd):
    """
    SQLAlchemy model representing sport facilities-related advertisement data.
    """
    __tablename__='sport_facilities_add'

class Bicycles(SportAdd):
    """
    SQLAlchemy model representing bicycles advertisement data.
    """
    __tablename__='bicycles_add'
    wheels_inches = db.Column(db.Integer)
