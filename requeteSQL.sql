-- Table des agences
CREATE TABLE agence (
    id_agence SERIAL PRIMARY KEY,
    nom_agence VARCHAR(100) NOT NULL,
    localisation VARCHAR(100) NOT NULL
);

-- Table des comptes
CREATE TABLE compte (
    id_compte SERIAL PRIMARY KEY,
    solde NUMERIC(15, 2) NOT NULL DEFAULT 0,
    date_ouverture TIMESTAMP NOT NULL DEFAULT NOW(),
    statut VARCHAR(20) CHECK (statut IN ('actif', 'inactif', 'cloture')) NOT NULL
);

-- Table des clients
CREATE TABLE client (
    id_client SERIAL PRIMARY KEY,
    nom_client VARCHAR(100) NOT NULL,
    prenom_client VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    agence_rattachement INTEGER REFERENCES agence(id_agence),
    id_compte INTEGER REFERENCES compte(id_compte)
);

-- Table des transactions
CREATE TABLE transaction (
    id_transaction SERIAL PRIMARY KEY,
    type_transaction VARCHAR(20) CHECK (type_transaction IN ('depot', 'retrait', 'virement')),
    montant NUMERIC(15, 2) NOT NULL CHECK (montant > 0),
    date_heure TIMESTAMP NOT NULL DEFAULT NOW(),
    etat_transaction VARCHAR(20) CHECK (etat_transaction IN ('validee', 'refusee', 'en_attente')),
    id_compte INTEGER REFERENCES compte(id_compte)
);

-- Journal des événements
CREATE TABLE journal (
    id_journal SERIAL PRIMARY KEY,
    evenement TEXT NOT NULL,
    id_transaction INTEGER REFERENCES transaction(id_transaction),
    horodatage TIMESTAMP NOT NULL DEFAULT NOW(),
    noeud_source VARCHAR(50) NOT NULL -- nom ou ID de l’agence/nœud
);
