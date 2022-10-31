from .. import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(10))
    authorName = db.Column(db.String(20))
    bookType = db.Column(db.Integer)
    bookDate = db.Column(db.String)
    availableBooks = db.Column(db.Integer)
    imagePath = db.Column(db.String)
    bookCategory = db.Column(db.String(20))
    loans = db.relationship('Loans', backref='book')
    
    def __repr__(self):
        return '<BookName {}>'.format(self.bookName)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
 
    
    def __repr__(self):
        return '<Category {}>'.format(self.name)