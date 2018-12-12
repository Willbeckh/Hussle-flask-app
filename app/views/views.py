from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms.forms import RegisterForm, LoginForm, BusinessForm, DeleteForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models.models import User, Business


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for {form.username.data} created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('Logged in successfully', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful, Please check your details!', 'danger')
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('account.html')

# the magic that happens when registering a business happens here
@app.route('/businesses', methods=['GET', 'POST'])
@login_required
def businesses():
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(name = form.name.data, location = form.location.data,
            started = form.date.data, business_description = form.business_description.data)
        db.session.add(business)
        db.session.commit()
        flash(f'Successfully registered {business.name} business', 'success')
        return redirect(url_for('businesses_present'))
    else:
        flash('Your business was not registered. Please check your details and try again ', 'danger')
    return render_template('register_biz.html', title='Register-biz', form=form)

# get all reegistered businesses
@app.route('/businesses-present', methods=['GET', 'POST'])
def businesses_present():
    businesses = Business.query.all()
    return render_template('present.html', businesses = businesses)

@app.route('/businesses/<int:business_id>/update', methods = ['POST', 'GET'])
@login_required
def update_business(business_id):
    business = Business.query.get_or_404(business_id)
    form = BusinessForm()
    if form.validate_on_submit():
        business.name = form.name.data
        business.location = form.location.data
        business.business_description = form.business_description.data
        db.session.commit()
        flash(f'Your business has been updated', 'success')
        return redirect(url_for('single_business', business_id = business.id))
    elif request.method == 'GET':
        form.name.data = business.name
        form.location.data = business.location
        form.business_description.data = business.business_description
        return render_template('register_biz.html', title = 'update', form = form)


# get business by its ID
@app.route('/businesses/<int:business_id>')
@login_required
def single_business(business_id):
    business = Business.query.get_or_404(business_id)
    return render_template('one_business.html', business = business)

@app.route('/delete/<int:business_id>', methods = ['POST', 'GET'])
@login_required
def deletebusiness(business_id):
    form = DeleteForm()
    business = Business.query.get_or_404(business_id)
    db.session.delete(business)
    db.session.commit()
    flash('Your business has been deleted', 'success')
    return render_template('delete_business.html', form=form)
