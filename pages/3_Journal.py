import streamlit as st
import pandas as pd
from database import fetch_all

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
    <h2>📜 Journal des opérations enregistrées</h2>
</div>
""", unsafe_allow_html=True)

agence_active = st.session_state.get("agence_active", "Agence Mbujimayi")

# Requête du journal filtrée sur l'agence
query = """
    SELECT j.id_journal, j.evenement, j.id_transaction, j.horodatage
    FROM journal j
    WHERE j.noeud_source = %s
    ORDER BY j.horodatage DESC
"""
journal_rows = fetch_all(query, (agence_active,))

if journal_rows:
    df = pd.DataFrame(journal_rows)
    df["horodatage"] = pd.to_datetime(df["horodatage"]).dt.strftime("%d/%m/%Y %H:%M:%S")

    # Préparer le CSV à télécharger
    csv_data = df.to_csv(index=False).encode('utf-8')

    # Bouton de téléchargement
    st.download_button(
        label="⬇️ Télécharger le rapport CSV",
        data=csv_data,
        file_name=f"journal_operations_{agence_active.replace(' ', '_')}.csv",
        mime='text/csv',
        key="download_journal"
    )

    # Encapsuler le tableau dans une card stylée
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Aucun événement journalisé pour cette agence.")
