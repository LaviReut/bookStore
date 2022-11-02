from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from core import app
from core.auth.models import User
from .models import Books, Category
from ..models import Loans
from . import books
from .forms import BookForm, LoanForm, CategoryForm, BookSearchForm, LoanSearchForm
from .. import db
from datetime import date, timedelta, datetime
import os

############################### Add-Category ###############################

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

############################### Add-Book ###############################

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

############################### Show-Books ###############################

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

############################### Search-Book ###############################

@books.route('/search-book', methods=['GET', 'POST'])
@login_required
def searchBook():
    search = BookSearchForm()
    if request.method == "POST":
        if search.validate_on_submit():
            filter = search.search.data
            return redirect(url_for('books.showBooks', filter=filter))
    return render_template('searchBook.html', title='add-Book', search=search)

############################### Book-Profile ###############################

@books.route('/book-profile/<bookID>', methods=['GET', 'POST'])
@login_required
def bookProfile(bookID):
    book= Books.query.filter_by(id=int(bookID)).one()
    if request.method == "POST":
        if request.form.get('deleteBook') is not None:
            db.session.delete(book)
            db.session.commit()
            flash(book.bookName + ' book deleted succesfully!')
            return redirect(url_for('books.showBooks', filter='all'))
        if request.form.get('loanBook') is not None:
            return redirect(url_for('books.addLoan')) 
        else:
             check = 'Please check-box of book to be deleted'
    return render_template('bookProfile.html', book=book)

############################### Search-Loan ###############################

@books.route('/search-loan', methods=['GET', 'POST'])
@login_required
def searchLoan():
    search = LoanSearchForm()
    if request.method == "POST":
        if search.validate_on_submit():
            filter = search.search.data
            return redirect(url_for('books.showLoans', filter=filter))
    return render_template('searchLoan.html', search=search)

############################### Loan-Profile ###############################

@books.route('/loan-profile/<loanID>', methods=['GET', 'POST'])
@login_required
def loanProfile(loanID):
    check= None
    print(loanID)
    loan= Loans.query.filter_by(id=int(loanID)).one()
    if request.method == "POST":
        if request.form.get('deleteLoan') is not None:
            flash('User: ' + loan.user.username + ' returened the book: ' + loan.book.bookName + '. Loan ID:' +  str(loan.id) + ' deleted succesfully!')
            db.session.delete(loan)
            db.session.commit()
            return redirect(url_for('books.showLoans', filter='all'))
    return render_template('loanProfile.html', loan=loan)

############################### Add-Loan ###############################

@books.route('/add-loan', methods=['GET', 'POST'])
@login_required
def addLoan():
    bookList = []
    userList = []
    form= LoanForm()
    books= Books.query.all()
    for book in books:
        if book.bookType == 1:
            loanLenght = '10 days'
        elif book.bookType == 2:    
            loanLenght = '5 days'
        elif book.bookType == 3:
            loanLenght = '2 days'
        bookList.append(book.bookName + '(' + loanLenght + ')')
    users= User.query.all()
    for user in users:
        userList.append(user.username)
    form.bookName.choices = bookList
    form.userName.choices = userList
    if form.validate_on_submit():
        book = Books.query.filter_by(bookName=form.bookName.data.split("(")[0]).first()
        user = User.query.filter_by(username=form.userName.data).first()
        loandate = date.today()
        if book.bookType==1:
            returnDate = loandate + timedelta(days=10)
        elif book.bookType==2:
            returnDate = loandate + timedelta(days=5) 
        elif book.bookType==3:
            returnDate = loandate + timedelta(days=2)     
        loan = Loans(bookName=form.bookName.data.split("(")[0], returnDate=str(returnDate.strftime("%d/%m/%y")), loanDate=str(loandate.strftime("%d/%m/%y")), book_id= book.id, user_id= user.id)
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('books.showLoans', filter='all'))
    return render_template('addLoan.html', title='add-Loan', form=form)

############################### Show-Loans ###############################

@books.route('/show-loans/<filter>', methods=['GET', 'POST'])
@login_required
def showLoans(filter):
    late = False
    if (filter == 'all') or filter is None:
        loans= Loans.query.all()
    elif filter == 'late':
        late = True
        allLoans= Loans.query.all() 
        today = datetime.now().date()
        lateIDs =[]
        for loan in allLoans:
            if datetime.strptime(loan.returnDate, '%d/%m/%y').date() < today:
                lateIDs.append(str(loan.id))
        loans= Loans.query.filter(Loans.id.in_(lateIDs)).all()
    else:
        loans = Loans.query.filter_by(bookName=filter)
    return render_template('showLoans.html', loans=loans, late=late)