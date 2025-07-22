import streamlit as st
from database import fetch_all
from logic import enregistrer_transaction, effectuer_virement

# --- Cacher le header et footer Streamlit par défaut ---
hide_streamlit_style = """
    <style>
    /* Masquer header, footer, menu hamburger */
    header, footer, #MainMenu {
        visibility: hidden;
    }
    /* Style du body */
    body {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Charger CSS personnalisée
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre personnalisé dans une card bleue foncée
st.markdown("""
<div class="title-container">
    <h2>💳 Opérations bancaires</h2>
</div>
""", unsafe_allow_html=True)

agence_active = st.session_state.get("agence_active", "Agence Mbujimayi")

# Récupérer les comptes de l’agence active
query = """
    SELECT c.id_compte, CONCAT(cl.nom_client, ' ', cl.prenom_client, ' (Solde: ', c.solde, ' FC)') AS libelle
    FROM compte c
    JOIN client cl ON cl.id_compte = c.id_compte
    JOIN agence a ON a.id_agence = cl.agence_rattachement
    WHERE a.nom_agence = %s
"""
comptes = fetch_all(query, (agence_active,))
compte_options = {row['libelle']: row['id_compte'] for row in comptes}

if not comptes:
    st.warning("Aucun compte trouvé pour cette agence.")
    st.stop()

# Formulaire dans une card avec styles
st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("form_transaction"):
    operation = st.radio(
        "Type d’opération",
        ["Dépôt", "Retrait", "Virement"],
        label_visibility="visible",
        horizontal=True
    )
    montant = st.number_input("Montant (FC)", min_value=100.0, step=100.0, format="%.2f")

    if operation in ["Dépôt", "Retrait"]:
        compte = st.selectbox("Compte concerné", list(compte_options.keys()))
        id_compte = compte_options[compte]
    elif operation == "Virement":
        col1, col2 = st.columns(2)
        with col1:
            compte_src = st.selectbox("Compte source", list(compte_options.keys()), key="src")
        with col2:
            compte_dest = st.selectbox("Compte destination", list(compte_options.keys()), key="dest")
        id_src = compte_options[compte_src]
        id_dest = compte_options[compte_dest]

    submitted = st.form_submit_button("Valider l’opération", help="Cliquez pour valider la transaction", use_container_width=True)

    if submitted:
        try:
            if operation == "Dépôt":
                enregistrer_transaction("depot", montant, id_compte, agence_active)
                st.success(f"Dépôt de {montant:.2f} FC effectué avec succès.")
            elif operation == "Retrait":
                enregistrer_transaction("retrait", montant, id_compte, agence_active)
                st.success(f"Retrait de {montant:.2f} FC effectué avec succès.")
            elif operation == "Virement":
                if id_src == id_dest:
                    st.error("Le compte source et le compte destination doivent être différents.")
                else:
                    ok = effectuer_virement(montant, id_src, id_dest, agence_active)
                    if ok:
                        st.success(f"Virement de {montant:.2f} FC réussi.")
                    else:
                        st.error("Erreur lors du virement.")
        except Exception as e:
            st.error(f"Erreur : {e}")
st.markdown('</div>', unsafe_allow_html=True)
