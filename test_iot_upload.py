import requests
import base64

# Optional: load a sample image
with open("sample.png", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

# Payload (sample pothole data)
data = {
    "latitude": 23.35978,
    "longitude": 85.30891,
    "depth": 15,
    "image": img_base64
}

# Send POST request to your Flask API
response = requests.post("http://127.0.0.1:5000/api/upload", json=data)

# Show response
print(response.status_code)
print(response.json())
