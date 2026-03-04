# 🔐 Smart Thermal Home Security & Emergency Alert System

A comprehensive web-based security monitoring system designed for Raspberry Pi 4, featuring thermal sensing simulation, intrusion detection, and automated emergency alerts.

## 🌟 Features

- **User Authentication**: Secure login system with session management
- **Real-time Dashboard**: Live thermal readings (20°C-45°C) with 5-second auto-refresh
- **System Control**: ARM/DISARM functionality with visual status indicators
- **Intrusion Detection**: Simulated intrusion events with emergency notifications
- **Event Logging**: Persistent SQLite database storing all security events
- **Event History**: Complete chronological log of all intrusion events
- **Responsive Design**: Dark security-themed Bootstrap interface
- **Production Ready**: Clean code structure with comprehensive comments

## 📁 Project Structure

```
Intrusion-Detection-System-IDS-/
│
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── INSTALLATION.md            # This file
├── security_system.db         # SQLite database (auto-created)
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── login.html            # Login page
│   ├── dashboard.html        # Main dashboard
│   └── history.html          # Event history page
│
└── static/                    # Static assets
    └── style.css             # Custom CSS styling
```

## 🚀 Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for CDN resources)

### Step 1: Clone or Download the Repository

```bash
cd /path/to/your/directory
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 (Web framework)
- Werkzeug 3.0.1 (WSGI utility library)

### Step 4: Run the Application

```bash
python3 app.py
```

You should see output similar to:

```
Database initialized successfully

============================================================
Smart Thermal Home Security & Emergency Alert System
Starting Flask application...
============================================================
Login Credentials:
  Username: admin
  Password: admin123
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 5: Access the Application

Open your web browser and navigate to:

- **Local access**: http://localhost:5000
- **Network access** (from other devices on same network): http://[YOUR_PI_IP]:5000

## 🔑 Default Login Credentials

```
Username: admin
Password: admin123
```

## 📱 Usage Guide

### Dashboard

1. **System Status**: Shows whether the system is ARMED or DISARMED
2. **Thermal Reading**: Displays live simulated temperature (updates every 5 seconds)
3. **Intrusion Status**: Shows SAFE or INTRUSION DETECTED

### Control Panel

- **ARM SYSTEM**: Activates security monitoring
- **DISARM SYSTEM**: Deactivates security monitoring and clears active intrusions
- **SIMULATE INTRUSION**: Tests the intrusion detection (system must be armed)

### Event History

View all logged intrusion events with:
- Event ID
- Timestamp
- Temperature at time of intrusion
- Event status

### Intrusion Detection Workflow

1. Click **ARM SYSTEM** to activate monitoring
2. Click **SIMULATE INTRUSION** to trigger an event
3. A red alert banner appears on the dashboard
4. Event is logged to SQLite database with timestamp and temperature
5. Console displays "Emergency services notified"
6. View the event in the Event History page

## 🛠️ Configuration

### Change Admin Credentials

Edit `app.py` lines 21-22:

```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_password'
```

### Change Port Number

Edit `app.py` line 259:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Disable Debug Mode (Production)

Edit `app.py` line 259:

```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

## 🔧 Troubleshooting

### Port Already in Use

If port 5000 is already in use, either:
1. Stop the conflicting service, or
2. Change the port in `app.py` (see Configuration section)

### Database Errors

If you encounter database errors:

```bash
# Delete the database and restart
rm security_system.db
python3 app.py
```

The database will be automatically recreated.

### Permission Denied

If you get permission errors:

```bash
chmod +x app.py
```

### Cannot Connect from Other Devices

1. Ensure the Raspberry Pi firewall allows port 5000:
```bash
sudo ufw allow 5000
```

2. Find your Raspberry Pi's IP address:
```bash
hostname -I
```

## 🔒 Security Notes

- **Change default credentials** before deploying in a production environment
- Use HTTPS in production (consider using a reverse proxy like Nginx)
- Implement rate limiting for login attempts
- Use environment variables for sensitive configuration
- Keep Flask and dependencies updated

## 📊 Database Schema

### Events Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| timestamp | TEXT | Event timestamp (YYYY-MM-DD HH:MM:SS) |
| temperature | REAL | Thermal reading at event time |
| status | TEXT | Event status (e.g., "INTRUSION DETECTED") |

## 🔄 Auto-Refresh Feature

The dashboard automatically refreshes every 5 seconds to show:
- Updated thermal readings
- System status changes
- Intrusion alerts

## 🖥️ Raspberry Pi 4 Specific Notes

### Auto-Start on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/security-system.service
```

Add this content:

```ini
[Unit]
Description=Smart Thermal Security System
After=network.target

[Service]
User=pi
WorkingDirectory=/path/to/Intrusion-Detection-System-IDS-
ExecStart=/path/to/venv/bin/python3 /path/to/Intrusion-Detection-System-IDS-/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable security-system.service
sudo systemctl start security-system.service
```

## 📝 Technical Details

- **Backend**: Python 3 with Flask framework
- **Database**: SQLite3 (file-based, no server required)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.10.0
- **Session Management**: Flask sessions with secure cookies

## 🎨 Design Features

- Dark security-themed color scheme
- Responsive layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Toast notifications for user feedback
- Real-time updates without page reload
- Accessible and user-friendly interface

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review console output for error messages
3. Ensure all dependencies are properly installed

## 📄 License

This project is provided as-is for educational and personal use.

## 🔮 Future Enhancements

Potential features to add:
- Real thermal sensor integration (e.g., MLX90640)
- Email/SMS notifications
- Multiple user accounts with roles
- Camera integration
- Mobile app
- Historical data analytics
- Export functionality (CSV, PDF)

---

**Built with ❤️ for Raspberry Pi 4**

🚨 **Remember**: This is a simulation system. For real security applications, integrate actual sensors and implement professional security protocols.
