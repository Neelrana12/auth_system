from flask import Flask
from flask_bcrypt import Bcrypt
import os
import traceback

app = Flask(__name__)
app.secret_key = "cyberguard_secret_2024_change_in_production"

bcrypt = Bcrypt(app)

# Error logging for debugging
@app.errorhandler(500)
def internal_error(error):
    print(f"500 ERROR: {error}")
    traceback.print_exc()
    return "Internal Server Error", 500

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)