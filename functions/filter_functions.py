"""
This module contains functions for filtering and fetching advertisements.
"""
from typing import  Optional ,List
from sqlalchemy import or_
from functions.other_functions import load_from_json
import models

def fetch_ads(category: Optional[str] = None, subcategory: Optional[str] = None)->models.BaseAdd:
    """
    Fetches advertisements based on the provided category and/or subcategory.
    """
    if subcategory :
        ads = models.db.session.query(models.BaseAdd).filter_by(subcategory_type=subcategory)
    elif category :
        ads = models.db.session.query(models.BaseAdd).filter_by(category_type=category)
    else :
        ads = models.BaseAdd.query.all()

    return ads

def price_filter(ads:models.BaseAdd,max_price:str)->List[models.BaseAdd]:
    """
    Filters advertisements based on the maximum price.
    """
    return [ad for ad in ads if ad.item_price < float(max_price)]

def location_filter(ads:models.BaseAdd,city:str)->List[models.BaseAdd]:
    """
    Filters advertisements based on the specified city.
    """
    return [ad for ad in ads if ad.location == city]

def category_filter(subcategory=None, category=None,current_user=None):
    """
    Filters advertisements based on category, subcategory, or user-related criteria.
    """
    subcategories=None
    selected_category=None
    json_data=load_from_json()
    user_key,favorite_user_key='user_ads','favorite_user_ads'
    if category == user_key:
        all_ads = current_user.ads
        message="Вашите обяви"
    elif category == favorite_user_key:
        all_ads = current_user.favorite_adds
        message="Вашите любими обяви"
    elif category or subcategory :
        message=f"Обяви в категория : {category} "
        json_data=load_from_json()
        subcategories=json_data['subcategories']
        selected_category=category
        if subcategory:
            all_ads = fetch_ads(subcategory=subcategory)
            message=f"Обяви в подкатегория : {subcategory} "
        else:
            message=f"Обяви в категория : {category} "
            all_ads = fetch_ads(category=category)
    else:
        message="Всички обяви"
        all_ads = models.BaseAdd.query.all()
    cities=json_data['cities']

    return {'message' : message ,'all_ads' : all_ads, 'selected_category' :
             selected_category,'is_selected_category':selected_category,
             'subcategories' : subcategories,'cities':cities}

def  search_filter(search_query:str)->models.BaseAdd:
    """
    Filters advertisements based on a search query.
    """
    return  models.BaseAdd.query.filter(or_(models.BaseAdd.title.ilike(f"%{search_query}%"),
                                    models.BaseAdd.content.ilike(f"%{search_query}%"))).all()
