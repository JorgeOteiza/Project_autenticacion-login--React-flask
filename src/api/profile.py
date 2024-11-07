# profile.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import User

# Define el Blueprint para el perfil
profile_bp = Blueprint('profile_bp', __name__)

# Ruta para obtener el perfil del usuario actual
@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Devuelve los datos del usuario autenticado
    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None
        },
        "message": "Profile retrieved successfully"
    }), 200
