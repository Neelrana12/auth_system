from flask import Flask
from flask_bcrypt import Bcrypt
from database import init_db

app = Flask(__name__)
app.secret_key = "cyberguard_secret_2024_change_in_production"

bcrypt = Bcrypt(app)

# Initialize database
init_db()

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
