"""
Smart Thermal Home Security & Emergency Alert System
Flask Backend Application
Designed for Raspberry Pi 4
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import random
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'thermal_security_secret_key_2026'  # Secret key for session management

# Database configuration
DATABASE = 'security_system.db'

# System state (stored in memory - would persist across server restarts in production)
system_state = {
    'armed': False,
    'intrusion_active': False
}

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


def get_db_connection():
    """
    Create and return a database connection
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """
    Initialize the SQLite database with required tables
    Creates the events table if it doesn't exist
    """
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully")


@app.route('/')
def index():
    """
    Root route - redirects to dashboard if logged in, otherwise to login
    """
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page route
    Handles both GET (display form) and POST (process login) requests
    """
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verify credentials against hardcoded admin account
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """
    Logout route - clears session and redirects to login
    """
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    """
    Main dashboard page
    Requires authentication - redirects to login if not logged in
    """
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         armed=system_state['armed'],
                         intrusion_active=system_state['intrusion_active'])


@app.route('/api/status')
def api_status():
    """
    API endpoint to get current system status and thermal reading
    Returns JSON data for AJAX requests
    """
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Generate random thermal reading between 20°C and 45°C
    temperature = round(random.uniform(20.0, 45.0), 1)
    
    return jsonify({
        'armed': system_state['armed'],
        'intrusion_active': system_state['intrusion_active'],
        'temperature': temperature,
        'status': 'ARMED' if system_state['armed'] else 'DISARMED'
    })


@app.route('/api/arm', methods=['POST'])
def api_arm():
    """
    API endpoint to arm the security system
    """
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    system_state['armed'] = True
    system_state['intrusion_active'] = False  # Clear any active intrusion when arming
    print("System ARMED")
    
    return jsonify({'success': True, 'armed': True})


@app.route('/api/disarm', methods=['POST'])
def api_disarm():
    """
    API endpoint to disarm the security system
    """
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    system_state['armed'] = False
    system_state['intrusion_active'] = False  # Clear any active intrusion when disarming
    print("System DISARMED")
    
    return jsonify({'success': True, 'armed': False})


@app.route('/api/simulate-intrusion', methods=['POST'])
def api_simulate_intrusion():
    """
    API endpoint to simulate an intrusion event
    Only triggers if system is armed
    Logs event to database and simulates emergency services notification
    """
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Only trigger intrusion if system is armed
    if not system_state['armed']:
        return jsonify({'error': 'System must be armed to detect intrusions'}), 400
    
    # Activate intrusion state
    system_state['intrusion_active'] = True
    
    # Generate thermal reading at time of intrusion
    temperature = round(random.uniform(20.0, 45.0), 1)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'INTRUSION DETECTED'
    
    # Log event to database
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, temperature, status) VALUES (?, ?, ?)',
                 (timestamp, temperature, status))
    conn.commit()
    conn.close()
    
    # Simulate emergency services notification
    print("=" * 60)
    print("🚨 ALERT: INTRUSION DETECTED!")
    print(f"Time: {timestamp}")
    print(f"Temperature: {temperature}°C")
    print("Emergency services notified")
    print("=" * 60)
    
    return jsonify({
        'success': True, 
        'intrusion_active': True,
        'temperature': temperature,
        'timestamp': timestamp
    })


@app.route('/history')
def history():
    """
    Event history page
    Display all logged intrusion events from the database
    Requires authentication
    """
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    # Retrieve all events from database, ordered by most recent first
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY id DESC').fetchall()
    conn.close()
    
    return render_template('history.html', events=events)


if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    print("\n" + "=" * 60)
    print("Smart Thermal Home Security & Emergency Alert System")
    print("Starting Flask application...")
    print("=" * 60)
    print("Login Credentials:")
    print(f"  Username: {ADMIN_USERNAME}")
    print(f"  Password: {ADMIN_PASSWORD}")
    print("=" * 60 + "\n")
    
    # Run Flask development server
    # For Raspberry Pi, set host='0.0.0.0' to allow external connections
    app.run(host='0.0.0.0', port=5000, debug=True)
