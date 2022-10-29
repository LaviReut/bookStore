from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from core import app
from core.auth.models import User
from .models import Books
from ..models import Loans
from . import books
from .forms import BookForm, LoanForm
from .. import db
from datetime import datetime
import os

@books.route('/add-book', methods=['GET', 'POST'])
def addBook():
    form= BookForm()
    form.bookType.choices =[1,2,3]
    if form.validate_on_submit():
        book = Books(bookName=form.bookName.data, authorName=form.authorName.data, bookType=form.bookType.data, bookDate= form.bookDate.data, availableBooks= form.amountToAdd.data, imagePath=request.files['imagePath'].filename)
        fileName = request.files['imagePath'].filename
        request.files['imagePath'].save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.showBooks'))
    return render_template('addBook.html', title='add-Book', form=form)

@books.route('/show-books', methods=['GET', 'POST'])
@login_required
def showBooks():
    check= None
    books= Books.query.all()
    date= datetime.now()
    now= date.strftime("%Y-%m-%d")
    if request.method == "POST":
        if request.form.get('bookDelete') is not None:
            deleteLoan = request.form.get('checkedbox')
            if deleteLoan is not None:
                book = Books.query.filter_by(id=int(deleteLoan)).one()
                db.session.delete(book)
                db.session.commit()
                return redirect(url_for('books.showBooks'))
            else:
                check = 'Please check-box of book to be deleted'
    return render_template('showBooks.html', title='add-Book', books=books, DateNow=now,check=check)

@books.route('/book-profile/<bookID>', methods=['GET', 'POST'])
@login_required
def bookProfile(bookID):
    check= None
    print(bookID)
    book= Books.query.filter_by(id=int(bookID)).one()
    if request.method == "POST":
        if request.form.get('bookDelete') is not None:
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted succesfully!')
            return redirect(url_for('books.showBooks'))
        else:
             check = 'Please check-box of book to be deleted'
    return render_template('bookProfile.html', book=book, check=check)

@books.route('/add-loan', methods=['GET', 'POST'])
@login_required
def addLoan():
    bookList = []
    userList = []
    form= LoanForm()
    books= Books.query.all()
    for book in books:
        bookList.append(book.bookName)
    users= User.query.all()
    for user in users:
        userList.append(user.username)
    form.bookName.choices = bookList
    form.userName.choices = userList
    form.LoanType.choices = [1,2,3]
    if form.validate_on_submit():
        loan = Loans(bookName=form.bookName.data, returnDate=form.ReturnDate.data, loanDate=form.LoanDate.data, book_id= form.bookName.data, user_id= form.userName.data)
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('books.showLoans'))
    return render_template('addLoan.html', title='add-Loan', form=form)

@books.route('/show-loans', methods=['GET', 'POST'])
@login_required
def showLoans():
    check= None
    loans= Loans.query.all()
    if request.method == "POST":
        if request.form.get('loanDelete') is not None:
            deleteLoan = request.form.get('checkedbox')
            if deleteLoan is not None:
                loan = Loans.query.filter_by(id=int(deleteLoan)).one()
                db.session.delete(loan)
                db.session.commit()
                return redirect(url_for('books.showLoans'))
            else:
                check = 'Please check-box of loan to be deleted'

    return render_template('showLoans.html', title='add-Loan', loans=loans, check=check)