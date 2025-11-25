# Cereza

Application Streamlit centralisant la gestion des livraisons, précommandes et boutique pour les marchands Cereza.

## Fonctionnalités

- Authentification avec création de compte, rôles `admin` et `user`, stockage SQLite et mots de passe hashés.
- **Livraisons** : enregistrement via formulaire, tableau filtrable, export Excel.
- **Précommandes** : upload d'images, suivi personnel, vue admin avec réponses.
- **Boutique** : ajout de produits par les admins, catalogue utilisateur, bouton “Intéressé”.
- Interface épurée (typographie moderne, palette bicolore), formulaires `st.form`, tableaux `st.dataframe`, onglets `st.tabs`.

## Installation

```bash
git clone https://github.com/votre-compte/cereza.git
cd cereza/app
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Lancement local

```bash
streamlit run main.py
```

La base SQLite `cereza.db` et le dossier `uploads` sont créés automatiquement. Connectez-vous ou créez un compte depuis la page principale, puis accédez aux pages via la barre latérale.

## Déploiement Streamlit Cloud

1. Pousser ce dossier `app` sur GitHub.
2. Sur [share.streamlit.io](https://share.streamlit.io), créer une nouvelle application en pointant vers `main.py`.
3. Renseigner `requirements.txt` (Streamlit Cloud l’installe automatiquement).
4. Définir `app/` comme dossier de travail si nécessaire.

Les fichiers SQLite et `uploads/` sont stockés sur l’instance Streamlit Cloud ; prévoir une sauvegarde externe si besoin.

