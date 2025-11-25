from __future__ import annotations

import pandas as pd
import streamlit as st

from database import execute_query, fetch_all
from utils import current_user, is_admin, load_css, require_login, save_uploaded_file


load_css()
require_login()
user = current_user()

st.title("Boutique Cereza")


if is_admin():
    with st.form("produit_form"):
        st.subheader("Ajouter un produit")
        nom = st.text_input("Nom du produit", max_chars=120)
        prix = st.number_input("Prix (€)", min_value=0.0, step=0.5, format="%.2f")
        description = st.text_area("Description")
        image = st.file_uploader("Image produit", type=["png", "jpg", "jpeg"], key="prod_image")
        submitted = st.form_submit_button("Créer")
        if submitted:
            if not (nom and image):
                st.error("Nom et image sont requis.")
            else:
                path = save_uploaded_file(image, "produit")
                execute_query(
                    """
                    INSERT INTO produits (nom, prix, description, image_path)
                    VALUES (?, ?, ?, ?)
                    """,
                    (nom, float(prix), description, path),
                )
                st.success("Produit ajouté.")
else:
    st.info("Contactez un administrateur pour ajouter des produits.")


st.subheader("Catalogue")
rows = fetch_all(
    """
    SELECT * FROM produits
    ORDER BY created_at DESC
    """
)

if rows:
    df = pd.DataFrame(rows, columns=rows[0].keys())
    for _, prod in df.iterrows():
        with st.container():
            cols = st.columns([2, 3])
            with cols[0]:
                if prod["image_path"]:
                    st.image(prod["image_path"], use_column_width=True)
            with cols[1]:
                st.markdown(f"### {prod['nom']}")
                st.markdown(f"**Prix :** {prod['prix']:.2f} €")
                st.write(prod["description"] or "Pas de description.")
                message = st.text_input(
                    "Message",
                    key=f"interest_msg_{prod['id']}",
                    placeholder="Optionnel",
                )
                if st.button("Intéressé", key=f"interest_btn_{prod['id']}"):
                    execute_query(
                        """
                        INSERT INTO interets (user_id, produit_id, message)
                        VALUES (?, ?, ?)
                        """,
                        (user["id"], int(prod["id"]), message),
                    )
                    st.success("Intérêt enregistré.")
else:
    st.info("Aucun produit pour le moment.")

