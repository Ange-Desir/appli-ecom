from __future__ import annotations

import streamlit as st

from auth import authenticate_user, create_user
from utils import init_session_state, load_css


st.set_page_config(
    page_title="Cereza",
    page_icon="C",
    layout="wide",
)

init_session_state()
load_css()


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.experimental_rerun()


def show_authenticated_home() -> None:
    user = st.session_state.user
    st.success(f"Bienvenue {user['username']} ({user['role']})")
    st.write(
        "Utilisez la barre latérale pour naviguer entre les pages "
        "Livraison, Précommande et Boutique."
    )
    st.info(
        "Vos données sont stockées localement dans SQLite et resteront disponibles "
        "lors de vos prochaines connexions."
    )
    st.button("Se déconnecter", on_click=logout)


def show_auth_forms() -> None:
    tab_login, tab_register = st.tabs(["Connexion", "Créer un compte"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter")
        if submitted:
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.experimental_rerun()
            else:
                st.error("Identifiants invalides.")

    with tab_register:
        with st.form("register_form"):
            username = st.text_input("Nom d'utilisateur", key="reg_username")
            password = st.text_input("Mot de passe", type="password", key="reg_password")
            role = st.selectbox(
                "Rôle",
                options=["user", "admin"],
                help="Réservé aux administrateurs autorisés.",
            )
            submitted = st.form_submit_button("Créer un compte")
        if submitted:
            ok, message = create_user(username, password, role)
            if ok:
                st.success(message)
            else:
                st.error(message)


st.title("Cereza · Console Opérationnelle")
st.caption("Gestion unifiée des livraisons, précommandes et boutique.")

if st.session_state.authenticated:
    show_authenticated_home()
else:
    show_auth_forms()

