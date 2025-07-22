from database import execute_query, execute_and_return_id
from datetime import datetime

# ➤ Créer un nouveau client avec son compte
def creer_client(nom, prenom, telephone, agence_id, compte_id):
    query = """
        INSERT INTO client (nom_client, prenom_client, telephone, agence_rattachement, id_compte)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (nom, prenom, telephone, agence_id, compte_id))

# ➤ Créer un compte bancaire
def creer_compte(solde_initial=0.0, statut='actif'):
    query = """
        INSERT INTO compte (solde, statut)
        VALUES (%s, %s)
        RETURNING id_compte
    """
    return execute_and_return_id(query, (solde_initial, statut))

# ➤ Enregistrer un dépôt ou un retrait
def enregistrer_transaction(type_transaction, montant, id_compte, agence, statut='validee'):
    # 1. Enregistrement de la transaction
    tx_query = """
        INSERT INTO transaction (type_transaction, montant, id_compte, etat_transaction)
        VALUES (%s, %s, %s, %s)
        RETURNING id_transaction
    """
    id_transaction = execute_and_return_id(tx_query, (type_transaction, montant, id_compte, statut))

    # 2. Mise à jour du solde
    if type_transaction == "depot":
        solde_query = "UPDATE compte SET solde = solde + %s WHERE id_compte = %s"
    elif type_transaction == "retrait":
        solde_query = "UPDATE compte SET solde = solde - %s WHERE id_compte = %s"
    else:
        raise ValueError("Type de transaction non valide")

    execute_query(solde_query, (montant, id_compte))

    # 3. Journalisation
    journaliser_event(id_transaction, f"{type_transaction.capitalize()} de {montant:.2f} FC", agence)

    return id_transaction

# ➤ Virement (de compte A vers B)
def effectuer_virement(montant, compte_src, compte_dest, agence):
    try:
        # 1. Débiter source
        enregistrer_transaction("retrait", montant, compte_src, agence)

        # 2. Créditer destination
        enregistrer_transaction("depot", montant, compte_dest, agence)

        # 3. Journal global
        journaliser_event(None, f"Virement de {montant:.2f} FC du compte {compte_src} vers {compte_dest}", agence)
        return True
    except Exception as e:
        print("Erreur virement :", e)
        return False

# ➤ Journalisation des opérations
def journaliser_event(id_transaction, message, agence):
    query = """
        INSERT INTO journal (evenement, id_transaction, horodatage, noeud_source)
        VALUES (%s, %s, %s, %s)
    """
    execute_query(query, (message, id_transaction, datetime.now(), agence))
 
