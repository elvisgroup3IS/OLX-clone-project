from hashlib import sha256

def f_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    h = sha256(usedforsecurity=True)
    h.update(password_bytes)
    hash = h.hexdigest()
    return hash