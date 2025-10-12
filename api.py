from flask import Blueprint, request, jsonify, abort
import sqlite3, os, base64,random
from datetime import datetime
from geopy.geocoders import Nominatim

api = Blueprint('api', __name__)
UPLOAD_FOLDER = 'static/uploads'
geolocator = Nominatim(user_agent="pothole-tracker")

@api.route('/api/upload', methods=['POST'])
def api_upload():
    try:
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        depth = data['depth']
        image_data = data.get('image')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Pending'

        # Reverse geocode
        location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
        address = location.raw.get("address", {})
        country = address.get("country")
        state = address.get("state")
        district = address.get("county") or address.get("district")
        city = address.get("city") or address.get("town") or address.get("village")

        # Decode image
        filename = None
        if image_data:
            image_bytes = base64.b64decode(image_data)
            filename = f"pothole_{int(datetime.now().timestamp())}_{random.randint(1000,9999)}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)

        # Save to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO potholes (image, latitude, longitude, depth, status, timestamp, country, state, district, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (filename, latitude, longitude, depth, status, timestamp, country, state, district, city))
        conn.commit()
        conn.close()

        return jsonify({"message": "Pothole uploaded successfully"}), 200

    except Exception as e:
        print("Upload failed:", e)
        abort(400, description="Upload failed")

@api.route('/api/potholes')
def api_potholes():
    query = "SELECT * FROM potholes WHERE 1=1"
    filters = []
    for field in ['country', 'state', 'district', 'city']:
        val = request.args.get(field)
        if val:
            query += f" AND {field} = ?"
            filters.append(val)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(query, filters)
    rows = c.fetchall()
    conn.close()

    return jsonify([{
        "id": r[0], "image": f"/static/uploads/{r[1]}", "lat": r[2], "lon": r[3],
        "depth": r[4], "status": r[5], "timestamp": r[6],
        "country": r[7], "state": r[8], "district": r[9], "city": r[10]
    } for r in rows])
