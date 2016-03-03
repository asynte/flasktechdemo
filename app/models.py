from app import db
from flask.ext.login import LoginManager, UserMixin
from werkzeug import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False) #could have duplicate
    userID = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    pwdhash = db.Column(db.String(54), nullable=True)  
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, social_id, userID, email, password):
        if social_id:
            self.social_id = social_id #not required if not using Facebook login
        if userID:
            self.userID = userID
        self.email = email.lower()
        if password:
            self.set_password(password)
            assert self.check_password(password)
        
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.userID)

class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
