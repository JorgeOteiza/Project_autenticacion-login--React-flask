from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, User

# Crear un nuevo Blueprint si prefieres manejarlo en un archivo separado
protected_bp = Blueprint('protected_bp', __name__)

@protected_bp.route('/api/protected', methods=['OPTIONS', 'GET'])
@jwt_required()
def protected_route():
    # Manejar solicitudes OPTIONS para preflight de CORS
    if request.method == 'OPTIONS':
        return '', 204

    # Código para manejar solicitudes GET en la ruta protegida
    user_id = get_jwt_identity()  # Obtener el ID de usuario desde el token JWT
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "This is a protected route",
        "user": {
            "id": user.id,
            "email": user.email,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
    }), 200
