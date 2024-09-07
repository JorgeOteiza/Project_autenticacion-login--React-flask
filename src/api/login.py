from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from api.models import User, db

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])  # Asegúrate de que esté definida con 'POST'
def login_post():
    try:
        # Obtener los datos enviados por el usuario (email y password)
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Verificar que ambos campos estén presentes
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        # Buscar al usuario en la base de datos
        user = User.query.filter_by(email=email).first()

        # Verificar que el usuario exista y que la contraseña sea correcta
        if user is None or not user.check_password(password):
            return jsonify({"message": "Invalid email or password"}), 401

        # Si el usuario es válido, generar un token JWT
        token = create_access_token(identity=user.id)

        # Actualizar último inicio de sesión
        user.update_last_login()
        db.session.commit()

        # Devolver el token JWT y la información del usuario
        return jsonify({"token": token, "user": {"id": user.id, "email": user.email}}), 200

    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({"message": "An error occurred during login", "error": str(e)}), 500
