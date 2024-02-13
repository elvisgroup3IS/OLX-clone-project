from datetime import  datetime
import models
from functions.hash_function import f_hash
from functions.filter_functions import fetch_ads
from functions import add_functions
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
        message="Вашите обяви"
    elif category == 'favorite_user_ads':
        all_ads = current_user.favorite_adds
        message="Вашите любими обяви"
    elif category:
        all_ads = db.session.query(models.BaseAdd).filter_by(category_type=category)
        message=f"Обяви в категория : {category} "
    else:
        message="Всички обяви"
        all_ads = models.BaseAdd.query.all()
    return render_template('user_page.html', all_ads=all_ads,message=message)

@app.route("/add_detail/<add_id>")
def add_page(add_id: int): 
    base_ad=models.BaseAdd.query.get(add_id)
    ad = add_functions.add_recognize(base_ad)
    is_login=current_user.is_authenticated
    if is_login:
        is_saved=base_ad in current_user.favorite_adds
        is_current_user_add= base_ad in current_user.ads
    else:
        is_saved=False
        is_current_user_add=False    
    return render_template('ad_details.html',ad=ad,is_login=is_login,is_save=is_saved,is_current_user_add=is_current_user_add)

@app.route('/add_delete/<add_id>',methods=['POST', 'DELETE'])
@login_required
def delete_add(add_id):
    if request.form.get('_method') != 'DELETE':
        return abort(400, 'Invalid method')
    
    add_functions.delete_add(add_id)
    return redirect(url_for('user_page'))

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
        'Недвижими имоти': ['Апартаменти', 'Къщи'],
        'Спорт': ['Фитнес и тренировки', 'Спортни съоръжения', 'Велосипеди'],
    }

    cities = ['София', 'Пловдив', 'Варна', 'Бургас', 'Русе', 'Стара Загора', 'Плевен', 'Велико Търново', 'Смолян']

    selected_category = request.form.get('category', '')
    selected_subcategory = request.form.get('subcategory', '')
    

    return render_template('sell.html', categories=categories, subcategories=subcategories,
                           selected_category=selected_category, selected_subcategory=selected_subcategory,cities=cities)


@app.route("/sell_action",methods=['GET', 'POST'])
def sell_action():
    current_user = load_user(session['user_id'])

    ad=add_functions.create_add(request,current_user)
    photos=[ad.photo1,ad.photo2,ad.photo3]
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

    return redirect(url_for('login', message='Succesfull registration ,please login in .'))

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
