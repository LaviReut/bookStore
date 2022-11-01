from core import app, db
from core.models import Loans
from core.auth.models import User 
from core.books.models import Books, Category

with app.app_context():
    db.create_all()
    db.session.commit()
    Auser = User.query.filter_by(username='admin').first()
    if not Auser:
        adminuser = User(username='admin', email='admin@admin.com', imagePath='users/programmer-avatar.png' )
        adminuser.set_password('admin')
        sampleUser = User(username='Amichai', email='sample@sample.com', imagePath='users/programmer-avatar.png')
        sampleUser.set_password('sample')
        db.session.add(adminuser)
        db.session.add(sampleUser)
        db.session.commit()
        cat1 = Category(name='Programming')
        cat2 = Category(name='Nature')
        cat3 = Category(name='Action')
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.add(cat3)
        db.session.commit()
        sampleBook = Books(bookName='WebDev', authorName='Ilya', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-christina-morillo-1181244.jpg', bookCategory='Programming')
        sampleBook2 = Books(bookName='FlaskDev', authorName='Kerem', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-christina-morillo-1181288.jpg', bookCategory='Programming')
        sampleBook3 = Books(bookName='DjangoDev', authorName='Noam', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-mart-production-7550312.jpg', bookCategory='Programming')
        sampleBook4 = Books(bookName='Mount Flask', authorName='Reut', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-thisisengineering-3861972.jpg', bookCategory='Nature')
        sampleBook5 = Books(bookName='Ocean Bugs', authorName='Ilya', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-christina-morillo-1181244.jpg', bookCategory='Nature')
        sampleBook6 = Books(bookName='Shoot Fast Die Slow', authorName='Kerem', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-christina-morillo-1181288.jpg', bookCategory='Action')
        sampleBook7 = Books(bookName='No Risk No Fun', authorName='Noam', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-mart-production-7550312.jpg', bookCategory='Action')
        sampleBook8 = Books(bookName='Code Gun', authorName='Reut', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-thisisengineering-3861972.jpg', bookCategory='Action')
        db.session.add(sampleBook)
        db.session.add(sampleBook2)
        db.session.add(sampleBook3)
        db.session.add(sampleBook4)
        db.session.add(sampleBook5)
        db.session.add(sampleBook6)
        db.session.add(sampleBook7)
        db.session.add(sampleBook8)
        db.session.commit()
