from flask import Flask, request, jsonify
import redis
import requests
import os
import yaml
import json

# Загрузка конфига
config_path = os.getenv("CONFIG_PATH", "/etc/cache-api/config.yaml")
try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {}

REDIS_HOST = os.getenv("REDIS_HOST", config.get("redis", {}).get("host", "localhost"))
REDIS_PORT = int(os.getenv("REDIS_PORT", config.get("redis", {}).get("port", 6379)))

BACKEND_HOST = os.getenv("BACKEND_HOST", config.get("backend", {}).get("host", "192.168.1.10"))
BACKEND_PORT = int(os.getenv("BACKEND_PORT", config.get("backend", {}).get("port", 8080)))

APP_PORT = int(os.getenv("APP_PORT", config.get("app", {}).get("port", 5000)))

app = Flask(__name__)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"error": "Missing id"}), 400

    cached = r.get(user_id)
    if cached:
        return jsonify({"cached": True, "user": json.loads(cached)})

    try:
        resp = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/user?id={user_id}")
        if resp.status_code != 200:
            return jsonify({"error": "User not found"}), 404
        user_data = resp.json()
        r.setex(user_id, 60, json.dumps(user_data))
        return jsonify({"cached": False, "user": user_data})
    except Exception as e:
        return jsonify({"error": "Backend unreachable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
