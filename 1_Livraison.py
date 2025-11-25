from __future__ import annotations

import pandas as pd
import streamlit as st

from database import execute_query, fetch_all
from utils import current_user, dataframe_to_excel_bytes, load_css, require_login


load_css()
require_login()
user = current_user()

st.title("Gestion des livraisons")


with st.form("livraison_form"):
    st.subheader("Nouvelle livraison")
    nom_client = st.text_input("Nom du client", max_chars=120)
    numero_client = st.text_input("Numéro du client", max_chars=50)
    adresse = st.text_area("Adresse du client", max_chars=250)
    nb_colis = st.number_input("Nombre de colis", min_value=1, step=1)
    commentaire = st.text_area("Commentaire", max_chars=300)
    submitted = st.form_submit_button("Enregistrer")
    if submitted:
        if nom_client and numero_client and adresse:
            execute_query(
                """
                INSERT INTO livraisons
                (user_id, nom_client, numero_client, adresse, nb_colis, commentaire)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user["id"], nom_client, numero_client, adresse, int(nb_colis), commentaire),
            )
            st.success("Livraison enregistrée.")
        else:
            st.error("Merci de remplir les champs obligatoires.")


st.subheader("Tableau des livraisons")
filter_text = st.text_input("Filtrer par client ou numéro")

if user["role"] == "admin":
    rows = fetch_all(
        """
        SELECT livraisons.*, users.username
        FROM livraisons
        JOIN users ON users.id = livraisons.user_id
        ORDER BY livraisons.created_at DESC
        """
    )
else:
    rows = fetch_all(
        """
        SELECT * FROM livraisons
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user["id"],),
    )

df = pd.DataFrame(rows, columns=rows[0].keys()) if rows else pd.DataFrame()
if not df.empty:
    if filter_text:
        mask = df["nom_client"].str.contains(filter_text, case=False, na=False) | df[
            "numero_client"
        ].str.contains(filter_text, case=False, na=False)
        df = df[mask]
    st.dataframe(df, use_container_width=True)
    excel_bytes = dataframe_to_excel_bytes(df)
    st.download_button(
        "Exporter en Excel",
        data=excel_bytes,
        file_name="livraisons.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("Aucune livraison enregistrée pour le moment.")

