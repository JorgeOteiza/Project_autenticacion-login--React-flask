import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.utils import generate_sitemap
from api.models import db
from api.routes import api  # Blueprint de rutas de la API
from api.admin import setup_admin
from api.commands import setup_commands
from api.login import login_bp  # Blueprint para login

app = Flask(__name__)

# Configuración de la base de datos y JWT
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev_secret_key')

db.init_app(app)
Migrate(app, db, compare_type=True)
jwt = JWTManager(app)

# Configuración de CORS: permite acceso desde el frontend
CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGIN", "https://petrifying-spooky-poltergeist-7v97v6w49rqgcp57v-3000.app.github.dev")}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Registro de Blueprints
setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api/login')
app.register_blueprint(profile_bp, url_prefix='/api')

@app.route('/')
def sitemap():
    ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    return generate_sitemap(app) if ENV == "development" else send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    return send_from_directory(static_file_dir, path)

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
