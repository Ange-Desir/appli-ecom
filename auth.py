from __future__ import annotations

import hashlib
from typing import Optional

from database import execute_query, fetch_one


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_user(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "Identifiants requis."
    if role not in {"user", "admin"}:
        role = "user"
    existing = fetch_one("SELECT id FROM users WHERE username = ?", (username,))
    if existing:
        return False, "Ce nom d'utilisateur existe déjà."
    execute_query(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hash_password(password), role),
    )
    return True, "Compte créé avec succès."


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = fetch_one("SELECT * FROM users WHERE username = ?", (username.strip(),))
    if user and verify_password(password, user["password_hash"]):
        return dict(user)
    return None

