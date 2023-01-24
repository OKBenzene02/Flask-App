from market import app, db, login_manage
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItem, SellItem
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def hello_world():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_item = PurchaseItem()
    sell = SellItem()
    if request.method == 'POST':
        # Purchase item section
        item_brought = request.form.get('purchased_item')
        item_object = Item.query.filter_by(name=item_brought).first()
        if item_object:
            if current_user.can_purchase(item_object):
                item_object.budget_change(current_user)
                flash(f'Congratulations! You have purchased {item_object.name} for {item_object.price}$', category='success')
            else:
                flash(f'Insufficient funds, unfortunately you cannot purchase {item_object.name}.', category='danger')

        # Purchase item section
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'Congratulations! You Sold {sold_item_object.name} for {sold_item_object.price}$', category='success')
            else:
                flash(f'Something went wrong with selling {sold_item_object.name}.', category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        item = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', item=item, purchase=purchase_item, owned_items=owned_items, selling=sell)


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(user=form.name.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully! You are logged in as: {user_to_create.user}", category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_login = User.query.filter_by(user=form.name.data).first()
        if user_login and user_login.check_password(user_pass=form.password_login.data):
            login_user(user_login)
            flash(f"Success! You are logged in as: {user_login.user}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password are incorrect! Please try again.', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out successfully.', category='info')
    return redirect(url_for('hello_world'))