"""
This module provides utility functions for handling
user authentication and loading data from JSON files
"""
from hashlib import sha256
import json

def f_hash(password: str) -> str:
    """
    Generates a SHA-256 hash for the given password.
    """
    password_bytes = password.encode('utf-8')
    h = sha256(usedforsecurity=True)
    h.update(password_bytes)
    hash_password = h.hexdigest()
    return hash_password

def load_from_json()-> dict:
    """
    Loads data from a JSON file.
    """

    with open('static/helping_data.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data
