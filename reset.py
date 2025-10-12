import os
import sqlite3

# Delete DB
if os.path.exists("database.db"):
    os.remove("database.db")
    print("✅ Deleted database.db")

# Recreate empty DB
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE potholes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT, latitude REAL, longitude REAL,
        depth INTEGER, status TEXT, timestamp TEXT,
        country TEXT, state TEXT, district TEXT, city TEXT
    )
''')
conn.commit()
conn.close()
print("✅ Recreated fresh pothole table")

# Clear uploaded images
upload_dir = "static/uploads"
for f in os.listdir(upload_dir):
    os.remove(os.path.join(upload_dir, f))
print("✅ Cleared uploaded images")
