import requests
import random
import time
import base64
import os
import sqlite3

API_URL = "http://127.0.0.1:5000/api/upload"
UPLOAD_FOLDER = "project_for_contest/static/uploads"  # Adjusted to correct folder
DB_PATH = "database.db"

# Step 1: Delete old simulated potholes
def delete_simulated_potholes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM potholes WHERE status = 'Simulated'")
    conn.commit()
    conn.close()
    print("🧹 Cleared previous simulated potholes")

# Step 2: Create simulated potholes
def simulate_potholes():
    base_lat = 23.34371
    base_lon = 85.24450

    locations = [
        (
            base_lat + random.uniform(-0.0005, 0.0005),
            base_lon + random.uniform(-0.0005, 0.0005)
        )
        for _ in range(20)
    ]

    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("❌ No images found in static/uploads/")
        return

    random.shuffle(image_files)
    images = (image_files * 20)[:20]

    for i, ((lat, lon), image_file) in enumerate(zip(locations, images), 1):
        depth = random.choice([5, 10, 15, 20, 25, 30])
        image_path = os.path.join(UPLOAD_FOLDER, image_file)

        try:
            with open(image_path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"[{i}] ❌ Failed to read {image_file}: {e}")
            continue

        data = {
            "latitude": lat,
            "longitude": lon,
            "depth": depth,
            "image": img_base64
        }

        try:
            res = requests.post(API_URL, json=data)
            if res.status_code == 200:
                print(f"[{i}/20] ✅ Uploaded {image_file} → ({lat:.6f}, {lon:.6f}) | Depth: {depth} cm")
            else:
                print(f"[{i}/20] ❌ Failed upload — Status: {res.status_code}")
        except Exception as e:
            print(f"[{i}/20] ❌ Request error: {e}")

        time.sleep(1)

# Run both
delete_simulated_potholes()
simulate_potholes()
