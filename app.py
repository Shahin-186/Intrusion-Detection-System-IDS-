"""
Smart Thermal Home Security & Emergency Alert System
Flask Backend Application — with real sensor integration
Sensors: MLX90640 (thermal), VL53L5CX (distance), ICM20948 (motion)
Designed for Raspberry Pi 4 + Pimoroni Breakout Garden
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import math
import threading
import time
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'thermal_security_secret_key_2026'

DATABASE = 'security_system.db'

system_state = {
    'armed': False,
    'intrusion_active': False
}

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# ── Alert thresholds ──────────────────────────────────────────────────────────
TEMP_ALERT_THRESHOLD   = 32.0   # °C
DIST_ALERT_THRESHOLD   = 800    # mm
MOTION_ALERT_THRESHOLD = 2.0    # deg/s

# ── Sensor imports ────────────────────────────────────────────────────────────
try:
    import board, busio
    import adafruit_mlx90640
    MLX_AVAILABLE = True
except Exception:
    MLX_AVAILABLE = False

try:
    from vl53l5cx import VL53L5CX
    VL53_AVAILABLE = True
except Exception:
    VL53_AVAILABLE = False

try:
    from icm20948 import ICM20948
    ICM_AVAILABLE = True
except Exception:
    ICM_AVAILABLE = False

# ── Live sensor data store ────────────────────────────────────────────────────
sensor_data = {
    "thermal":  {"frame": [25.0]*768, "min_temp": 25.0, "max_temp": 25.0, "avg_temp": 25.0},
    "distance": {"grid": [2000]*64,   "min_mm": 2000,   "max_mm": 2000,   "closest_zone": -1},
    "motion":   {"accel": {"x":0,"y":0,"z":1}, "gyro": {"x":0,"y":0,"z":0},
                 "mag": {"x":0,"y":0,"z":0}, "motion_detected": False, "motion_intensity": 0.0},
    "timestamp": 0,
}
data_lock = threading.Lock()

# ── Simulation helpers ────────────────────────────────────────────────────────
_sim_t = 0.0

def simulate_thermal():
    global _sim_t
    _sim_t += 0.1
    frame = []
    for i in range(768):
        row, col = i // 32, i % 32
        cx = 16 + 10 * math.sin(_sim_t)
        cy = 12 + 6  * math.cos(_sim_t * 0.7)
        d  = math.sqrt((col-cx)**2 + (row-cy)**2)
        frame.append(round(36.0 - d*0.8 + random.uniform(-0.3, 0.3), 2))
    return frame

def simulate_distance():
    grid = []
    for i in range(64):
        row, col = i // 8, i % 8
        d = math.sqrt((col-3.5)**2 + (row-3.5)**2)
        grid.append(int(500 + d*200 + random.randint(-30, 30)))
    return grid

def simulate_motion():
    t = time.time()
    return {
        "accel": {"x": round(math.sin(t)*0.05,4), "y": round(math.cos(t)*0.05,4), "z": 1.0},
        "gyro":  {"x": round(random.uniform(-0.5,0.5),4), "y": round(random.uniform(-0.5,0.5),4), "z": round(random.uniform(-0.5,0.5),4)},
        "mag":   {"x": round(random.uniform(-50,50),2),   "y": round(random.uniform(-50,50),2),   "z": round(random.uniform(-50,50),2)},
    }

# ── Sensor init ───────────────────────────────────────────────────────────────
def init_sensors():
    mlx = vl53 = imu = None
    if MLX_AVAILABLE:
        try:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
            mlx = adafruit_mlx90640.MLX90640(i2c)
            mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
            print("[OK] MLX90640 ready")
        except Exception as e:
            print(f"[WARN] MLX90640: {e}")
    if VL53_AVAILABLE:
        try:
            vl53 = VL53L5CX()
            vl53.set_resolution(64)
            vl53.set_ranging_frequency_hz(10)
            vl53.start_ranging()
            print("[OK] VL53L5CX ready")
        except Exception as e:
            print(f"[WARN] VL53L5CX: {e}")
    if ICM_AVAILABLE:
        try:
            imu = ICM20948()
            print("[OK] ICM20948 ready")
        except Exception as e:
            print(f"[WARN] ICM20948: {e}")
    return mlx, vl53, imu

# ── Auto intrusion detection ──────────────────────────────────────────────────
def auto_detect_intrusion(frame, grid, motion, intensity):
    if not system_state['armed'] or system_state['intrusion_active']:
        return
    hot_pixels  = sum(1 for t in frame if t > TEMP_ALERT_THRESHOLD)
    close_zones = sum(1 for d in grid  if 0 < d < DIST_ALERT_THRESHOLD)
    if hot_pixels > 10 or close_zones > 0 or intensity > MOTION_ALERT_THRESHOLD:
        system_state['intrusion_active'] = True
        avg_temp  = round(sum(frame)/len(frame), 1)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reasons = []
        if hot_pixels  > 10: reasons.append(f"thermal ({hot_pixels} hot pixels)")
        if close_zones > 0:  reasons.append(f"proximity ({close_zones} zones)")
        if intensity > MOTION_ALERT_THRESHOLD: reasons.append(f"motion ({intensity:.1f} deg/s)")
        conn = get_db_connection()
        conn.execute('INSERT INTO events (timestamp, temperature, status) VALUES (?, ?, ?)',
                     (timestamp, avg_temp, f'AUTO: {", ".join(reasons)}'))
        conn.commit()
        conn.close()
        print(f"[ALERT] Auto-detected at {timestamp}: {', '.join(reasons)}")

# ── Sensor background thread ──────────────────────────────────────────────────
def sensor_loop(mlx, vl53, imu):
    print("[INFO] Sensor loop started")
    while True:
        try:
            if mlx:
                frame = [0.0] * 768
                mlx.getFrame(frame)
            else:
                frame = simulate_thermal()

            if vl53 and vl53.data_ready():
                raw  = vl53.get_data()
                grid = list(raw.distance_mm[0])
            else:
                grid = simulate_distance()

            if imu:
                ax,ay,az,gx,gy,gz = imu.read_accelerometer_gyro_data()
                mx,my,mz = imu.read_magnetometer_data()
                motion_raw = {"accel":{"x":ax,"y":ay,"z":az},"gyro":{"x":gx,"y":gy,"z":gz},"mag":{"x":mx,"y":my,"z":mz}}
            else:
                motion_raw = simulate_motion()

            g = motion_raw["gyro"]
            intensity = math.sqrt(g["x"]**2 + g["y"]**2 + g["z"]**2)
            valid = [d for d in grid if d > 0]

            with data_lock:
                sensor_data["thermal"]  = {"frame": frame, "min_temp": round(min(frame),2),
                                            "max_temp": round(max(frame),2), "avg_temp": round(sum(frame)/len(frame),2)}
                sensor_data["distance"] = {"grid": grid, "min_mm": min(valid) if valid else 0,
                                            "max_mm": max(valid) if valid else 0,
                                            "closest_zone": grid.index(min(valid)) if valid else -1}
                sensor_data["motion"]   = {**motion_raw, "motion_detected": intensity > MOTION_ALERT_THRESHOLD,
                                            "motion_intensity": round(intensity,3)}
                sensor_data["timestamp"] = round(time.time()*1000)

            auto_detect_intrusion(frame, grid, motion_raw, intensity)

        except Exception as e:
            print(f"[ERR] {e}")
        time.sleep(0.5)

# ── Database ──────────────────────────────────────────────────────────────────
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS events
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT NOT NULL, temperature REAL NOT NULL, status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('dashboard') if session.get('logged_in') else url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username']  = request.form.get('username')
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', armed=system_state['armed'],
                           intrusion_active=system_state['intrusion_active'])

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('history.html', events=events)

# ── API ───────────────────────────────────────────────────────────────────────
@app.route('/api/status')
def api_status():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    with data_lock:
        avg_temp = sensor_data["thermal"]["avg_temp"]
        max_temp = sensor_data["thermal"]["max_temp"]
        min_mm   = sensor_data["distance"]["min_mm"]
        motion   = sensor_data["motion"]["motion_detected"]
    return jsonify({'armed': system_state['armed'], 'intrusion_active': system_state['intrusion_active'],
                    'temperature': avg_temp, 'max_temperature': max_temp,
                    'closest_mm': min_mm, 'motion_detected': motion,
                    'status': 'ARMED' if system_state['armed'] else 'DISARMED',
                    'sensors': {'mlx90640': MLX_AVAILABLE, 'vl53l5cx': VL53_AVAILABLE, 'icm20948': ICM_AVAILABLE}})

@app.route('/api/sensors')
def api_sensors():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    with data_lock:
        return jsonify(sensor_data)

@app.route('/api/arm', methods=['POST'])
def api_arm():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    system_state['armed'] = True
    system_state['intrusion_active'] = False
    return jsonify({'success': True, 'armed': True})

@app.route('/api/disarm', methods=['POST'])
def api_disarm():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    system_state['armed'] = False
    system_state['intrusion_active'] = False
    return jsonify({'success': True, 'armed': False})

@app.route('/api/simulate-intrusion', methods=['POST'])
def api_simulate_intrusion():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    if not system_state['armed']:
        return jsonify({'error': 'System must be armed to detect intrusions'}), 400
    system_state['intrusion_active'] = True
    with data_lock:
        temperature = sensor_data["thermal"]["avg_temp"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute('INSERT INTO events (timestamp, temperature, status) VALUES (?, ?, ?)',
                 (timestamp, temperature, 'INTRUSION DETECTED'))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'intrusion_active': True, 'temperature': temperature, 'timestamp': timestamp})

# ── Start ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    mlx, vl53, imu = init_sensors()
    threading.Thread(target=sensor_loop, args=(mlx, vl53, imu), daemon=True).start()
    print(f"\n{'='*60}\nIDS running | login: {ADMIN_USERNAME}/{ADMIN_PASSWORD}\n{'='*60}\n")
    app.run(host='0.0.0.0', port=5000, debug=False)    