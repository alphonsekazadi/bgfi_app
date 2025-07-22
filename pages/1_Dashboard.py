import streamlit as st
import pandas as pd
from database import fetch_one, fetch_all

# Charger CSS personnalisé pour les cards, grids, etc.
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("### 📊 Tableau de bord de l’agence")

agence_active = st.session_state.get("agence_active", "Agence Mbujimayi")

# Récupérer ID de l'agence
query_id_agence = "SELECT id_agence FROM agence WHERE nom_agence = %s"
result = fetch_one(query_id_agence, (agence_active,))
id_agence = result["id_agence"] if result else None

if id_agence:
    # Récupération des données
    nb_clients = fetch_one("SELECT COUNT(*) FROM client WHERE agence_rattachement = %s", (id_agence,))
    query_solde = """
        SELECT SUM(c.solde) AS total
        FROM compte c
        JOIN client cl ON cl.id_compte = c.id_compte
        WHERE cl.agence_rattachement = %s
    """
    total_solde = fetch_one(query_solde, (id_agence,))
    query_tx = """
        SELECT COUNT(*) FROM transaction t
        JOIN client cl ON cl.id_compte = t.id_compte
        WHERE cl.agence_rattachement = %s
    """
    nb_tx = fetch_one(query_tx, (id_agence,))
    query_pie = """
        SELECT type_transaction, COUNT(*) as total
        FROM transaction t
        JOIN client cl ON cl.id_compte = t.id_compte
        WHERE cl.agence_rattachement = %s
        GROUP BY type_transaction
    """
    rows = fetch_all(query_pie, (id_agence,))

    # Création de 2 colonnes côte à côte
    col1, col2 = st.columns(2)

    # Cards dans colonne 1
    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h4>👥 Nombre de clients</h4>
                <p class="metric">{nb_clients['count']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="card">
                <h4>💰 Solde total</h4>
                <p class="metric">{total_solde['total'] or 0:,.2f} FC</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Cards dans colonne 2
    with col2:
        st.markdown(
            f"""
            <div class="card">
                <h4>🔁 Transactions</h4>
                <p class="metric">{nb_tx['count']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Section graphique en pleine largeur, sous les deux colonnes
    st.markdown("---")
    st.markdown("#### 📈 Répartition des transactions")

    if rows:
        df_pie = pd.DataFrame(rows)
        st.plotly_chart({
            "data": [{
                "type": "pie",
                "labels": df_pie["type_transaction"],
                "values": df_pie["total"],
                "textinfo": "label+percent"
            }],
            "layout": {"margin": {"t": 10, "b": 10}}
        }, use_container_width=True)
    else:
        st.info("Aucune transaction enregistrée pour cette agence.")
else:
    st.warning("Agence inconnue.")
