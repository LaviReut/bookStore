from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .forms import RegistrationForm, LoginForm
from .models import User
from .. import db
from werkzeug.urls import url_parse

@auth.route('/show-users', methods=['GET', 'POST'])
@login_required
def showUsers():
    check= None
    users= User.query.all()
    if request.method == "POST":
        if request.form.get('userDelete') is not None:
            deleteLoan = request.form.get('checkedbox')
            if deleteLoan is not None:
                user = User.query.filter_by(id=int(deleteLoan)).one()
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for('auth.showUsers'))
            else:
                check = 'Please check-box of user to be deleted'
    return render_template('auth/showUsers.html', users=users,check=check)

@auth.route('/add-user', methods=['GET', 'POST'])
@login_required
def addUser():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), imagePath=request.files['imagePath'].filename)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/addUser.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    nologin = False
    if current_user.is_authenticated:
        return redirect(url_for('books.showBooks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            nologin = True
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('books.showBooks')
            return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form, message=nologin)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))