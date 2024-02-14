from hashlib import sha256
import json

def f_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    h = sha256(usedforsecurity=True)
    h.update(password_bytes)
    hash = h.hexdigest()
    return hash

def load_from_json():
    with open('static/helping_data.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data
