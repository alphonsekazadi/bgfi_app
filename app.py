import streamlit as st
from config import AGENCES

# Configuration de la page
st.set_page_config(
    page_title="BGFi Bank – Système Réparti",
    page_icon="🏦",
    layout="wide"
)

# 🔽 Chargement du CSS externe
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 🔽 CSS supplémentaires intégrés (optionnels)
custom_css = """
    <style>
        
        /* Personnalisation du selectbox */
        .stSelectbox > div {
            background-color: white !important;
            border-radius: 10px;
            padding: 0.5rem;
            color: #003366;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 🔽 Barre latérale avec logo
st.sidebar.image("https://upload.wikimedia.org/wikipedia/fr/5/52/BGFI_logo.png", width=150)  
st.sidebar.markdown(
    "<h4 style='color:#003366;'>Choisir une agence (nœud)</h4>",
    unsafe_allow_html=True
)

selected_agence = st.sidebar.selectbox("Agence active", AGENCES)

# 🔽 Enregistrer l’agence active dans la session
st.session_state["agence_active"] = selected_agence

# 🔽 Titre principal avec style
st.markdown(f"""
    <div class="title-container">
        <h2>Système Réparti de Gestion des Transactions – BGFi Bank</h2>
        <h4>{selected_agence}</h4>
    </div>
""", unsafe_allow_html=True)

# 🔽 Message d’accueil
st.success("Bienvenue dans l’interface bancaire répartie. Utilisez le menu à gauche pour accéder aux fonctionnalités.")
