from __future__ import annotations

import pandas as pd
import streamlit as st

from database import execute_query, fetch_all
from utils import (
    current_user,
    is_admin,
    load_css,
    require_login,
    save_uploaded_file,
)


load_css()
require_login()
user = current_user()

st.title("Précommandes Chine")


with st.form("precommande_form"):
    st.subheader("Soumettre une précommande")
    nom = st.text_input("Nom du produit", max_chars=120)
    image = st.file_uploader("Image du produit", type=["png", "jpg", "jpeg"])
    quantite = st.number_input("Quantité", min_value=1, step=1)
    commentaire = st.text_area("Commentaire")
    submitted = st.form_submit_button("Envoyer")
    if submitted:
        if not (nom and image):
            st.error("Nom et image sont obligatoires.")
        else:
            path = save_uploaded_file(image, "precommande")
            execute_query(
                """
                INSERT INTO precommandes
                (user_id, produit_nom, produit_image_path, quantite, commentaire)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user["id"], nom, path, int(quantite), commentaire),
            )
            st.success("Précommande enregistrée.")


tab_perso, tab_admin = st.tabs(["Mes précommandes", "Vue administrateur"])

with tab_perso:
    rows = fetch_all(
        """
        SELECT produit_nom, produit_image_path, quantite, commentaire, admin_msg, created_at
        FROM precommandes
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user["id"],),
    )
    df = pd.DataFrame(rows, columns=rows[0].keys()) if rows else pd.DataFrame()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune précommande pour l'instant.")


with tab_admin:
    if not is_admin():
        st.warning("Réservé aux administrateurs.")
    else:
        rows = fetch_all(
            """
            SELECT precommandes.*, users.username
            FROM precommandes
            JOIN users ON users.id = precommandes.user_id
            ORDER BY precommandes.created_at DESC
            """
        )
        df = pd.DataFrame(rows, columns=rows[0].keys()) if rows else pd.DataFrame()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            precommande_ids = df["id"].tolist()
            selection = st.selectbox("Sélectionner une précommande", precommande_ids)
            reponse = st.text_area("Réponse admin")
            if st.button("Enregistrer la réponse"):
                execute_query(
                    "UPDATE precommandes SET admin_msg = ? WHERE id = ?",
                    (reponse, int(selection)),
                )
                st.success("Réponse enregistrée.")
        else:
            st.info("Aucune précommande enregistrée.")

