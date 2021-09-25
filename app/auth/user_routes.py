from flask import request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.db_users import User, Group
from app import db


def username_is_registered(username):
    """  username validation   """
    first_user = User.query.filter_by(username=username).first()
    if first_user is None:
        return False
    return True


def Group_exsist(name):
    """  group validation   """
    first_group = Group.query.filter_by(name=name).first()
    if first_group is None:
        return False
    return True


def user_at_group(user, group_name):
    for group in user.Group:
        if group.name == group_name:
            return True
    return False


@auth_bp.route('/signup', methods=['POST'])
def add_user():
    new_user_data = request.get_json() or {}
    if "username" in new_user_data:
        if not username_is_registered(new_user_data["username"]):
            new_user = User(username=new_user_data["username"])
            new_user.set_password(new_user_data["password"])
            db.session.add(new_user)
            db.session.commit()
            return '', 201

    return jsonify(error="valid input or auth already registered "), 404


@auth_bp.route('/login', methods=['GET'])
def login():
    return "please login as post to this url"


@auth_bp.route('/login', methods=['POST'])
def login_post():
    data = request.get_json() or {}
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user and not user.check_password(password):
        return redirect(url_for('auth.login'))

    login_user(user)

    return 'login success', 200


@auth_bp.route('/logout')
def logout():
    logout_user()
    return 'logout success', 200


@auth_bp.route('/add_group', methods=['POST'])
@login_required
def add_group():
    new_group_data = request.get_json() or {}
    if "name" in new_group_data and not Group_exsist(new_group_data["name"]):
        new_group = Group(name=new_group_data["name"])
        db.session.add(new_group)
        db.session.commit()
        return 'new group added', 201

    return jsonify(error="valid input or group already exsist "), 404


@auth_bp.route('/join_group/<string:group_name>', methods=['POST'])
@login_required
def join_group(group_name):
    if not Group_exsist(group_name):
        return 'group not exsist', 404

    if user_at_group(current_user, group_name):
        return "You've joined the group already", 404
    group = Group.query.filter_by(name=group_name).first()

    group.users.append(current_user)
    db.session.commit()
    return 'you just added to group named :' + group_name, 200


@auth_bp.route('/leave_group/<string:group_name>', methods=['POST'])
@login_required
def leave_group(group_name):
    if not Group_exsist(group_name):
        return 'group not exsist', 404

    if not user_at_group(current_user, group_name):
        return "You've left the group already", 404

    group = Group.query.filter_by(name=group_name).first()
    group.users.remove(current_user)
    db.session.commit()
    return 'you just leave group named :' + group_name, 200


@auth_bp.route('/my_groups', methods=['GET'])
@login_required
def my_groups():
    group_list = [group.name for group in current_user.Group]
    return jsonify(my_groups=group_list), 200
