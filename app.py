"""This is route app module"""
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager , login_user, logout_user, login_required, current_user
from flask import render_template,redirect,url_for,request,abort,Response
from functions import other_functions, filter_functions, add_functions,user_functions
from setup import app,db
import models

login_manager=LoginManager(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    """
    Renders the home page with advertisements.
    """
    logout()
    category = request.args.get('category')

    if category:
        kwargs = filter_functions.category_filter(category=category)
    else:
        kwargs = filter_functions.category_filter()
    return render_template('home_page.html', **kwargs)




@app.route("/login")
def login(message=None):
    """
    Renders the login page with optional message.
    """

    message = request.args.get('message')
    return render_template('login.html', title='Login', message=message)


@app.route('/logout')
def logout():
    """
    Loggout user then redirect the home page .
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/register")
def register(message=None):
    """
    Renders the register page with optional message.
    """

    message = request.args.get('message')
    return render_template('register.html', message=message)

@app.route("/clear_filters",methods=['POST'])
def clear_filters():
    kwargs=filter_functions.category_filter()
    return render_template('user_page.html', **kwargs)

@app.route("/filter",methods=['POST'])
def filter_ads():
    """
    Redirect user_page route with filter kwargs to filter ads.
    """
    subcategory_key = 'subcategory'

    categories=other_functions.load_from_json()
    selected_category=request.form['category_selected']
    substring = selected_category.split(":")[-1].strip()

    if subcategory_key in request.form:
        if request.form['subcategory'] != 'not_selected':
            subcategory=request.form['subcategory']
            ads=filter_functions.category_filter(subcategory=subcategory)['all_ads']
        elif substring in categories['categories']:
            ads=filter_functions.category_filter(category=substring)['all_ads']
        else :
            ads=filter_functions.category_filter()['all_ads']

    elif substring in categories['categories']:
        ads=filter_functions.category_filter(category=substring)['all_ads']
    else :
        ads=filter_functions.category_filter()['all_ads']

    max_price=request.form['max_price']
    if max_price != '':
        ads=filter_functions.price_filter(ads,max_price)
    if 'location' in request.form:
        city=request.form['location']
        if city != 'default':
            ads=filter_functions.location_filter(ads,city)

    return render_template('user_page.html', all_ads=ads,is_filtered=True)

@app.route("/user_page")
@login_required
def user_page():
    """
    Render user_page with filter adds and kwarg for next filter(subcategory).
    """
    category = request.args.get('category')
    ads_key='ads'
    is_filtred=request.args.get('is_filtered')
    if ads_key not in request.args:
        kwargs = filter_functions.category_filter(category=category, current_user=current_user)
    elif ads_key in request.args:
        ads=request.args.get('ads')
        kwargs={'all_ads':ads,'is_filtred':is_filtred}
    elif not category :
        pass

    return render_template('user_page.html', **kwargs)

@app.route("/add_detail/<add_id>")
def add_page(add_id: int):
    """
    Render add_page with ad and bool flags for define actions.
    """
    base_ad=models.BaseAdd.query.get(add_id)
    ad = add_functions.add_recognize(base_ad)
    is_login=current_user.is_authenticated
    params={'ad':ad,'is_login':is_login}
    if is_login:
        is_saved=base_ad in current_user.favorite_adds
        is_current_user_add= base_ad in current_user.ads
    else:
        is_saved=False
        is_current_user_add=False
    params.update({'is_save':is_saved,'is_current_user_add':is_current_user_add})
    return render_template('ad_details.html',**params)

@app.route('/add_delete/<add_id>',methods=['POST'])
@login_required
def delete_add(add_id):
    """
    Delete add for base and then render to user_page.
    """
    try:
        add_functions.delete_add(add_id)
    except ValueError:
        abort(Response('Няма такава обява'))

    return redirect(url_for('user_page'))

@app.route("/to_sell")
def to_sell():
    """
    Redirect to sell_form.
    """
    return redirect(url_for('sell_form'))

@app.route("/to_login")
def login_go():
    """
    Redirect to login.
    """
    return redirect(url_for('login'))

@app.route("/to_add_detail")
def ad_detail_go():
    """
    Redirect to ad_detail.
    """
    return redirect(url_for('ad_detail'))

@app.route("/close")
def login_close():
    """
    Redirect to home.
    """
    return redirect(url_for('home'))

@app.route('/sell', methods=['POST','GET'])
def sell_form():
    """
    Render the sell form with category, subcategory, and city options.
    """
    json_data=other_functions.load_from_json()

    categories,subcategories = json_data['categories'],json_data['subcategories']
    cities = json_data['cities']

    selected_category = request.form.get('category')
    selected_subcategory = request.form.get('subcategory')

    return render_template('sell.html',selected_category=selected_category,
                        selected_subcategory=selected_subcategory,categories=categories,
                        subcategories=subcategories,cities=cities)


@app.route("/sell_action",methods=['GET', 'POST'])
def sell_action():
    """
    Process the form submission for creating a new ad.
    """

    subcategory = request.form['subcategory']
    if current_user.is_limit_by_category(subcategory) :
        abort(400, 'Превишили сте лимита в тази категория , моля върнете се и изберете друга.')

    ad=add_functions.create_add(request.form,current_user)
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
    """
    Process the request to save an advertisement as a favorite.
    """
    add_id = request.form.get('save_addbtn')

    if not add_id:
        abort(400, 'Invalid request')

    add = models.BaseAdd.query.get(add_id)

    if not add:
        abort(404, 'Ad not found')

    add.saves+=1

    try:
        current_user.add_favorite_advert(add)
    except IntegrityError:
        db.session.rollback()
        render_template('ad_details.html', ad=add)

    return render_template('ad_details.html', ad=add)


@app.route("/login_action", methods=['POST'])
def login_action():
    """
    Process the login form submission.
    """
    email = request.form['email']
    password_hash = other_functions.f_hash(request.form['password'])

    current_local_user = user_functions.search_for_user(email=email)

    if current_local_user and current_local_user.password_hash == password_hash:
        login_user(current_local_user)
        return redirect(url_for('user_page'))

    return redirect(url_for('login', message='Invalid username or password!'))


@app.route("/register_action", methods=['POST'])
def register_action_action():
    """
    Process the user registration form submission.
    """
    user_name = request.form['username'].lower()
    password_hash = other_functions.f_hash(request.form['password'])
    email = request.form['email'].lower()
    new_user = models.User(name=user_name, email=email, password_hash=password_hash)
    error_message=''
    name_error_key="UNIQUE constraint failed: users.name"
    email_error_key="UNIQUE constraint failed: users."
    try:
        user_functions.save_user(new_user)
    except IntegrityError as e:
        db.session.rollback()
        if name_error_key in str(e):
            error_message = "The username is already in use. Please choose a different username."
        elif email_error_key in str(e):
            error_message = "The email address is already in use. Please choose a different email."
        return redirect(url_for('register', message=error_message))

    return redirect(url_for('login', message='Succesfull registration ,please login in .'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    Handle the search functionality.
    """
    method_key='POST'
    if request.method == method_key:
        search_query = request.form.get('search_query')

        all_ads=filter_functions.search_filter(search_query)

        if all_ads:
            result_string = f"Резултати за '{search_query}'"
            template = 'user_page.html' if current_user.is_authenticated else 'home_page.html'
            return render_template(template, all_ads=all_ads,
                                    message=result_string,is_filtered=True)

    result_string = f"Няма резултати за '{search_query}'"
    template = 'user_page.html' if current_user.is_authenticated else 'home_page.html'
    return render_template(template, message=result_string,is_filtered=True)


@login_manager.user_loader
def load_user(user_id: int):
    """
    Load the user object from the database based on the user ID.
    """
    return models.User.query.get(int(user_id))
