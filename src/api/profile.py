from flask import Blueprint, request, jsonify

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['GET'])
def profile():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.split(" ")[1] == "fake-jwt-token":
        return jsonify({"id": 1, "email": "usuario@example.com"}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401
