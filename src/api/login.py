from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Lógica de autenticación, ej.
    if email == "usuario@example.com" and password == "contraseña":
        token = create_access_token(identity=email)
        return jsonify({"token": token, "user": {"id": 1, "email": email}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
