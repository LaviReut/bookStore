from core import app, db
from core.auth.models import User 
from core.books.models import Books

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
        sampleBook = Books(bookName='WebDev', authorName='Ilya', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-christina-morillo-1181244.jpg')
        sampleBook2 = Books(bookName='FlaskDev', authorName='Kerem', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-christina-morillo-1181288.jpg')
        sampleBook3 = Books(bookName='DjangoDev', authorName='Noam', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-mart-production-7550312.jpg')
        sampleBook4 = Books(bookName='StopDev', authorName='Reut', bookType=1 , bookDate= '12/1/99', availableBooks= 1, imagePath='pexels-thisisengineering-3861972.jpg')
        sampleBook5 = Books(bookName='WebDev2', authorName='Ilya', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-christina-morillo-1181244.jpg')
        sampleBook6 = Books(bookName='FlaskDev2', authorName='Kerem', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-christina-morillo-1181288.jpg')
        sampleBook7 = Books(bookName='DjangoDev2', authorName='Noam', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-mart-production-7550312.jpg')
        sampleBook8 = Books(bookName='StopDev2', authorName='Reut', bookType=1 , bookDate= '12/1/2000', availableBooks= 1, imagePath='pexels-thisisengineering-3861972.jpg')
        db.session.add(sampleBook)
        db.session.add(sampleBook2)
        db.session.add(sampleBook3)
        db.session.add(sampleBook4)
        db.session.add(sampleBook5)
        db.session.add(sampleBook6)
        db.session.add(sampleBook7)
        db.session.add(sampleBook8)
        db.session.commit()