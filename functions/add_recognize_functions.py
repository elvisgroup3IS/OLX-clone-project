import models

def add_recognize(ad):
    add_id=ad.id

    if ad.subcategory_type == "Компютри":
        ad_subtype = models.Computer.query.get(add_id) 
    elif ad.subcategory_type == "Таблети":
        ad_subtype = models.Tablet.query.get(add_id)
    elif ad.subcategory_type == "Телефони":
        ad_subtype = models.Phone.query.get(add_id) 
    elif ad.subcategory_type == "Аудио техника":
        ad_subtype = models.AudioEquipment.query.get(add_id)
    elif ad.subcategory_type == "Телевизори":
        ad_subtype = models.Television.query.get(add_id)
    elif ad.subcategory_type == "Домашна техника":
        ad_subtype = models.HouseholdAppliance.query.get(add_id) 
    elif ad.subcategory_type == "Дамско":
        ad_subtype = models.WomenClothing.query.get(add_id)
    elif ad.subcategory_type == "Мъжко":
        ad_subtype = models.MenClothing.query.get(add_id)
    elif ad.subcategory_type == "Автомобили":
        ad_subtype = models.Car.query.get(add_id)
    elif ad.subcategory_type == "Мотоциклети":
        ad_subtype = models.Motorcycle.query.get(add_id)
    elif ad.subcategory_type == "Пълно работно време":
        ad_subtype = models.FullTime.query.get(add_id)
    elif ad.subcategory_type == "Непълно работно време":
        ad_subtype = models.PartTime.query.get(add_id)
    elif ad.subcategory_type == "Работа от вкъщи":
        ad_subtype = models.WorkFromHome.query.get(add_id)
    elif ad.subcategory_type == "Апартаменти за продажба":
        ad_subtype = models.ApartmentAdd.query.get(add_id)
    elif ad.subcategory_type == "Къщи за продажба":
        ad_subtype = models.HouseAdd.query.get(add_id)
    elif ad.subcategory_type == "Велосипеди":
        ad_subtype = models.Bicycles.query.get(add_id)

    return ad_subtype
