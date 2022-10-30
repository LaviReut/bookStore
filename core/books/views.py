from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from core import app
from core.auth.models import User
from .models import Books, Category
from ..models import Loans
from . import books
from .forms import BookForm, LoanForm, CategoryForm, BookSearchForm, LoanSearchForm
from .. import db
from datetime import datetime
import os

@books.route('/add-category', methods=['GET', 'POST'])
@login_required
def addCategory():
    form= CategoryForm()
    if form.validate_on_submit():
        cat = Category(name=form.categoryName.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('books.addBook'))
    return render_template('addCategory.html', title='add-Book', form=form)


@books.route('/add-book', methods=['GET', 'POST'])
@login_required
def addBook():
    form= BookForm()
    form.bookType.choices =[1,2,3]
    catagories= Category.query.all()
    catList = []
    for catagory in catagories:
        catList.append(str(catagory.name))
    form.bookCategory.choices = catList
    if form.validate_on_submit():
        book = Books(bookName=form.bookName.data, authorName=form.authorName.data, bookType=form.bookType.data, bookDate= form.bookDate.data, availableBooks= form.amountToAdd.data, imagePath=request.files['imagePath'].filename, bookCategory=form.bookCategory.data)
        fileName = request.files['imagePath'].filename
        request.files['imagePath'].save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.showBooks', filter='all'))
    return render_template('addBook.html', title='add-Book', form=form)

@books.route('/show-books/<filter>', methods=['GET', 'POST'])
@login_required
def showBooks(filter):
    search = BookSearchForm()
    check= None
    if (filter == 'all') or filter is None:
        books= Books.query.all()
    else:
        books = Books.query.filter_by(bookName=filter)
    catagories= Category.query.all()
    catList = []
    for catagory in catagories:
        catList.append(str(catagory.name))
    if request.method == "POST":
        if search.validate_on_submit():
            filter = search.search.data
            return redirect(url_for('books.showBooks', filter=filter))
    return render_template('showBooks.html', title='add-Book', books=books, catList=catList, check=check, search=search)

@books.route('/search-book', methods=['GET', 'POST'])
@login_required
def searchBook():
    search = BookSearchForm()
    if request.method == "POST":
        if search.validate_on_submit():
            filter = search.search.data
            return redirect(url_for('books.showBooks', filter=filter))
    return render_template('searchBook.html', title='add-Book', search=search)


@books.route('/search-loan', methods=['GET', 'POST'])
@login_required
def searchLoan():
    search = LoanSearchForm()
    if request.method == "POST":
        if search.validate_on_submit():
            filter = search.search.data
            return redirect(url_for('books.showLoans', filter=filter))
    return render_template('searchLoan.html', search=search)


@books.route('/loan-profile/<loanID>', methods=['GET', 'POST'])
@login_required
def loanProfile(loanID):
    check= None
    print(loanID)
    loan= Loans.query.filter_by(id=int(loanID)).one()
    if request.method == "POST":
        if request.form.get('deleteLoan') is not None:
            db.session.delete(loan)
            db.session.commit()
            flash('Loan deleted succesfully!')
            return redirect(url_for('books.showLoans', filter='all'))
    return render_template('loanProfile.html', loan=loan)


@books.route('/book-profile/<bookID>', methods=['GET', 'POST'])
@login_required
def bookProfile(bookID):
    check= None
    print(bookID)
    book= Books.query.filter_by(id=int(bookID)).one()
    if request.method == "POST":
        if request.form.get('deleteBook') is not None:
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted succesfully!')
            return redirect(url_for('books.showBooks', filter='all'))
        if request.form.get('loanBook') is not None:
            return redirect(url_for('books.addLoan')) 
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
        return redirect(url_for('books.showLoans', filter='all'))
    return render_template('addLoan.html', title='add-Loan', form=form)

@books.route('/show-loans/<filter>', methods=['GET', 'POST'])
@login_required
def showLoans(filter):
    check= None
    if (filter == 'all') or filter is None:
        loans= Loans.query.all()
    else:
        loans = Loans.query.filter_by(bookName=filter)
    return render_template('showLoans.html', loans=loans, check=check)