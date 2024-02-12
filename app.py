from datetime import  datetime
import models
from functions.hash_function import f_hash
from functions.filter_functions import fetch_ads
from functions.add_recognize_functions import add_recognize
from setup import app,db
from flask import render_template,redirect,url_for,request,session
from flask_login import LoginManager , login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from flask import abort

login_manager=LoginManager(app)

with app.app_context():
    db.create_all()
# Home route
@app.route("/")
def home():

    category = request.args.get('category')

    if category:
        all_ads = fetch_ads(category)
    else:
        all_ads = fetch_ads()

    return render_template('home_page.html', all_ads=all_ads)


@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()


@app.route("/login")
def login(message=None):
    message = request.args.get('message')
    return render_template('login.html', title='Login', message=message)


@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('home'))


@app.route("/register")
def register(message=None):
    message = request.args.get('message')
    return render_template('register.html', title='Login', message=message)


@app.route("/user_page")
@login_required
def user_page():
    category = request.args.get('category')
    if category == 'user_ads':
        all_ads = current_user.ads
    elif category == 'favorite_user_ads':
        all_ads = current_user.favorite_adds
    elif category:
        all_ads = db.session.query(models.BaseAdd).filter_by(category_type=category)
    else:
        all_ads = models.BaseAdd.query.all()
    return render_template('user_page.html', all_ads=all_ads)

@app.route("/add_detail/<add_id>")
def add_page(add_id: int): 
    base_ad=models.BaseAdd.query.get(add_id)
    ad = add_recognize(base_ad)
    is_login=current_user.is_authenticated
    if is_login:
        is_saved=base_ad in current_user.favorite_adds
        is_current_user_add= base_ad in current_user.ads
    else:
        is_saved=False
        is_current_user_add=False    
    return render_template('ad_details.html',ad=ad,is_login=is_login,is_saved=is_saved,is_current_user_add=is_current_user_add)

@app.route("/show_ad_list>")
def add_list():
    all_ads=current_user.ads
    return render_template('ad_list.html',all_ads=all_ads)

@app.route("/to_sell")
def to_sell():
    return redirect(url_for('sell_form'))

@app.route("/to_login")
def login_go():
    return redirect(url_for('login'))

@app.route("/to_add_detail")
def ad_detail_go():
    return redirect(url_for('ad_detail'))

@app.route("/close")
def login_close():
    return redirect(url_for('home'))

@app.route('/sell', methods=['POST','GET'])
def sell_form():
    categories = ['Електроника', 'Облекло','Превозни средства','Работа','Недвижими имоти','Спорт']

    subcategories = {
        'Електроника': ['Компютри', 'Таблети', 'Аудио техника', 'Телефони', 'Телевизори', 'Домашна техника'],
        'Облекло': ['Дамско', 'Мъжко'],
        'Превозни средства': ['Автомобили', 'Мотоциклети'],
        'Работа': ['Пълно работно време', 'Непълно работно време', 'Работа от вкъщи'],
        'Недвижими имоти': ['Апартаменти за продажба', 'Къщи за продажба'],
        'Спорт': ['Фитнес и тренировки', 'Спортни съоръжения', 'Велосипеди'],
    }

    cities = ['София', 'Пловдив', 'Варна', 'Бургас', 'Русе', 'Стара Загора', 'Плевен', 'Велико Търново', 'Смолян']

    selected_category = request.form.get('category', '')
    selected_subcategory = request.form.get('subcategory', '')
    

    return render_template('sell.html', categories=categories, subcategories=subcategories,
                           selected_category=selected_category, selected_subcategory=selected_subcategory,cities=cities)


