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

## 🎨 Design

- **Theme**: Dark cybersecurity aesthetic
- **Typography**: Inter & JetBrains Mono fonts
- **Framework**: Bootstrap 5 + Bootstrap Icons
- **Colors**: 
  - Green (#00ff88) for success
  - Red (#ff4757) for danger/errors
  - Yellow (#ffa502) for warnings
  - Cyan (#00d4ff) for accents

---

## 📦 Dependencies

```python
Flask==3.1.0                 # Web framework
Flask-Bcrypt==1.0.1         # Password hashing
SQLite3                      # Database (built-in)
Bootstrap 5 (CDN)           # Frontend framework
Bootstrap Icons (CDN)       # Icon library
```

---

## 🛠️ Configuration

### Change Secret Key (Required for Production)

Edit `app.py`:
```python
app.secret_key = "your-very-long-random-secret-key-here"
```

### Database
SQLite database (`cyberguard.db`) is created automatically on first run.
Default admin user is also created automatically.

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

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements!

---

## 📞 Support

For issues or questions, open an issue on GitHub.
# 🛡️ CyberGuard — Security Dashboard with Role-Based Access Control

A professional Flask-based security dashboard application with admin and user role management, audit logging, and threat monitoring.

## ✨ Features

✅ **Authentication System**
- User registration with password strength validation
- Secure login with bcrypt hashing
- Brute-force protection (5 failed attempts = 10-minute account lock)
- Session-based authentication

✅ **Role-Based Access Control**
- **Admin**: Full system access - view all logs, manage users, monitor threats
- **User**: Limited access - view only their own activity
- Automatic role assignment (new users = "user" role)

✅ **Security Monitoring**
- Real-time audit logging of all activities
- IP address tracking for each login
- Suspicious activity flagging (5+ failed attempts)
- Login success/failure tracking

✅ **User Management**
- Admin can view all registered users
- Delete user functionality with confirmation
- User activity history

✅ **Professional UI/UX**
- Modern dark cybersecurity theme
- Responsive sidebar navigation
- Real-time clock display
- Color-coded status indicators (Green: success, Red: danger, Yellow: warning)

---

## 📁 Project Structure

```
cyberguard/
├── app.py                    # Flask application entry point
├── database.py              # SQLite database management
├── requirements.txt         # Python dependencies
│
├── routes/
│   ├── __init__.py          # Routes package
│   ├── auth.py              # Login, Register, Logout routes
│   └── dashboard.py         # Admin & User dashboard routes
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Shared layout, sidebar, topbar
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard_admin.html # Admin dashboard
│   └── dashboard_user.html  # User dashboard
│
└── static/
    └── css/
        └── style.css        # External stylesheet (dark theme)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

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

> ⚠️ Change these credentials in production!

---

## 🔐 Role-Based Features

| Feature | Admin | User |
|---------|:-----:|:----:|
| View all logs               | ✅    | ❌   |
| View suspicious IPs/users   | ✅    | ❌   |
| Analytics charts            | ✅    | ❌   |
| Delete users                | ✅    | ❌   |
| View own activity           | ✅    | ✅   |

During registration, select **Admin** or **User** role.

---

## 🔐 Security Features

- **bcrypt** password hashing (industry standard)
- **Brute-force protection**: account locked after 5 failed attempts (10-min cooldown)
- **IP tracking** for all login events
- **Audit logging**: every action is timestamped and stored
- **Role-based route protection**: decorators enforce access control
- **Password strength meter**: real-time client-side validation
- **Session management**: server-side session with secret key

---

## 📊 Dashboard Features (Admin)

- **Overview Cards**: Total users, logins, failed attempts, suspicious IPs
- **Login Trend Chart**: 7-day line chart (success vs failed)
- **Success Ratio Donut**: visual breakdown
- **Suspicious Activity Panel**: color-coded threat alerts
- **User Management**: view and delete users
- **Audit Logs Table**: searchable, filterable, 200-record history

---

## 🎨 UI/UX

- Dark cybersecurity theme with CSS custom properties
- JetBrains Mono for code/IP display
- Inter font for clean readability
- Responsive sidebar navigation
- Flash message system (success/error/warning/locked)
- Smooth scroll navigation
- Real-time clock in topbar
- Bootstrap 5 + Bootstrap Icons
- Chart.js for all analytics

---

## 🔧 Configuration

In `app.py`, change the secret key before deploying:
```python
app.secret_key = "your-very-long-random-secret-here"
```

---

## 📦 Dependencies

- **Flask** — lightweight web framework
- **Flask-Bcrypt** — password hashing
- **SQLite** — embedded database (no setup needed)
- **Bootstrap 5** — responsive UI (CDN)
- **Bootstrap Icons** — icon set (CDN)
