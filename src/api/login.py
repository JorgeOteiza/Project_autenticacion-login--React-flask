# login.py: Rutas para login de usuarios
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.models import User, db

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=user.id)
    user.update_last_login()
    db.session.commit()
    
    return jsonify({"token": token, "user": user.serialize()}), 200
