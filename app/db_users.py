from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


""" many-to-many = User to Group table """
User_Group = db.Table("User_Group",
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('Group_id', db.Integer, db.ForeignKey('group.id'))
                      )


class User(UserMixin, db.Model):
    """ User table """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Group = db.relationship('Group', secondary=User_Group, backref=db.backref('users', lazy='dynamic'))
    sent_messages = db.relationship('Messages', backref='sent', lazy=True)

    inbox_messages = db.relationship('Msg_Recipient', backref='user_recipient', lazy=True)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def valid_password(self, password):
        return check_password_hash(self.password_hash, password)


class Group(db.Model):
    """ Group table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    inbox_messages = db.relationship('Msg_Recipient', backref='group_recipient', lazy=True)
