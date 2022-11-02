from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .forms import RegistrationForm, LoginForm
from .models import User
from .. import db, app
from werkzeug.urls import url_parse
import os


@auth.route('/user-profile/<userID>', methods=['GET', 'POST'])
@login_required
def userProfile(userID):
    user= User.query.filter_by(id=int(userID)).one()
    if request.method == "POST":
        if request.form.get('deleteUser') is not None:
            db.session.delete(user)
            db.session.commit()
            flash('The User: ' + user.username + ' Deleted Succesfully!')
            return redirect(url_for('auth.showUsers', filter='all'))
    return render_template('auth/userProfile.html', user=user)


@auth.route('/show-users', methods=['GET', 'POST'])
@login_required
def showUsers():
    users= User.query.all()
    return render_template('auth/showUsers.html', users=users)

@auth.route('/add-user', methods=['GET', 'POST'])
@login_required
def addUser():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), age=form.age.data.lower(), city=form.city.data.lower(), imagePath=request.files['imagePath'].filename)
        user.set_password(form.password.data)
        fileName = request.files['imagePath'].filename
        request.files['imagePath'].save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('auth.showUsers'))
    return render_template('auth/addUser.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    nologin = False
    if current_user.is_authenticated:
        return redirect(url_for('books.showBooks', filter='all'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            nologin = True
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('books.showBooks', filter='all')
            return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form, message=nologin)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))