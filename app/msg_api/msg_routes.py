from flask import request, jsonify
from flask_login import login_required, current_user
from app.msg_api import msgapi_bp
from app.db_users import User, Group
from app.db_msg import Messages, Msg_Recipient
from app import db


def msg_is_valid(msg):
    """    message validation   """
    return "recipient" in msg and "message" in msg and "subject" in msg


@msgapi_bp.route('/send_msg', methods=['POST'])
@login_required
def send_msg():
    new_msg = request.get_json() or {}

    if not msg_is_valid(new_msg):
        return jsonify(error="valid input , missing data"), 404

    recipient = User.query.filter_by(username=new_msg['recipient']).first()
    if recipient:
        msg = Messages(subject=new_msg['subject'], message=new_msg['message'], sent=current_user,
                       recipient_name=new_msg['recipient'])
        msg_r = Msg_Recipient(user_recipient=recipient, msg_id=msg)
        db.session.add(msg)
        db.session.add(msg_r)
        db.session.commit()
        return "the message has been sent", 200

    group = Group.query.filter_by(name=new_msg['recipient']).first()
    if group:
        # add Messages
        msg = Messages(subject=new_msg['subject'], message=new_msg['message'], sent=current_user,
                       msg_for_group=True, recipient_name=new_msg['recipient'])
        db.session.add(msg)

        # add recipients
        for user in group.users:
            db.session.add(Msg_Recipient(user_recipient=user, group_recipient=group, msg_id=msg))
        db.session.commit()

        return "the message has been sent to all recipient in the group", 200

    return jsonify(error="invalid recipient"), 404


@msgapi_bp.route('/sent', methods=['GET'])
@login_required
def sent():
    sents = db.session.query(Messages)\
                .filter(Messages.creator_id == current_user.id)\
                .filter(Messages.creation_del == False)
    return jsonify(sent_Messages=[msg.to_dict(shortened=True) for msg in sents]), 200


@msgapi_bp.route('/inbox', methods=['GET'])
@login_required
def inbox():
    inbox_msgs = db.session.query(Messages).join(Msg_Recipient) \
        .filter(Msg_Recipient.recipient_id == current_user.id)\
        .filter(Msg_Recipient.recipient_del == False).all()

    return jsonify(Inbox_messages=[msg.to_dict(shortened=True) for msg in inbox_msgs]), 200


@msgapi_bp.route('/unread', methods=['GET'])
@login_required
def unread_inbox():
    unread_msg = db.session.query(Messages).join(Msg_Recipient) \
        .filter(Msg_Recipient.recipient_id == current_user.id) \
        .filter(Msg_Recipient.recipient_del == False)\
        .filter(Msg_Recipient.is_read == False).all()

    return jsonify(Inbox_unread_messages=[msg.to_dict(shortened=True) for msg in unread_msg]), 200


@msgapi_bp.route('/inbox/read/<int:msg_id>', methods=['GET'])
@login_required
def inbox_read_msg(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    # wrong id , id not found.
    if not msg:
        return jsonify("Invalid input , check msg id"), 404

    msg_recipient = db.session.query(Msg_Recipient) \
        .filter(Msg_Recipient.recipient_id == current_user.id) \
        .filter(Msg_Recipient.message_id == msg.id).first()

    # msg not connect to the current user
    if not msg_recipient:
        return jsonify("Invalid input , check msg id"), 200

    # msg deleted
    if msg_recipient.recipient_del:
        return jsonify("Invalid input , check msg id"), 404

    if not msg_recipient.is_read:
        msg_recipient.is_read = True
        db.session.commit()
    return jsonify(message=msg.to_dict()), 200


@msgapi_bp.route('/sent/read/<int:msg_id>', methods=['GET'])
@login_required
def sent_read_msg(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    # wrong id or msg deleted or msg not connect to current user
    if not msg or msg.creation_del or msg.creator_id != current_user.id:
        return jsonify("Invalid input , check msg id"), 404

    return jsonify(message=msg.to_dict()), 200


@msgapi_bp.route('/delet_sent_msg/<int:msg_id>', methods=['DELETE'])
@login_required
def delet_sent_msg(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    # wrong id or msg already deleted.
    if not msg or msg.creation_del or msg.creator_id != current_user.id:
        return jsonify("Invalid input , check msg id"), 404

    msg.creation_del = True
    db.session.commit()
    return jsonify("Message deleted"), 202


@msgapi_bp.route('/delet_inbox_msg/<int:msg_id>', methods=['DELETE'])
@login_required
def delet_inbox_msg(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    # wrong id or , id not found.
    if not msg:
        return jsonify("Invalid input , check msg id"), 404

    msg_recipient = db.session.query(Msg_Recipient)\
        .filter(Msg_Recipient.recipient_id == current_user.id)\
        .filter(Msg_Recipient.message_id == msg.id).first()

    # msg not for current user
    if not msg_recipient:
        return jsonify("Invalid input , check msg id"), 404

    # msg already deleted
    if msg_recipient.recipient_del:
        return jsonify("Invalid input , check msg id"), 404

    msg_recipient.recipient_del = True
    db.session.commit()
    return jsonify("Message deleted"), 202
