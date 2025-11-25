from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cereza.db"


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row factory configured."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the application tables if they do not exist."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS livraisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nom_client TEXT NOT NULL,
            numero_client TEXT NOT NULL,
            adresse TEXT NOT NULL,
            nb_colis INTEGER NOT NULL,
            commentaire TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS precommandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            produit_nom TEXT NOT NULL,
            produit_image_path TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            commentaire TEXT,
            admin_msg TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            description TEXT,
            image_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS interets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
        """,
    ]

    conn = get_connection()
    cur = conn.cursor()
    for query in queries:
        cur.execute(query)
    conn.commit()
    conn.close()


def execute_query(query: str, params: Iterable[Any] = ()) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query: str, params: Iterable[Any] = ()) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return row


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


init_db()

