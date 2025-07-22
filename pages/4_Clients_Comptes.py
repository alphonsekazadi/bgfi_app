import streamlit as st
import pandas as pd
from database import fetch_all
from logic import creer_compte, creer_client

# Cacher header/footer/menu Streamlit par défaut
hide_streamlit_style = """
    <style>
    header, footer, #MainMenu {
        visibility: hidden;
    }
    body {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Charger CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre personnalisé dans une card bleu foncé
st.markdown("""
<div class="title-container">
    <h2>👤 Gestion des clients et des comptes</h2>
</div>
""", unsafe_allow_html=True)

agence_active = st.session_state.get("agence_active", "Agence Mbujimayi")

# Obtenir l’ID de l’agence active
query_id_agence = "SELECT id_agence FROM agence WHERE nom_agence = %s"
res = fetch_all(query_id_agence, (agence_active,))
if not res:
    st.error("Agence non trouvée.")
    st.stop()
id_agence = res[0]["id_agence"]

# ===========================
# 🔹 FORMULAIRE AJOUT CLIENT
# ===========================

st.markdown('<div class="card">', unsafe_allow_html=True)
with st.expander("➕ Ajouter un nouveau client"):
    with st.form("form_ajout_client"):
        nom = st.text_input("Nom *")
        prenom = st.text_input("Prénom *")
        telephone = st.text_input("Téléphone")
        solde_initial = st.number_input("Solde initial du compte", min_value=0.0, step=100.0, format="%.2f")

        submitted = st.form_submit_button("Créer client et compte")

        if submitted:
            if not nom.strip() or not prenom.strip():
                st.error("Veuillez remplir les champs Nom et Prénom.")
            else:
                try:
                    id_compte = creer_compte(solde_initial)
                    creer_client(nom.strip(), prenom.strip(), telephone.strip(), id_agence, id_compte)
                    st.success(f"Client {nom} {prenom} ajouté avec succès (solde initial : {solde_initial:.2f} FC).")
                except Exception as e:
                    st.error(f"Erreur : {e}")
st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# 📋 LISTE DES CLIENTS
# ===========================

st.markdown("""
<div class="title-container" style="margin-top: 30px;">
    <h2>📋 Liste des clients de l’agence</h2>
</div>
""", unsafe_allow_html=True)

query_liste = """
    SELECT cl.nom_client, cl.prenom_client, cl.telephone,
           c.id_compte, c.solde, c.statut, c.date_ouverture
    FROM client cl
    JOIN compte c ON c.id_compte = cl.id_compte
    WHERE cl.agence_rattachement = %s
    ORDER BY cl.nom_client
"""
rows = fetch_all(query_liste, (id_agence,))

if rows:
    df = pd.DataFrame(rows)
    df["date_ouverture"] = pd.to_datetime(df["date_ouverture"]).dt.strftime("%d/%m/%Y %H:%M")
    df.rename(columns={
        "nom_client": "Nom",
        "prenom_client": "Prénom",
        "telephone": "Téléphone",
        "id_compte": "N° Compte",
        "solde": "Solde (FC)",
        "statut": "Statut",
        "date_ouverture": "Date d’ouverture"
    }, inplace=True)

    # Préparer CSV pour téléchargement
    csv_data = df.to_csv(index=False).encode('utf-8')

    # Bouton téléchargement CSV au-dessus du tableau
    st.download_button(
        label="⬇️ Télécharger la liste des clients (CSV)",
        data=csv_data,
        file_name=f"clients_agence_{agence_active.replace(' ', '_')}.csv",
        mime="text/csv",
        key="download_clients"
    )

    # Tableau dans une card stylée
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun client enregistré dans cette agence.")
