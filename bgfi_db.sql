PGDMP      5                }            bgfi_db    17.5    17.5 +    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16387    bgfi_db    DATABASE     z   CREATE DATABASE bgfi_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE bgfi_db;
                     postgres    false            �            1259    16389    agence    TABLE     �   CREATE TABLE public.agence (
    id_agence integer NOT NULL,
    nom_agence character varying(100) NOT NULL,
    localisation character varying(100) NOT NULL
);
    DROP TABLE public.agence;
       public         heap r       postgres    false            �            1259    16388    agence_id_agence_seq    SEQUENCE     �   CREATE SEQUENCE public.agence_id_agence_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.agence_id_agence_seq;
       public               postgres    false    218            �           0    0    agence_id_agence_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.agence_id_agence_seq OWNED BY public.agence.id_agence;
          public               postgres    false    217            �            1259    16406    client    TABLE     �   CREATE TABLE public.client (
    id_client integer NOT NULL,
    nom_client character varying(100) NOT NULL,
    prenom_client character varying(100) NOT NULL,
    telephone character varying(20),
    agence_rattachement integer,
    id_compte integer
);
    DROP TABLE public.client;
       public         heap r       postgres    false            �            1259    16405    client_id_client_seq    SEQUENCE     �   CREATE SEQUENCE public.client_id_client_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.client_id_client_seq;
       public               postgres    false    222            �           0    0    client_id_client_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.client_id_client_seq OWNED BY public.client.id_client;
          public               postgres    false    221            �            1259    16396    compte    TABLE     �  CREATE TABLE public.compte (
    id_compte integer NOT NULL,
    solde numeric(15,2) DEFAULT 0 NOT NULL,
    date_ouverture timestamp without time zone DEFAULT now() NOT NULL,
    statut character varying(20) NOT NULL,
    CONSTRAINT compte_statut_check CHECK (((statut)::text = ANY ((ARRAY['actif'::character varying, 'inactif'::character varying, 'cloture'::character varying])::text[])))
);
    DROP TABLE public.compte;
       public         heap r       postgres    false            �            1259    16395    compte_id_compte_seq    SEQUENCE     �   CREATE SEQUENCE public.compte_id_compte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.compte_id_compte_seq;
       public               postgres    false    220            �           0    0    compte_id_compte_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.compte_id_compte_seq OWNED BY public.compte.id_compte;
          public               postgres    false    219            �            1259    16439    journal    TABLE     �   CREATE TABLE public.journal (
    id_journal integer NOT NULL,
    evenement text NOT NULL,
    id_transaction integer,
    horodatage timestamp without time zone DEFAULT now() NOT NULL,
    noeud_source character varying(50) NOT NULL
);
    DROP TABLE public.journal;
       public         heap r       postgres    false            �            1259    16438    journal_id_journal_seq    SEQUENCE     �   CREATE SEQUENCE public.journal_id_journal_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.journal_id_journal_seq;
       public               postgres    false    226            �           0    0    journal_id_journal_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.journal_id_journal_seq OWNED BY public.journal.id_journal;
          public               postgres    false    225            �            1259    16423    transaction    TABLE     �  CREATE TABLE public.transaction (
    id_transaction integer NOT NULL,
    type_transaction character varying(20),
    montant numeric(15,2) NOT NULL,
    date_heure timestamp without time zone DEFAULT now() NOT NULL,
    etat_transaction character varying(20),
    id_compte integer,
    CONSTRAINT transaction_etat_transaction_check CHECK (((etat_transaction)::text = ANY ((ARRAY['validee'::character varying, 'refusee'::character varying, 'en_attente'::character varying])::text[]))),
    CONSTRAINT transaction_montant_check CHECK ((montant > (0)::numeric)),
    CONSTRAINT transaction_type_transaction_check CHECK (((type_transaction)::text = ANY ((ARRAY['depot'::character varying, 'retrait'::character varying, 'virement'::character varying])::text[])))
);
    DROP TABLE public.transaction;
       public         heap r       postgres    false            �            1259    16422    transaction_id_transaction_seq    SEQUENCE     �   CREATE SEQUENCE public.transaction_id_transaction_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.transaction_id_transaction_seq;
       public               postgres    false    224            �           0    0    transaction_id_transaction_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.transaction_id_transaction_seq OWNED BY public.transaction.id_transaction;
          public               postgres    false    223            5           2604    16392    agence id_agence    DEFAULT     t   ALTER TABLE ONLY public.agence ALTER COLUMN id_agence SET DEFAULT nextval('public.agence_id_agence_seq'::regclass);
 ?   ALTER TABLE public.agence ALTER COLUMN id_agence DROP DEFAULT;
       public               postgres    false    217    218    218            9           2604    16409    client id_client    DEFAULT     t   ALTER TABLE ONLY public.client ALTER COLUMN id_client SET DEFAULT nextval('public.client_id_client_seq'::regclass);
 ?   ALTER TABLE public.client ALTER COLUMN id_client DROP DEFAULT;
       public               postgres    false    222    221    222            6           2604    16399    compte id_compte    DEFAULT     t   ALTER TABLE ONLY public.compte ALTER COLUMN id_compte SET DEFAULT nextval('public.compte_id_compte_seq'::regclass);
 ?   ALTER TABLE public.compte ALTER COLUMN id_compte DROP DEFAULT;
       public               postgres    false    219    220    220            <           2604    16442    journal id_journal    DEFAULT     x   ALTER TABLE ONLY public.journal ALTER COLUMN id_journal SET DEFAULT nextval('public.journal_id_journal_seq'::regclass);
 A   ALTER TABLE public.journal ALTER COLUMN id_journal DROP DEFAULT;
       public               postgres    false    225    226    226            :           2604    16426    transaction id_transaction    DEFAULT     �   ALTER TABLE ONLY public.transaction ALTER COLUMN id_transaction SET DEFAULT nextval('public.transaction_id_transaction_seq'::regclass);
 I   ALTER TABLE public.transaction ALTER COLUMN id_transaction DROP DEFAULT;
       public               postgres    false    224    223    224            �          0    16389    agence 
   TABLE DATA           E   COPY public.agence (id_agence, nom_agence, localisation) FROM stdin;
    public               postgres    false    218   �5       �          0    16406    client 
   TABLE DATA           q   COPY public.client (id_client, nom_client, prenom_client, telephone, agence_rattachement, id_compte) FROM stdin;
    public               postgres    false    222   46       �          0    16396    compte 
   TABLE DATA           J   COPY public.compte (id_compte, solde, date_ouverture, statut) FROM stdin;
    public               postgres    false    220   �6       �          0    16439    journal 
   TABLE DATA           b   COPY public.journal (id_journal, evenement, id_transaction, horodatage, noeud_source) FROM stdin;
    public               postgres    false    226   7       �          0    16423    transaction 
   TABLE DATA           y   COPY public.transaction (id_transaction, type_transaction, montant, date_heure, etat_transaction, id_compte) FROM stdin;
    public               postgres    false    224   �7       �           0    0    agence_id_agence_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.agence_id_agence_seq', 3, true);
          public               postgres    false    217            �           0    0    client_id_client_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.client_id_client_seq', 4, true);
          public               postgres    false    221            �           0    0    compte_id_compte_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.compte_id_compte_seq', 4, true);
          public               postgres    false    219            �           0    0    journal_id_journal_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.journal_id_journal_seq', 7, true);
          public               postgres    false    225            �           0    0    transaction_id_transaction_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.transaction_id_transaction_seq', 6, true);
          public               postgres    false    223            C           2606    16394    agence agence_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.agence
    ADD CONSTRAINT agence_pkey PRIMARY KEY (id_agence);
 <   ALTER TABLE ONLY public.agence DROP CONSTRAINT agence_pkey;
       public                 postgres    false    218            G           2606    16411    client client_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id_client);
 <   ALTER TABLE ONLY public.client DROP CONSTRAINT client_pkey;
       public                 postgres    false    222            E           2606    16404    compte compte_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.compte
    ADD CONSTRAINT compte_pkey PRIMARY KEY (id_compte);
 <   ALTER TABLE ONLY public.compte DROP CONSTRAINT compte_pkey;
       public                 postgres    false    220            K           2606    16447    journal journal_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.journal
    ADD CONSTRAINT journal_pkey PRIMARY KEY (id_journal);
 >   ALTER TABLE ONLY public.journal DROP CONSTRAINT journal_pkey;
       public                 postgres    false    226            I           2606    16432    transaction transaction_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id_transaction);
 F   ALTER TABLE ONLY public.transaction DROP CONSTRAINT transaction_pkey;
       public                 postgres    false    224            L           2606    16412 &   client client_agence_rattachement_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_agence_rattachement_fkey FOREIGN KEY (agence_rattachement) REFERENCES public.agence(id_agence);
 P   ALTER TABLE ONLY public.client DROP CONSTRAINT client_agence_rattachement_fkey;
       public               postgres    false    222    218    4675            M           2606    16417    client client_id_compte_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_id_compte_fkey FOREIGN KEY (id_compte) REFERENCES public.compte(id_compte);
 F   ALTER TABLE ONLY public.client DROP CONSTRAINT client_id_compte_fkey;
       public               postgres    false    4677    222    220            O           2606    16448 #   journal journal_id_transaction_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.journal
    ADD CONSTRAINT journal_id_transaction_fkey FOREIGN KEY (id_transaction) REFERENCES public.transaction(id_transaction);
 M   ALTER TABLE ONLY public.journal DROP CONSTRAINT journal_id_transaction_fkey;
       public               postgres    false    226    224    4681            N           2606    16433 &   transaction transaction_id_compte_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_id_compte_fkey FOREIGN KEY (id_compte) REFERENCES public.compte(id_compte);
 P   ALTER TABLE ONLY public.transaction DROP CONSTRAINT transaction_id_compte_fkey;
       public               postgres    false    4677    224    220            �   B   x�3�tLO�KNU�M*���M��䄳��`�>�I��I����&�1L�;3�8#�8�������� ���      �   m   x�E��
�0�#kє+9$j���p���c��)��$��^0�x����P�H
a�>������
E����5^g��o�(�A矹�GNp�0w�2��}+"�Y^�      �   W   x��̱�0�ڞ�};v<BB�gAAI���NIo �zA�E<��Y���Pڏ�:�� �Z�#d��oO -*:"�[e�Ko%Z      �   �   x�m�=�0��9=�/@d;q�!L,�D�H-�$nOAH-m}�G~?R�t��pJ@�9�˹"��2A?a�(.�h	����c���qɋ�+ϸU�5��h ��5zOb�����G��6�Ձ�VmR]��/�c�#����2�U���&IG(~����c�Q#�m^m�*��1pz��Z��f+x��V�֣�T����Y��4��      �   �   x�}�A
�0����~ B�-��[z	ć@�%���)��PS�w������~#˄ib��т�PI�{~�K��<LhTP��0�E��_ñP1����ڶym{|�%\0@d5�����}%%4��!��A����� E�J�     