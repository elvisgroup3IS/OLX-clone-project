import models

def fetch_ads(category=None):
    if category :
        return models.BaseAdd.filter_by(category_type=category)
    else :
        return models.BaseAdd.query.all()