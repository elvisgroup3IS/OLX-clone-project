import models
from functions.other_functions import load_from_json

def fetch_ads(category=None,subcategory=None):
    if subcategory :
        return models.db.session.query(models.BaseAdd).filter_by(subcategory_type=subcategory)
    elif category :
        return models.db.session.query(models.BaseAdd).filter_by(category_type=category)
    else :
        return models.BaseAdd.query.all()
    
def price_filter(ads,max_price):
    return [ad for ad in ads if ad.item_price < float(max_price)]

def category_filter(subcategory=None,category=None,current_user=None):
    subcategories=None
    selected_category=None
    if category == 'user_ads':
        all_ads = current_user.ads
        message="Вашите обяви"
    elif category == 'favorite_user_ads':
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
        is_selected_category=False
        message="Всички обяви"
        all_ads = models.BaseAdd.query.all()
    

    return {'message' : message ,'all_ads' : all_ads, 'selected_category' : selected_category,'is_selected_category':selected_category,'subcategories' : subcategories}
