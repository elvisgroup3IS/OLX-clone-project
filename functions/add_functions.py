"""
This module contains functions for handling the creation, 
recognition, and deletion of advertisements.
"""
from datetime import datetime
from typing import Type, Optional, Dict, Union
from functions.other_functions import load_from_json
import models

def add_recognize(ad:models.BaseAdd)->Optional[Type[models.BaseAdd]]:
    """
    Recognizes the subclass of an advertisement and returns an instance of the corresponding model.
    """
    add_id = ad.id

    key_to_model = {
        "Компютри": models.Computer,
        "Таблети": models.Tablet,
        "Телефони": models.Phone,
        "Аудио техника": models.AudioEquipment,
        "Телевизори": models.Television,
        "Домашна техника": models.HouseholdAppliance,
        "Дамско": models.WomenClothing,
        "Мъжко": models.MenClothing,
        "Автомобили": models.Car,
        "Мотоциклети": models.Motorcycle,
        "Пълно работно време": models.FullTime,
        "Непълно работно време": models.PartTime,
        "Работа от вкъщи": models.WorkFromHome,
        "Апартаменти": models.ApartmentAdd,
        "Къщи": models.HouseAdd,
        "Велосипеди": models.Bicycles,
        "Спортни съоражения": models.SportFacilities,
        "Фитнес и тренировки": models.Fitness,
    }

    ad_subtype = key_to_model.get(ad.subcategory_type)

    if ad_subtype:
        ad_subtype = ad_subtype.query.get(add_id)

    return ad_subtype


def create_add(form: Dict[str, Union[str, int]], current_user: models.User)-> Type[models.BaseAdd]:
    """
    Creates a new advertisement based on the form data and the current user.
    """
    ad_params = {
        'title': form['title'],
        'content': form['description'],
        'item_price': form['price'],
        'location': form['location'],
        'created_at': datetime.now().date(),
        'owner_id': current_user.id,
        'contact_name': current_user.name,
        'phone': form['phone'],
        'owner': current_user,
        'photo1': form['photo1'],
        'photo2': form['photo2'],
        'photo3': form['photo3'],
        'subcategory_type': form.get('subcategory'),
        'category_type': form.get('category'),
        'saves': 0,
        'condition':form.get('condition'),
        'delivery_action':form.get('delivery_action')
    }

    json_data=load_from_json()

    category_keys=json_data['categories']

    category = ad_params['category_type']

    if category == category_keys[0]:
        ad=create_electronic_ad(ad_params,form)
    elif category == category_keys[1]:
        ad=create_clothing_ad(ad_params,form)
    elif category == category_keys[2]:
        ad = create_vehicle_ad(ad_params,form)
    elif category == category_keys[3]:
        ad = create_work_ad(ad_params,form)
    elif category == category_keys[4]:
        ad = create_real_estate_ad(ad_params, form)
    elif category == category_keys[5]:
        ad = create_sport_ad(ad_params,form)

    return ad





def create_electronic_ad(ad_params: Dict[str, Union[str, int]],
                        form: Dict[str, Union[str, int]])-> Type[models.BaseAdd] :
    """
    Creates a new electronic advertisement based on the form data.
    """
    keys=['Компютри','Таблети','Телефони','Аудио техника','Телевизори','Домашна техника']

    if ad_params['subcategory_type'] == keys[0]:
        pc_type = form['type_PC']
        ad = models.Computer(**ad_params, pc_type=pc_type)

    elif ad_params['subcategory_type'] == keys[1]:
        reader_type = form['type_tablet']
        ad = models.Tablet(**ad_params, reader_type=reader_type)

    elif ad_params['subcategory_type'] == keys[2]:
        brand = form['Phones']
        ad = models.Phone(**ad_params, phone_brand=brand)

    elif ad_params['subcategory_type'] == keys[3]:
        audio_type = form['type_audio']
        ad = models.AudioEquipment(**ad_params, type=audio_type)

    elif ad_params['subcategory_type'] == keys[4]:
        inches = form['inches']
        ad = models.Television(**ad_params, inches=inches)

    elif ad_params['subcategory_type'] == keys[5]:
        house_appliance_type = form['type_house_hold_appliance']
        ad = models.HouseholdAppliance(**ad_params, house_appliance_type=house_appliance_type)

    return ad
