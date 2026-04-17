from flask import Flask
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_change_in_production")

bcrypt = Bcrypt(app)

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)