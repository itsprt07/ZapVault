import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="../static")
    app.secret_key = "zapvault_secret_key_2025"

    # ✅ Upload & QR folders
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['QR_FOLDER'] = os.path.join(os.getcwd(), 'static', 'qrs')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

    # ✅ Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'zapvault.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ (Optional) Google OAuth
    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scope=["profile", "email"],
        redirect_url="/login/google/authorized"
    )
    app.register_blueprint(google_bp, url_prefix="/login")

    # ✅ Initialize DB
    db.init_app(app)

    with app.app_context():
        from .models import user, file
        db.create_all()

    # ✅ Register blueprints
    from .routes.home import home_bp
    from .routes.upload import upload_bp
    from .routes.dashboard import dashboard_bp
    from .routes.auth import auth_bp
    from .routes.actions import actions_bp
    from .routes.download import download_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(actions_bp)      # Handles expire/delete
    app.register_blueprint(download_bp)     # Handles download only

    return app
