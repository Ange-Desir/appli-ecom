from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path
from typing import Optional
from uuid import uuid4

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
CSS_PATH = BASE_DIR / "styles.css"


def ensure_environment() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def load_css() -> None:
    if CSS_PATH.exists():
        st.markdown(
            f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def init_session_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None


def require_login() -> None:
    if not st.session_state.get("authenticated"):
        st.warning("Merci de vous connecter depuis la page principale.")
        st.stop()


def current_user() -> Optional[dict]:
    return st.session_state.get("user")


def save_uploaded_file(file, prefix: str) -> Optional[str]:
    if file is None:
        return None
    ensure_environment()
    suffix = Path(file.name).suffix
    filename = f"{prefix}_{uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / filename
    with destination.open("wb") as out:
        out.write(file.getbuffer())
    return str(destination)


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer.read()


def is_admin() -> bool:
    user = current_user()
    return bool(user and user.get("role") == "admin")


ensure_environment()

