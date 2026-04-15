from flask import Blueprint, render_template, request, redirect, session, flash
from database import (
    get_all_logs, get_user_logs, get_all_users, get_suspicious_users,
    get_stats, delete_user, add_log
)

dashboard_bp = Blueprint("dashboard", __name__)

# Simple decorators for access control
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "error")
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session or session.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return wrapper


# Main Dashboard Route
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    username = session.get("user")
    role = session.get("role", "user")

    # Admin Dashboard
    if role == "admin":
        stats = get_stats()
        logs = get_all_logs(200)
        suspicious = get_suspicious_users(3)
        users = get_all_users()

        return render_template(
            "dashboard_admin.html",
            username=username,
            fullname=session.get("fullname", username),
            stats=stats,
            logs=logs,
            suspicious=suspicious,
            users=users,
        )
    
    # User Dashboard
    else:
        user_logs = get_user_logs(username, 50)
        success_count = sum(1 for l in user_logs if l["action"] == "Login Success")
        failed_count = sum(1 for l in user_logs if l["action"] == "Login Failed")
        last_login = next((l["time"] for l in user_logs if l["action"] == "Login Success"), "Never")

        return render_template(
            "dashboard_user.html",
            username=username,
            fullname=session.get("fullname", username),
            user_logs=user_logs,
            success_count=success_count,
            failed_count=failed_count,
            last_login=last_login,
        )


# Delete User (Admin Only)
@dashboard_bp.route("/admin/delete-user/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    users = get_all_users()
    target = next((u for u in users if u["id"] == user_id), None)
    
    if target:
        if target["username"] == session.get("user"):
            flash("Cannot delete your own account.", "error")
        else:
            delete_user(user_id)
            add_log(session.get("user"), f"Deleted user: {target['username']}", "N/A", "warning")
            flash(f"User '{target['username']}' deleted successfully.", "success")
    else:
        flash("User not found.", "error")
    
    return redirect("/dashboard")

