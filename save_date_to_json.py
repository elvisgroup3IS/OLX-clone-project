import json

categories = ['Електроника', 'Облекло', 'Превозни средства', 'Работа', 'Недвижими имоти', 'Спорт']

subcategories = {
    'Електроника': ['Компютри', 'Таблети', 'Аудио техника', 'Телефони', 'Телевизори', 'Домашна техника'],
    'Облекло': ['Дамско', 'Мъжко'],
    'Превозни средства': ['Автомобили', 'Мотоциклети'],
    'Работа': ['Пълно работно време', 'Непълно работно време', 'Работа от вкъщи'],
    'Недвижими имоти': ['Апартаменти', 'Къщи'],
    'Спорт': ['Фитнес и тренировки', 'Спортни съоръжения', 'Велосипеди'],
}

cities = ['София', 'Пловдив', 'Варна', 'Бургас', 'Русе', 'Стара Загора', 'Плевен', 'Велико Търново', 'Смолян']

# Combine categories and subcategories into a single dictionary
data = {'categories': categories, 'subcategories': subcategories,'cities': cities}

# Convert the dictionary to JSON
json_data = json.dumps(data, ensure_ascii=False, indent=2)

# Write the JSON data to a file
with open('static/helping_data.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)