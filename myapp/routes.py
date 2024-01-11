from flask import Blueprint, redirect, url_for, jsonify

from .extensions import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    res = [user.username for user in users]
    return jsonify(users=res)

@main.route('/add/<username>')
def add_user(username):
    try:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User added successfully')
    except Exception as e:
        return jsonify(error=str(e))
