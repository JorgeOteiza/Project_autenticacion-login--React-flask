from flask import Flask, request, jsonify
from models import db, User
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)

# Configura la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gitpod:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201