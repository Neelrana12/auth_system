from flask import Blueprint, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
import re
from database import (
    get_user_by_username, get_user_by_email, create_user,
    is_account_locked, increment_attempt, reset_attempts, add_log, get_attempts
)

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

def get_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr) or "N/A"

def password_strength(password):
    """Returns (score 0-4, list of issues)."""
    issues = []
    if len(password) < 8:
        issues.append("At least 8 characters")
    if not re.search(r"[A-Z]", password):
        issues.append("One uppercase letter")
    if not re.search(r"[a-z]", password):
        issues.append("One lowercase letter")
    if not re.search(r"\d", password):
        issues.append("One number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("One special character")
    score = 5 - len(issues)
    return score, issues

# ─── Register ─────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        full_name  = request.form.get("full_name", "").strip()
        username   = request.form.get("username", "").strip()
        email      = request.form.get("email", "").strip().lower()
        password   = request.form.get("password", "")
        confirm_pw = request.form.get("confirm_password", "")

        # Validations
        if not all([full_name, username, email, password, confirm_pw]):
            flash("All fields are required.", "error")
            return render_template("register.html")

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            flash("Invalid email address.", "error")
            return render_template("register.html")

        if password != confirm_pw:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        score, issues = password_strength(password)
        if score < 3:
            flash("Weak password. Missing: " + ", ".join(issues), "error")
            return render_template("register.html")

        if get_user_by_username(username):
            flash("Username already taken.", "error")
            return render_template("register.html")

        if get_user_by_email(email):
            flash("Email already registered.", "error")
            return render_template("register.html")

        # Always assign 'user' role for new registrations (admin is predefined only)
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        create_user(full_name, username, email, hashed, role="user")
        add_log(username, "Account Registered", get_ip(), "success")

        flash("Account created! You can now log in.", "success")
        return redirect("/login")

    return render_template("register.html")


# ─── Login ───────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip       = get_ip()

        if not username or not password:
            flash("Please fill in all fields.", "error")
            return render_template("login.html")

        # Brute-force check
        locked, count = is_account_locked(username)
        if locked:
            add_log(username, "Login Blocked (Brute Force)", ip, "danger")
            flash(f"⚠️ Account locked after {count} failed attempts. Try again in 10 minutes.", "locked")
            return render_template("login.html")

        user = get_user_by_username(username)

        if user and bcrypt.check_password_hash(user["password"], password):
            reset_attempts(username)
            session["user"]     = username
            session["role"]     = user["role"]
            session["fullname"] = user["full_name"]
            add_log(username, "Login Success", ip, "success")
            flash(f"Welcome back, {user['full_name']}! 👋", "success")
            return redirect("/dashboard")
        else:
            increment_attempt(username, ip)
            attempt_row = get_attempts(username)
            remaining   = max(0, 5 - (attempt_row["count"] if attempt_row else 1))
            add_log(username, "Login Failed", ip, "danger")
            if remaining > 0:
                flash(f"Invalid credentials. {remaining} attempt(s) remaining before lockout.", "error")
            else:
                flash("Account locked due to too many failed attempts. Try again in 10 minutes.", "locked")
            return render_template("login.html")

    return render_template("login.html")


# ─── Logout ──────────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    username = session.get("user", "unknown")
    add_log(username, "Logout", get_ip(), "info")
    session.clear()
    flash("You have been logged out securely.", "success")
    return redirect("/login")
