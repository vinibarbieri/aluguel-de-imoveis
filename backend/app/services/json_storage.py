import json
import os

BASE_PATH = "data"

def load_all(file_name):
    path = os.path.join(BASE_PATH, file_name)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_all(file_name, data):
    path = os.path.join(BASE_PATH, file_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1
