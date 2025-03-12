from flask import Blueprint, jsonify
from models.user import User
from db import db

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user')
def get_users():
    users = User.query.all()
    return jsonify([{'id':user.id, 'name':user.name} for user in users])