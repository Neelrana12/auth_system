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
        
        # Format log timestamps for display
        for log in logs:
            if hasattr(log["time"], 'strftime'):
                log["time"] = log["time"].strftime("%Y-%m-%d %H:%M:%S")
            else:
                log["time"] = str(log["time"])[:19]
        
        suspicious = get_suspicious_users(3)
        
        # Format suspicious users' last_attempt timestamps
        for s in suspicious:
            if hasattr(s["last_attempt"], 'strftime'):
                s["last_attempt"] = s["last_attempt"].strftime("%Y-%m-%d %H:%M")
            else:
                s["last_attempt"] = str(s["last_attempt"])[:16]
        
        users = get_all_users()
        
        # Format users' created_at timestamps
        for u in users:
            if hasattr(u["created_at"], 'strftime'):
                u["created_at"] = u["created_at"].strftime("%Y-%m-%d")
            else:
                u["created_at"] = str(u["created_at"])[:10]

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
        
        # Format log timestamps for display
        for log in user_logs:
            if hasattr(log["time"], 'strftime'):
                log["time"] = log["time"].strftime("%Y-%m-%d %H:%M:%S")
            else:
                log["time"] = str(log["time"])[:19]
        
        success_count = sum(1 for l in user_logs if l["action"] == "Login Success")
        failed_count = sum(1 for l in user_logs if l["action"] == "Login Failed")
        
        # Get last login time and format it
        last_login_obj = next((l for l in user_logs if l["action"] == "Login Success"), None)
        last_login = last_login_obj["time"] if last_login_obj else "Never"

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