def create_clothing_ad(ad_params: Dict[str, Union[str, int]],
                    form: Dict[str, Union[str, int]])-> Type[models.BaseAdd] :
    """
    Creates a new clothing advertisement based on the form data.
    """
    keys='Дамско','Мъжко'

    if ad_params['subcategory_type'] == keys[0]:
        women_clothing_type = form['women_clothing_type']
        ad = models.WomenClothing(**ad_params, women_clothing_type=women_clothing_type)

    elif ad_params['subcategory_type'] == keys[1]:
        men_clothing_type = form['men_clothing_type']
        ad = models.MenClothing(**ad_params, male_clothing_type=men_clothing_type)

    return ad

def create_real_estate_ad(ad_params,form)-> Type[models.BaseAdd] :
    """
    Creates a new real estate advertisement based on the form data.
    """
    square_meters = form['square_meters']
    construction_year = datetime.strptime(form['construction_year'], "%Y-%m-%d").date()
    furnishing = form['furnishing']
    heating = form['heating']
    sale_or_rent = form['sale_or_rent']
    keys='Апартаменти','Къщи'

    ad_params.update({
        'square_meters': square_meters,
        'furnishing': furnishing,
        'construction_year': construction_year,
        'heating': heating,
        'sale_or_rent': sale_or_rent,
    })

    if ad_params['subcategory_type'] == keys[0]:
        apartment_type = form['apartment_type']
        floor = form['floor']
        ad = models.ApartmentAdd(**ad_params, apartment_type=apartment_type, floor=floor)

    if ad_params['subcategory_type'] == keys[1]:
        house_height = form['house_height']
        ad = models.HouseAdd(**ad_params, floors_height=house_height)

    return ad


def create_work_ad(ad_params, form)-> Type[models.BaseAdd] :
    """
    Creates a new work-related advertisement based on the form data.
    """
    sector = form['work_sector']
    salary = form['salary']
    keys='Пълно работно време','Непълно работно време'

    if ad_params['subcategory_type'] == keys[0]:
        ad = models.FullTime(**ad_params, sector=sector, salary=salary)
    elif ad_params['subcategory_type'] == keys[1]:
        ad = models.PartTime(**ad_params, sector=sector, salary=salary)
    else :
        ad = models.WorkFromHome(**ad_params, sector=sector, salary=salary)

    return ad

def create_sport_ad(ad_params, form):
    """
    Creates a new sports-related advertisement based on the form data.
    """
    sport_type = form['sport_type']
    keys='Велосипеди',"Фитнес и тренировки","Спортни съоръжения"
    if ad_params['subcategory_type'] == keys[0]:
        wheels_inches = form["wheels_inches"]
        ad = models.Bicycles(**ad_params, sport_type=sport_type, wheels_inches=wheels_inches)
    if ad_params['subcategory_type'] == keys[1]:
        ad = models.Fitness(**ad_params, sport_type=sport_type)
    if ad_params['subcategory_type'] == keys[2]:
        ad = models.SportFacilities(**ad_params, sport_type=sport_type)


    return ad

def create_vehicle_ad(ad_params, form)-> Type[models.BaseAdd] :
    """
    Create a new vehicle advertisement based on the form dat
    """
    vehicle_brand = form['vehicle_brand']
    year = datetime.strptime(form['year'], "%Y-%m-%d").date()
    power = form['power']
    keys='Автомобили','Мотоциклети'

    ad_params.update({
        'vehicle_brand': vehicle_brand,
        'year': year,
        'power': power,
    })

    if ad_params['subcategory_type'] == keys[0]:
        coupe = form['coupe_type']
        model = form['car_model']
        engine = form['engine_type']
        transmission = form['transmission_type']

        ad_params.update({
            'coupe': coupe,
            'model': model,
            'engine': engine,
            'transmission': transmission,
        })

        ad = models.Car(**ad_params)

    if ad_params['subcategory_type'] == keys[1]:
        motor_type = form['motorcycle_type']
        ad = models.Motorcycle(**ad_params, motor_type=motor_type)

    return ad

def get_add_by_id(ad_id:int)->models.BaseAdd:
    """
    Retrieve an advertisement by its ID.
    """
    return models.db.session.query(models.BaseAdd).get(ad_id)

def delete_add(ad_id:int)->None:
    """
    Delete an advertisement based on its ID.
    """
    ad = get_add_by_id(ad_id)
    if ad:
        models.db.session.delete(ad)
        models.db.session.commit()
        print(f"Record with ID {ad_id} deleted successfully.")
    else:
        raise ValueError(f"Record with ID {ad_id} not found.")
