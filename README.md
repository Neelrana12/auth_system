# 🛡️ CyberGuard — Professional Security Operations Platform

A professional Flask-based cybersecurity web application with a modern SOC-style dashboard, role-based access control, and real-time threat monitoring.

---

## 📁 Project Structure

```
cyberguard/
├── app.py              # Flask app entry point
├── database.py         # All DB logic (SQLite helpers)
├── requirements.txt
├── routes/
│   ├── auth.py         # Login, Register, Logout
│   └── dashboard.py    # Admin & User dashboards
└── templates/
    ├── base.html           # Shared layout, CSS vars, sidebar/topbar
    ├── login.html          # Card-based login UI
    ├── register.html       # Full registration with password meter
    ├── dashboard_admin.html  # SOC dashboard (charts, logs, alerts)
    └── dashboard_user.html   # Limited personal activity view
```

---

## ⚙️ Setup & Run

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# or: source .venv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open in browser: **http://127.0.0.1:5000**

---

## 👤 Role-Based Access

| Feature                     | Admin | User |
|-----------------------------|-------|------|
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
- **Chart.js** — analytics charts (CDN)
- **Bootstrap Icons** — icon set (CDN)
