import models

def fetch_ads(category=None,subcategory=None):
    if subcategory :
        return models.db.session.query(models.BaseAdd).filter_by(subcategory_type=subcategory)
    if category :
        return models.db.session.query(models.BaseAdd).filter_by(category_type=category)
    else :
        return models.BaseAdd.query.all()