from setup import db,app
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, JSON
from hashlib import sha256
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin
from typing import Union


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True) 
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    ads = db.relationship('BaseAdd', back_populates='owner', lazy='dynamic', enable_typechecks=False)
    favorite_adds = db.relationship('BaseAdd', secondary='user_favorite_adds', backref='users')


    def add_favorite_advert(self, add: Union['BaseAdd', 'Computer', 'RealEstateAdd', 'Vehicle', 'ElectronicDevice', 'ClothingAdd', ...]) -> None:
        self.favorite_adds.append(add)
        self.save_to_db()

    def add_advert(self, add: Union['BaseAdd', 'Computer', 'RealEstateAdd', 'Vehicle', 'ElectronicDevice', 'ClothingAdd', ...]) -> None:
        self.ads.append(add)
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

class BaseAdd(db.Model):
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
    owner = db.relationship('User', back_populates='ads', primaryjoin='BaseAdd.owner_id == User.id', foreign_keys='BaseAdd.owner_id')
    category_type=db.Column(db.String(15))
    subcategory_type=db.Column(db.String(15))
    saves=db.Column(db.Integer)

user_favorite_adds = db.Table(
    'user_favorite_adds',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('base_add_id', db.Integer, db.ForeignKey('base_add.id'), primary_key=True)
)


engine = create_engine('sqlite:///app.db')

def save_user(user: User) -> None:
    db.session.add(user)
    db.session.commit()
    db.session.close()

def search_for_user(email: str) -> User:
    user = db.session.query(User).filter((User.email == email)).first()
    db.session.close()
    return user


class Image(db.Model):
    __tablename__='images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    add_id = db.Column(db.Integer, db.ForeignKey('base_add.id'))
    add = db.relationship('BaseAdd', backref='images_add')


# Недвижими имоти
class RealEstateAdd(BaseAdd):
    square_meters = db.Column(db.Integer)
    construction_year = db.Column(db.Date)
    furnishing = db.Column(db.String(50))
    heating = db.Column(db.String(50))
    sale_or_rent = db.Column(db.String(1))

class ApartmentAdd(RealEstateAdd):
    __tablename__ = 'apartment_adds'
    apartment_type = db.Column(db.String(50))
    floor = db.Column(db.Integer)

class HouseAdd(RealEstateAdd):
    __tablename__ = 'house_adds'
    floors_height = db.Column(db.Integer)

# Превозни средства
class Vehicle(BaseAdd):
    vehicle_brand = db.Column(db.String(100))
    year = db.Column(db.Date)
    power = db.Column(db.Integer)

class Car(Vehicle):
    __tablename__ = 'car_adds'
    coupe = db.Column(db.String(50))
    model = db.Column(db.String(50))
    engine = db.Column(db.String(50))
    transmission = db.Column(db.String(50))

class Motorcycle(Vehicle):
    __tablename__ = 'motorcycle_adds'
    motor_type = db.Column(db.String(100))

# Електроника
class ElectronicDevice(BaseAdd):
    pass
 
class Computer(ElectronicDevice):
    
    __tablename__ = 'computer'
    pc_type = db.Column(db.String(50))

class Tablet(ElectronicDevice):
    __tablename__ = 'tablet'
    reader_type = db.Column(db.String(50))

class Phone(ElectronicDevice):
    __tablename__ = 'phone'
    phone_brand = db.Column(db.String(50))

class Television(ElectronicDevice):
    __tablename__ = 'television'
    inches=db.Column(db.Integer)

class AudioEquipment(ElectronicDevice):
    __tablename__ = 'audio_equipment'
    type = db.Column(db.String(50))

class HouseholdAppliance(ElectronicDevice):
    __tablename__ = 'household_appliance'
    house_appliance_type = db.Column(db.String(50))

# Облекло
class ClothingAdd(BaseAdd):
    __tablename__ = 'clothing_add'

class MenClothing(ClothingAdd):
    __tablename__ = 'men_clothing'
    male_clothing_type = db.Column(db.String(50))

class WomenClothing(ClothingAdd):
    __tablename__ = 'women_clothing'
    women_clothing_type = db.Column(db.String(50))


class Work(BaseAdd):
    sector=db.Column(db.String(50))
    salary=db.Column(db.Double)

class FullTime(Work):
    __tablename__ = 'full_time'
    pass

class PartTime(Work):
    __tablename__ = 'part_time'
    pass

class WorkFromHome(Work):
    __tablename__ = 'home_work'
    pass   

class SportAdd(BaseAdd):
    sport_type=db.Column(db.String(20))

class Fitness(SportAdd):
    __tablename__='fitness_add'

class SportFacilities(SportAdd):
    __tablename__='sport_facilities_add'

class Bicycles(SportAdd):
    __tablename__='bicycles_add'
    wheels_inches = db.Column(db.Integer)