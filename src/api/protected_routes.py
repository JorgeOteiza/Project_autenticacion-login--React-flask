from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, User

# Crear el Blueprint
protected_bp = Blueprint('protected_bp', __name__)

# Definir la ruta protegida dentro del Blueprint
@protected_bp.route('/protected', methods=['OPTIONS', 'GET'])
@jwt_required(optional=True)
def protected_route():
    # Manejar solicitudes OPTIONS para preflight de CORS
    if request.method == 'OPTIONS':
        return '', 204  # Respuesta rápida para solicitudes preflight

    # Obtener el ID del usuario desde el token JWT para las solicitudes GET
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    # Buscar al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retornar la información del usuario autenticado
    return jsonify({
        "message": "This is a protected route",
        "user": {
            "id": user.id,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
    }), 200
