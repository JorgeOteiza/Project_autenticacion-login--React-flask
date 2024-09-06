from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.models import User, db

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Crear token de acceso JWT
    token = create_access_token(identity=user.id)

    # Actualizar el campo last_login
    user.update_last_login()
    db.session.commit()

    return jsonify({"token": token, "user": {"id": user.id, "email": user.email}}), 200
