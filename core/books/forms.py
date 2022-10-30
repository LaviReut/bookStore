from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TimeField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class BookForm(FlaskForm):
    bookName = StringField('Book Name', validators=[DataRequired()])
    bookType = SelectField('Book Type', coerce=int , validators=[DataRequired()]) 
    bookCategory = SelectField('Book Category', coerce=str , validators=[DataRequired()])
    authorName = StringField('Author Name', validators=[DataRequired()]) 
    bookDate = DateField('Release Date', format='%Y-%m-%d' , validators=[DataRequired()])
    amountToAdd = StringField('Amount to add', validators=[DataRequired()]) 
    imagePath = FileField('Image')
    # bookType = DateField('Date', format='%Y-%m-%d' , validators=[DataRequired()])
    # time = TimeField('Time', format='%H:%M' , validators=[DataRequired()])
    submit = SubmitField('Add Book')

class CategoryForm(FlaskForm):
    categoryName = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

class LoanForm(FlaskForm):
    bookName = SelectField('Book Name', coerce=str , validators=[DataRequired()]) 
    userName = SelectField('User Name', coerce=str , validators=[DataRequired()]) 
    LoanType = SelectField('Loan Type', coerce=int , validators=[DataRequired()]) 
    LoanDate = DateField('Loan Date', format='%Y-%m-%d' , validators=[DataRequired()])
    ReturnDate = DateField('Return Date', format='%Y-%m-%d' , validators=[DataRequired()])
    # time = TimeField('Time', format='%H:%M' , validators=[DataRequired()])
    submit = SubmitField('Add Loan')