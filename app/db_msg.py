from app import db
from datetime import datetime


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20))
    message = db.Column(db.Text())
    recipient_name = db.Column(db.String(50))
    msg_for_group = db.Column(db.Boolean, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_del = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    recipient = db.relationship('Msg_Recipient', backref='msg_id', lazy=True)

    def to_dict(self, shortened=False):
        data = {
            'id': self.id,
            'subject': self.subject,
            'creation_date': self.creation_date
        }
        if not shortened:
            data['message'] = self.message

        if self.msg_for_group:
            data['Group recipient'] = self.recipient_name
        else:
            data['user recipient'] = self.recipient_name
        return data


class Msg_Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    is_read = db.Column(db.Boolean, default=False)
    recipient_del = db.Column(db.Boolean, default=False)
