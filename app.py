from flask import Flask, render_template, request, redirect
from api import api
import os, sqlite3, random
from datetime import datetime
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

geolocator = Nominatim(user_agent="pothole-tracker")
app.register_blueprint(api)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS potholes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            latitude REAL,
            longitude REAL,
            depth INTEGER,
            status TEXT,
            timestamp TEXT,
            country TEXT,
            state TEXT,
            district TEXT,
            city TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    image = request.files['image']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    depth = request.form['depth']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate a unique image name
    filename = f"pothole_{int(datetime.now().timestamp())}_{random.randint(1000,9999)}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    # Reverse geocode
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    address = location.raw.get("address", {})
    country = address.get("country")
    state = address.get("state")
    district = address.get("county") or address.get("district")
    city = address.get("city") or address.get("town") or address.get("village")

    # Save to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO potholes (image, latitude, longitude, depth, status, timestamp, country, state, district, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (filename, latitude, longitude, depth, 'Pending', timestamp, country, state, district, city))
    conn.commit()
    conn.close()

    return redirect('/map')

if __name__ == '__main__':
    app.run(debug=True)
