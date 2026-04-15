# 🛡️ CyberGuard — Security Dashboard

A professional Flask-based security dashboard application with role-based access control, secure authentication, and audit logging.

## ✨ Key Features

✅ **Secure Authentication**
- User registration with password strength validation
- Bcrypt password hashing
- Brute-force protection (5 failed attempts → 10-minute lockout)
- Session-based authentication

✅ **Role-Based Access Control**
- **Admin**: View all logs, manage users, monitor suspicious activity
- **User**: View only their own activity and profile
- Automatic "user" role assignment on registration

✅ **Security Monitoring**
- Real-time audit logging of all activities
- IP address tracking for each login attempt
- Suspicious activity detection and flagging
- Login success/failure statistics

✅ **Professional UI/UX**
- Modern dark cybersecurity theme
- Responsive sidebar navigation
- Real-time clock display
- Color-coded status indicators
- Clean, intuitive interface

---

## 📁 Project Structure

```
cyberguard/
├── app.py                    # Flask entry point
├── database.py              # SQLite database helpers
├── requirements.txt         # Python dependencies
│
├── routes/
│   ├── __init__.py
│   ├── auth.py              # Login, Register, Logout
│   └── dashboard.py         # Admin & User dashboards
│
├── templates/               # HTML templates
│   ├── base.html            # Shared layout
│   ├── login.html
│   ├── register.html
│   ├── dashboard_admin.html
│   └── dashboard_user.html
│
└── static/css/
    └── style.css            # External stylesheet
```

---

## 🚀 Quick Start

### Requirements
- Python 3.7+
- pip

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Neelrana12/auth_system.git
cd auth_system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py
```

**Open in browser:** http://127.0.0.1:5000

---

## 👤 Default Login Credentials

```
Username: admin
Password: admin123
```

⚠️ Change these credentials in production!

---

## 🔐 User Roles & Permissions

| Feature | Admin | User |
|---------|:-----:|:----:|
| View all logs | ✅ | ❌ |
| View all users | ✅ | ❌ |
| Delete users | ✅ | ❌ |
| View suspicious activity | ✅ | ❌ |
| View personal logs | ✅ | ✅ |
| Change own password | ✅ | ✅ |

---

## 🔒 Security Architecture

**Password Security:**
- Bcrypt hashing (industry standard)
- Minimum 8 characters
- Real-time strength validation

**Login Protection:**
- Brute-force detection
- IP-based rate limiting
- Account lockout mechanism

**Data Protection:**
- SQL injection prevention
- Session-based authentication
- Audit trail logging
- Role-based access control

**Monitoring:**
- All user actions logged
- IP addresses tracked
- Failed attempts flagged
- Suspicious activity alerts

---

## 📊 Admin Dashboard

- **Overview Stats**: Users, logins, failed attempts, suspicious IPs
- **Suspicious Activity Panel**: Real-time threat alerts
- **User Management**: View and delete registered users
- **Audit Logs**: Complete activity history with timestamps and IP addresses

---

## 👤 User Dashboard

- **Personal Statistics**: Login counts and last login time
- **Activity Log**: Own login history with dates and times
- **Security Alerts**: Warning if suspicious activity detected

---

## 📝 Usage

### For Admins:
1. Login with default credentials
2. View system statistics and alerts
3. Monitor all user activities
4. Manage user accounts (view, delete)
5. Review complete audit logs

### For Users:
1. Register new account (auto-assigned "user" role)
2. Login with credentials
3. View personal login statistics
4. Check own activity logs
5. See security alerts if needed

---

## 🔄 Database Schema

**Users Table:**
- id (primary key)
- full_name
- username (unique)
- email
- password (hashed)
- role (admin/user)
- created_at
- is_locked (for brute-force protection)

**Logs Table:**
- id (primary key)
- username
- action
- ip
- status (success/danger/warning/info)
- time

**Attempts Table:**
- id (primary key)
- username
- ip
- count (failed attempts)
- last_attempt

---

## 🚨 Error Handling

- Invalid credentials → Clear error message
- Account locked → Lockout timer shown
- Missing fields → Form validation
- Unauthorized access → Redirect to login
- Database errors → Graceful fallback

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Neelrana12**

---

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Neelrana12/auth_system.git
cd auth_system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# or: source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

The app will be available at: **http://127.0.0.1:5000**

---

## 📝 Default Credentials

```
Username: admin
Password: admin123
```
---


