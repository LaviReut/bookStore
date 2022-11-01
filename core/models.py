from core import db

class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(140))
    returnDate = db.Column(db.String())
    loanDate = db.Column(db.String())
    book_id= db.Column(db.String, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<ToDo {}>'.format(self.title)