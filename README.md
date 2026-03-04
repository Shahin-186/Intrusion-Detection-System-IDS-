# 🔐 Smart Thermal Home Security & Emergency Alert System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-Educational-orange.svg)
![Raspberry Pi](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-red.svg)

A complete, production-ready web-based intrusion detection and thermal monitoring system designed for Raspberry Pi 4. Features real-time thermal sensor simulation, automated emergency alerts, and comprehensive event logging.

## 📸 Features Overview

✅ **User Authentication** - Secure login with session management  
✅ **Real-Time Dashboard** - Live thermal readings (20°C-45°C) with 5-second auto-refresh  
✅ **System Control** - ARM/DISARM functionality with visual indicators  
✅ **Intrusion Detection** - Automated event detection with emergency notifications  
✅ **Event Logging** - Persistent SQLite database for all security events  
✅ **Event History** - Complete chronological log viewer  
✅ **Responsive Design** - Dark security-themed Bootstrap interface  
✅ **Production Ready** - Clean code with comprehensive comments

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python3 app.py
```

### 3. Access the System

Open your browser and go to: **http://localhost:5000**

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 📁 Project Structure

```
Intrusion-Detection-System-IDS-/
├── app.py                    # Flask backend with all routes and logic
├── requirements.txt          # Python dependencies
├── start.sh                 # Auto-install and startup script
├── QUICKSTART.md            # Quick start guide
├── INSTALLATION.md          # Detailed installation guide
├── README.md                # This file
├── security_system.db       # SQLite database (auto-created)
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── login.html          # Login page
│   ├── dashboard.html      # Main dashboard
│   └── history.html        # Event history page
└── static/                  # Static assets
    └── style.css           # Custom dark-themed CSS
```

## 🎯 How to Use

### Dashboard Operations

1. **ARM SYSTEM** - Activate security monitoring
2. **DISARM SYSTEM** - Deactivate monitoring and clear alerts
3. **SIMULATE INTRUSION** - Test the intrusion detection system

### Testing Intrusion Detection

1. Click **ARM SYSTEM** button (status changes to ARMED)
2. Click **SIMULATE INTRUSION** button
3. Red alert banner appears: "INTRUSION DETECTED!"
4. Console displays: "Emergency services notified"
5. Event logged to database with timestamp and temperature
6. View event in **Event History** page

## 🛠️ Technical Stack

- **Backend**: Python 3 + Flask 3.0.0
- **Database**: SQLite3 (file-based, no server required)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0 + Bootstrap Icons
- **Session Management**: Flask sessions with secure cookies

## 📊 Database Schema

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| timestamp | TEXT | Event timestamp (YYYY-MM-DD HH:MM:SS) |
| temperature | REAL | Thermal reading at event time (°C) |
| status | TEXT | Event status ("INTRUSION DETECTED") |

## 🔧 Configuration

### Change Admin Credentials

Edit `app.py` (lines 21-22):

```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_password'
```

### Change Port

Edit `app.py` (line 259):

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Production Mode

Set `debug=False` in production:

```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

## 🔒 Security Features

- Session-based authentication
- Secure cookie management
- SQL injection protection (parameterized queries)
- Input validation on all forms
- Auto-logout on session expiry

## 📱 Screenshots & Demo

### Login Page
- Secure authentication with error handling
- Dark security-themed design
- Responsive layout

### Dashboard
- Real-time system status (ARMED/DISARMED)
- Live thermal readings with auto-refresh
- Intrusion status indicator
- Control panel with action buttons
- Red alert banner on intrusion detection

### Event History
- Complete log of all events
- Sortable table with ID, timestamp, temperature, status
- Statistics summary cards
- Empty state with helpful message

## 🔄 Auto-Refresh Feature

Dashboard automatically updates every 5 seconds:
- Thermal readings
- System status
- Intrusion alerts
- Last update timestamp

## 🧪 Testing

### Manual Test Procedure

1. Start application: `python3 app.py`
2. Login with admin credentials
3. Verify dashboard loads correctly
4. Test ARM button - status should change to ARMED
5. Test DISARM button - status should change to DISARMED
6. ARM system, then click SIMULATE INTRUSION
7. Verify red alert banner appears
8. Check console for "Emergency services notified"
9. Navigate to Event History
10. Verify event is logged with correct data

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to dashboard or login |
| `/login` | GET/POST | Login page and authentication |
| `/logout` | GET | Clear session and logout |
| `/dashboard` | GET | Main dashboard page |
| `/history` | GET | Event history page |
| `/api/status` | GET | Get current system status (JSON) |
| `/api/arm` | POST | Arm the security system |
| `/api/disarm` | POST | Disarm the security system |
| `/api/simulate-intrusion` | POST | Trigger intrusion event |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

### Database Errors
```bash
# Delete and recreate database
rm security_system.db
python3 app.py
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 🚀 Deployment on Raspberry Pi

### Auto-Start on Boot

Create systemd service:

```bash
sudo nano /etc/systemd/system/security-system.service
```

Add:

```ini
[Unit]
Description=Smart Thermal Security System
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Intrusion-Detection-System-IDS-
ExecStart=/usr/bin/python3 /home/pi/Intrusion-Detection-System-IDS-/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl enable security-system.service
sudo systemctl start security-system.service
```

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 3 steps
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide

## 🔮 Future Enhancements

- [ ] Real thermal sensor integration (MLX90640)
- [ ] Email/SMS notifications
- [ ] Multi-user support with roles
- [ ] Camera integration
- [ ] Mobile app
- [ ] Data analytics and charts
- [ ] Export functionality (CSV, PDF)
- [ ] Custom alert thresholds
- [ ] Zone-based monitoring

## 🤝 Contributing

This is an educational project. Feel free to fork and customize for your needs.

## 📄 License

Educational and personal use. Modify as needed for your projects.

## ⚠️ Disclaimer

This is a **simulation system** for educational purposes. For real security applications, integrate actual sensors and implement professional security protocols.

## 📞 Support

- Check console output for error messages
- Review INSTALLATION.md for detailed setup instructions
- Ensure all dependencies are properly installed
- Verify Python 3.8+ is installed

---

**Built for Raspberry Pi 4** | **Flask + SQLite + Bootstrap** | **2026**

🔥 **Ready to deploy!** All files are production-ready with clean code and comprehensive comments.
