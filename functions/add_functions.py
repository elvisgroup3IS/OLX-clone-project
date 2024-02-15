import models
from datetime import  datetime

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

def create_add(request,current_user):
    title=request.form['title']
    photos = [request.form[f'photo{i}'] for i in range(1, 4)]
    description=request.form['description']
    price=request.form['price']
    location=request.form['location']
    phone=request.form['phone']
    subcategory = request.form.get('subcategory')
    category = request.form.get('category')
    saves=0
    ad_params = {
        'title': title,
        'content': description,
        'item_price': price,
        'location': location,
        'created_at': datetime.now().date(),
        'owner_id': current_user.id,
        'contact_name': current_user.name,
        'phone': phone,
        'owner': current_user,
        'photo1': photos[0],
        'photo2': photos[1],
        'photo3': photos[2],
        'subcategory_type': subcategory,
        'category_type': category,
        'saves': saves,
    }
    if(subcategory == 'Компютри'):
        type_pc=request.form['type_PC']
        ad = models.Computer(**ad_params,pc_type=type_pc)
    elif(subcategory == 'Таблети'):
        reader_type=request.form['type_tablet']
        ad = models.Tablet(**ad_params,reader_type=reader_type)
    elif subcategory == 'Телефони':
        brand = request.form['brand']
        ad = models.Phone(**ad_params,phone_brand=brand) 
    elif subcategory == 'Аудио техника':
        type = request.form['brand']
        ad = models.AudioEquipment(**ad_params,type=type) 
    elif subcategory == 'Телевизори':
        inches = request.form['brand']
        ad = models.Television(**ad_params, inches=inches) 
    elif subcategory == 'Домашна техника':
        house_appliance_type = request.form['house_appliance_type']
        ad = models.HouseholdAppliance(**ad_params, house_appliance_type=house_appliance_type) 
    elif subcategory == 'Дамско':
        women_clothing_type = request.form['women_clothing_type']
        ad = models.WomenClothing(**ad_params, women_clothing_type=women_clothing_type) 
    elif subcategory == 'Мъжко':
        men_clothing_type = request.form['men_clothing_type']
        ad = models.MenClothing(**ad_params,male_clothing_type=men_clothing_type) 
    elif category == 'Работа':
        sector=request.form['work_sector']
        salary =request.form['salary']
        if subcategory == 'Пълно работно време':
            ad = models.FullTime(**ad_params, sector=sector,salary=salary) 
        elif subcategory == 'Непълно работно време':
            ad = models.PartTime(**ad_params, sector=sector,salary=salary) 
        else :
            ad = models.WorkFromHome(**ad_params, sector=sector,salary=salary) 
    elif category == 'Недвижими имоти':
        square_meters = request.form['square_meters']
        construction_year = request.form['construction_year']
        construction_year = datetime.strptime(construction_year, "%Y-%m-%d").date()
        furnishing = request.form['furnishing']
        heating = request.form['heating']
        sale_or_rent = request.form['sale_or_rent']
        ad_params.update({ 
            'square_meters': square_meters,
            'furnishing': furnishing,
            'construction_year': construction_year,
            'heating': heating,
            'sale_or_rent': sale_or_rent,
        })
        if subcategory == 'Апартаменти':
            apartment_type = request.form['apartment_type']
            floor = request.form['floor']
            ad = models.ApartmentAdd(**ad_params, apartment_type=apartment_type,floor=floor)
        if subcategory == 'Къщи':
            house_height = request.form['house_height']
            ad = models.HouseAdd(**ad_params, floors_height=house_height)
    elif category == 'Спорт':
        sport_type=request.form['sport_type']
        if subcategory == 'Велосипеди':
            wheels_inches = request.form["wheels_inches"]
            ad = models.Bicycles(**ad_params,sport_type=sport_type , wheels_inches=wheels_inches)
        else :
            ad = models.SportAdd(**ad_params,sport_type=sport_type)
    elif category == 'Превозни средства':
        vehicle_brand = request.form['vehicle_brand']
        year = request.form['year']
        print(year)
        year = datetime.strptime(year, "%Y-%m-%d").date()
        
        power = request.form['power']
        ad_params.update({ 
            'vehicle_brand': vehicle_brand ,
            'year': year,
            'power': power,
        })
        if subcategory == 'Автомобили':
            coupe = request.form['coupe_type']
            model = request.form['car_model']
            engine = request.form['engine_type']
            transmission = request.form['transmission_type']
            ad_params.update({ 
                'coupe': coupe ,
                'model': model,
                'engine': engine,
                'transmission': transmission,
            })
            ad = models.Car(**ad_params)
        else :
            motor_type=request.form['motorcycle_type']
            ad = models.Motorcycle(**ad_params,motor_type=motor_type)

    return ad

def get_add_by_id(ad_id):
    return models.db.session.query(models.BaseAdd).get(ad_id)

def delete_add(add_id):
    add = get_add_by_id(add_id)
    if add:
        models.db.session.delete(add)
        models.db.session.commit()
        print(f"Record with ID {add_id} deleted successfully.")
    else:
        raise ValueError(f"Record with ID {add_id} not found.")