@app.route("/sell_action",methods=['GET', 'POST'])
def sell_action():
    title=request.form['title']
    photos = [request.form[f'photo{i}'] for i in range(1, 4)]
    description=request.form['description']
    price=request.form['price']
    location=request.form['location']
    phone=request.form['phone']
    current_user = load_user(session['user_id'])
    subcategory = request.form.get('subcategory')
    category = request.form.get('category')
    saves=0
    ad_params = {
        'title': title,
        'content': description,
        'item_price': price,
        'location': location,
        'created_at': datetime.now(),
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
        ad = models.Computer(ad_params,pc_type=type_pc)
    elif(subcategory == 'Таблети'):
        reader_type=request.form['type_PC']
        ad = models.Tablet(ad_params,reader_type=reader_type)
    elif subcategory == 'Телефони':
        brand = request.form['brand']
        ad = models.Phone(ad_params,phone_brand=brand) 
    elif subcategory == 'Аудио техника':
        type = request.form['brand']
        ad = models.AudioEquipment(ad_params,type=type) 
    elif subcategory == 'Телевизори':
        inches = request.form['brand']
        ad = models.Television(ad_params, inches) 
    elif subcategory == 'Домашна техника':
        house_appliance_type = request.form['house_appliance_type']
        ad = models.HouseholdAppliance(ad_params, house_appliance_type) 
    elif subcategory == 'Дамско':
        women_clothing_type = request.form['women_clothing_types ']
        ad = models.WomenClothing(ad_params, women_clothing_type) 
    elif subcategory == 'Мъжко':
        men_clothing_type = request.form['men_clothing_type']
        ad = models.MenClothing(ad_params, men_clothing_type) 
    elif category == 'Работа':
        sector=request.form['work_sector']
        salary =request.form['salary']
        if subcategory == 'Пълно работно време':
            ad = models.FullTime(ad_params, sector,salary) 

    db.session.close()
    images = [models.Image(url=photo,add_id=ad.id) for photo in photos]
    with db.session.begin():
        for image in images: 
            db.session.add(image)
        db.session.add(ad)
        db.session.commit()
    
    current_user.ads.append(ad)

    return redirect(url_for('user_page'))


    
@app.route("/save_add", methods=['POST'])
def save_add():
    add_id = request.form.get('save_addbtn')

    if not add_id:
        abort(400, 'Invalid request')

    add = models.BaseAdd.query.get(add_id)


    if not add:
        abort(404, 'Ad not found')

    add.saves+=1

    current_user.add_favorite_advert(add)

    return render_template('ad_details.html', ad=add)



@app.route("/login_action", methods=['POST'])
def login_action():
    if request.method != 'POST':
        return abort(400, 'Invalid method')

    email = request.form['email']
    password_hash = f_hash(request.form['password'])
    
    current_local_user = models.User.query.filter_by(email=email).first()

    if current_local_user and current_local_user.password_hash == password_hash:
        session['username'] = current_local_user.name
        session['user_id'] = current_local_user.id
        login_user(current_local_user)
        return redirect(url_for('user_page', user_name=current_local_user.name))
    else:
        return redirect(url_for('login', message='Invalid username or password!'))
   


@app.route("/register_action", methods=['POST'])
def register_action_action():
    if request.method != 'POST':
        return redirect(url_for('register', message='Invalid method'))

    user_name = request.form['username'].lower()
    password_hash = f_hash(request.form['password'])
    email = request.form['email'].lower()
    new_user = models.User(name=user_name, email=email, password_hash=password_hash)

    try:
        models.save_user(new_user)
    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: users.name" in str(e):
            error_message = "The username is already in use. Please choose a different username."
        elif "UNIQUE constraint failed: users.email" in str(e):
            error_message = "The email address is already in use. Please choose a different email."
        return redirect(url_for('register', message=error_message))

    session_data = {'username': user_name, 'user_id': new_user.id}
    session.update(session_data)

    login_user(new_user)

    return redirect(url_for('registration_success'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        print(search_query)
        if search_query:
            all_ads = models.BaseAdd.query.filter(or_(models.BaseAdd.title.ilike(f"%{search_query}%"),
                                                       models.BaseAdd.content.ilike(f"%{search_query}%"))).all()
            result_string = f"Резултати за '{search_query}'"
            if current_user.is_authenticated: 
                return render_template('user_page.html', all_ads=all_ads,category_title=result_string)
            else :
                return render_template('home_page.html', all_ads=all_ads,category_title=result_string)
    
    result_string = f"Няма резултати за '{search_query}'"
    if current_user : 
         return render_template('user_page.html', category_title=result_string)
    else :
        return render_template('home_page.html', category_title=result_string)


@login_manager.user_loader
def load_user(user_id: int):
    return models.User.query.get(int(user_id))
