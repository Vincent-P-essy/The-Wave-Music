--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS thewave;
--
-- Name: thewave; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE thewave WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE thewave OWNER TO postgres;

\connect thewave

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dataset; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA dataset;


ALTER SCHEMA dataset OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: album; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.album (
    "numAlb" integer NOT NULL,
    "titreAlbum" character varying NOT NULL,
    "dateParution" date NOT NULL,
    "imageCouverture" bytea,
    description text
);


ALTER TABLE dataset.album OWNER TO postgres;

--
-- Name: album_numAlb_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."album_numAlb_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."album_numAlb_seq" OWNER TO postgres;

--
-- Name: album_numAlb_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."album_numAlb_seq" OWNED BY dataset.album."numAlb";


--
-- Name: apparait_dans; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.apparait_dans (
    "numArt" integer NOT NULL,
    "numMorc" integer NOT NULL,
    role character varying(100) NOT NULL
);


ALTER TABLE dataset.apparait_dans OWNER TO postgres;

--
-- Name: artiste; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.artiste (
    "numArt" integer NOT NULL,
    nom character varying NOT NULL,
    prenom character varying NOT NULL,
    nationalite character varying NOT NULL,
    "dateNaissance" date NOT NULL,
    "dateDeces" date
);


ALTER TABLE dataset.artiste OWNER TO postgres;

--
-- Name: artiste_numArt_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."artiste_numArt_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."artiste_numArt_seq" OWNER TO postgres;

--
-- Name: artiste_numArt_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."artiste_numArt_seq" OWNED BY dataset.artiste."numArt";


--
-- Name: contient; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.contient (
    "numAlb" integer NOT NULL,
    "numMorc" integer NOT NULL,
    ordre integer NOT NULL
);


ALTER TABLE dataset.contient OWNER TO postgres;

--
-- Name: cree; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.cree (
    "numUsr" integer NOT NULL,
    "numPlay" integer NOT NULL,
    "dateCreation" timestamp without time zone NOT NULL
);


ALTER TABLE dataset.cree OWNER TO postgres;

--
-- Name: ecoute; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.ecoute (
    "numUsr" integer NOT NULL,
    "numMorc" integer NOT NULL,
    date timestamp without time zone NOT NULL,
    "nombreEcoute" integer NOT NULL
);


ALTER TABLE dataset.ecoute OWNER TO postgres;

--
-- Name: groupe; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.groupe (
    "numGrp" integer NOT NULL,
    "nomGroupe" character varying NOT NULL,
    "dateCreation" date,
    nationalite character varying,
    "gerneMusical" character varying
);


ALTER TABLE dataset.groupe OWNER TO postgres;

--
-- Name: groupe_numGrp_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."groupe_numGrp_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."groupe_numGrp_seq" OWNER TO postgres;

--
-- Name: groupe_numGrp_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."groupe_numGrp_seq" OWNED BY dataset.groupe."numGrp";


--
-- Name: inclut; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.inclut (
    "numPlay" integer NOT NULL,
    "numMorc" integer NOT NULL,
    ordre integer NOT NULL
);


ALTER TABLE dataset.inclut OWNER TO postgres;

--
-- Name: joue; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.joue (
    "numGrp" integer NOT NULL,
    "numMorc" integer NOT NULL
);


ALTER TABLE dataset.joue OWNER TO postgres;

--
-- Name: morceau; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.morceau (
    "numMorc" integer NOT NULL,
    "titreMorceau" character varying NOT NULL,
    duree integer NOT NULL,
    paroles text
);


ALTER TABLE dataset.morceau OWNER TO postgres;

--
-- Name: morceau_numMorc_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."morceau_numMorc_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."morceau_numMorc_seq" OWNER TO postgres;

--
-- Name: morceau_numMorc_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."morceau_numMorc_seq" OWNED BY dataset.morceau."numMorc";


--
-- Name: notification; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.notification (
    "numNotif" integer NOT NULL,
    type character varying NOT NULL,
    message text NOT NULL,
    "dateCreation" date NOT NULL,
    lu boolean NOT NULL
);


ALTER TABLE dataset.notification OWNER TO postgres;

--
-- Name: notification_numNotif_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."notification_numNotif_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."notification_numNotif_seq" OWNER TO postgres;

--
-- Name: notification_numNotif_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."notification_numNotif_seq" OWNED BY dataset.notification."numNotif";


--
-- Name: participe_a; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.participe_a (
    "numArt" integer NOT NULL,
    "numGrp" integer NOT NULL,
    role character varying NOT NULL,
    "dateEntree" date,
    "dateSortie" date
);


ALTER TABLE dataset.participe_a OWNER TO postgres;

--
-- Name: playlist; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.playlist (
    "numPlay" integer NOT NULL,
    "titrePlaylist" character varying NOT NULL,
    visibilite character varying NOT NULL,
    description text
);


ALTER TABLE dataset.playlist OWNER TO postgres;

--
-- Name: playlist_numPlay_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."playlist_numPlay_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."playlist_numPlay_seq" OWNER TO postgres;

--
-- Name: playlist_numPlay_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."playlist_numPlay_seq" OWNED BY dataset.playlist."numPlay";


--
-- Name: publie; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.publie (
    "numGrp" integer NOT NULL,
    "numAlb" integer NOT NULL
);


ALTER TABLE dataset.publie OWNER TO postgres;

--
-- Name: rapport_popularite_morceaux; Type: VIEW; Schema: dataset; Owner: postgres
--

CREATE VIEW dataset.rapport_popularite_morceaux AS
 SELECT m."numMorc" AS "ID_Morceau",
    m."titreMorceau" AS "Titre_Morceau",
    count(DISTINCT e.date) AS "Nb_Ecoutes_Uniques",
    count(DISTINCT e."numUsr") AS "Nb_Personnes_Ayant_Ecoute",
    count(DISTINCT
        CASE
            WHEN ((p.visibilite)::text = 'publique'::text) THEN i."numPlay"
            ELSE NULL::integer
        END) AS "Nb_Partages_Playlists_Publiques",
    (((count(DISTINCT e."numUsr"))::numeric * 0.10) + (((count(e.date) - count(DISTINCT e."numUsr")))::numeric * 0.01)) AS "Remuneration_Euro"
   FROM (((dataset.morceau m
     LEFT JOIN dataset.ecoute e ON ((m."numMorc" = e."numMorc")))
     LEFT JOIN dataset.inclut i ON ((m."numMorc" = i."numMorc")))
     LEFT JOIN dataset.playlist p ON ((i."numPlay" = p."numPlay")))
  GROUP BY m."numMorc", m."titreMorceau";


ALTER VIEW dataset.rapport_popularite_morceaux OWNER TO postgres;

--
-- Name: recois; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.recois (
    "numUsr" integer NOT NULL,
    "numNotif" integer NOT NULL
);


ALTER TABLE dataset.recois OWNER TO postgres;

--
-- Name: suit; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.suit (
    "idSuiveur" integer NOT NULL,
    "idSuivi" integer NOT NULL,
    "typeSuivi" character varying NOT NULL
);


ALTER TABLE dataset.suit OWNER TO postgres;

--
-- Name: utilisateur; Type: TABLE; Schema: dataset; Owner: postgres
--

CREATE TABLE dataset.utilisateur (
    pseudonyme character varying NOT NULL,
    email character varying NOT NULL,
    "motDePasse" character varying NOT NULL,
    "dateInscription" date NOT NULL,
    "numUsr" integer NOT NULL,
    CONSTRAINT "utilisateur_motDePasse_check" CHECK ((length(("motDePasse")::text) >= 8))
);


ALTER TABLE dataset.utilisateur OWNER TO postgres;

--
-- Name: utilisateur_numUsr_seq; Type: SEQUENCE; Schema: dataset; Owner: postgres
--

CREATE SEQUENCE dataset."utilisateur_numUsr_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dataset."utilisateur_numUsr_seq" OWNER TO postgres;

--
-- Name: utilisateur_numUsr_seq; Type: SEQUENCE OWNED BY; Schema: dataset; Owner: postgres
--

ALTER SEQUENCE dataset."utilisateur_numUsr_seq" OWNED BY dataset.utilisateur."numUsr";


--
-- Name: album numAlb; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.album ALTER COLUMN "numAlb" SET DEFAULT nextval('dataset."album_numAlb_seq"'::regclass);


--
-- Name: artiste numArt; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.artiste ALTER COLUMN "numArt" SET DEFAULT nextval('dataset."artiste_numArt_seq"'::regclass);


--
-- Name: groupe numGrp; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.groupe ALTER COLUMN "numGrp" SET DEFAULT nextval('dataset."groupe_numGrp_seq"'::regclass);


--
-- Name: morceau numMorc; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.morceau ALTER COLUMN "numMorc" SET DEFAULT nextval('dataset."morceau_numMorc_seq"'::regclass);


--
-- Name: notification numNotif; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.notification ALTER COLUMN "numNotif" SET DEFAULT nextval('dataset."notification_numNotif_seq"'::regclass);


--
-- Name: playlist numPlay; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.playlist ALTER COLUMN "numPlay" SET DEFAULT nextval('dataset."playlist_numPlay_seq"'::regclass);


--
-- Name: utilisateur numUsr; Type: DEFAULT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.utilisateur ALTER COLUMN "numUsr" SET DEFAULT nextval('dataset."utilisateur_numUsr_seq"'::regclass);


--
-- Data for Name: album; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.album ("numAlb", "titreAlbum", "dateParution", "imageCouverture", description) VALUES (1, 'A Night at the Opera', '1975-11-21', NULL, 'Fourth studio album by Queen');
INSERT INTO dataset.album ("numAlb", "titreAlbum", "dateParution", "imageCouverture", description) VALUES (2, 'Are You Experienced', '1967-05-12', NULL, 'Debut album by The Jimi Hendrix Experience');
INSERT INTO dataset.album ("numAlb", "titreAlbum", "dateParution", "imageCouverture", description) VALUES (3, 'Imagine', '1971-09-09', NULL, 'Second studio album by John Lennon');


--
-- Data for Name: apparait_dans; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.apparait_dans ("numArt", "numMorc", role) VALUES (2, 2, 'pianist');
INSERT INTO dataset.apparait_dans ("numArt", "numMorc", role) VALUES (1, 1, 'main vocal');
INSERT INTO dataset.apparait_dans ("numArt", "numMorc", role) VALUES (3, 3, 'producer');
INSERT INTO dataset.apparait_dans ("numArt", "numMorc", role) VALUES (2, 1, 'pianist');


--
-- Data for Name: artiste; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.artiste ("numArt", nom, prenom, nationalite, "dateNaissance", "dateDeces") VALUES (1, 'Mercury', 'Freddie', 'British', '1946-09-05', '1991-11-24');
INSERT INTO dataset.artiste ("numArt", nom, prenom, nationalite, "dateNaissance", "dateDeces") VALUES (2, 'Hendrix', 'Jimi', 'American', '1942-11-27', '1970-09-18');
INSERT INTO dataset.artiste ("numArt", nom, prenom, nationalite, "dateNaissance", "dateDeces") VALUES (3, 'Lennon', 'John', 'British', '1940-10-09', '1980-12-08');


--
-- Data for Name: contient; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.contient ("numAlb", "numMorc", ordre) VALUES (1, 1, 1);
INSERT INTO dataset.contient ("numAlb", "numMorc", ordre) VALUES (2, 2, 1);
INSERT INTO dataset.contient ("numAlb", "numMorc", ordre) VALUES (1, 3, 2);


--
-- Data for Name: cree; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.cree ("numUsr", "numPlay", "dateCreation") VALUES (1, 1, '2023-05-20 10:30:00');
INSERT INTO dataset.cree ("numUsr", "numPlay", "dateCreation") VALUES (2, 2, '2023-05-22 14:45:00');


--
-- Data for Name: ecoute; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (2, 3, '2024-12-08 19:02:10', 15);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (1, 3, '2024-12-08 19:01:51', 18);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (3, 1, '2024-12-10 16:32:27.618155', 5);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (3, 3, '2023-06-03 09:45:00', 12);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (3, 2, '2024-12-10 16:32:17.913731', 4);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (1, 1, '2024-12-11 18:34:41.166347', 10);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (1, 2, '2024-12-11 18:35:04.777443', 7);
INSERT INTO dataset.ecoute ("numUsr", "numMorc", date, "nombreEcoute") VALUES (2, 2, '2024-12-11 18:41:52.565883', 4);


--
-- Data for Name: groupe; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.groupe ("numGrp", "nomGroupe", "dateCreation", nationalite, "gerneMusical") VALUES (1, 'Queen', '1970-01-01', 'British', 'Rock');
INSERT INTO dataset.groupe ("numGrp", "nomGroupe", "dateCreation", nationalite, "gerneMusical") VALUES (2, 'The Beatles', '1960-01-01', 'British', 'Rock');
INSERT INTO dataset.groupe ("numGrp", "nomGroupe", "dateCreation", nationalite, "gerneMusical") VALUES (3, 'Jimi Hendrix Experience', '1966-10-01', 'American', 'Psychedelic Rock');


--
-- Data for Name: inclut; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.inclut ("numPlay", "numMorc", ordre) VALUES (1, 1, 1);
INSERT INTO dataset.inclut ("numPlay", "numMorc", ordre) VALUES (1, 2, 2);
INSERT INTO dataset.inclut ("numPlay", "numMorc", ordre) VALUES (2, 3, 1);


--
-- Data for Name: joue; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.joue ("numGrp", "numMorc") VALUES (1, 1);
INSERT INTO dataset.joue ("numGrp", "numMorc") VALUES (3, 2);


--
-- Data for Name: morceau; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.morceau ("numMorc", "titreMorceau", duree, paroles) VALUES (1, 'Bohemian Rhapsody', 355, 'Is this the real life? Is this just fantasy...');
INSERT INTO dataset.morceau ("numMorc", "titreMorceau", duree, paroles) VALUES (2, 'Purple Haze', 170, NULL);
INSERT INTO dataset.morceau ("numMorc", "titreMorceau", duree, paroles) VALUES (3, 'Imagine', 183, 'Imagine there''s no heaven, it''s easy if you try...');


--
-- Data for Name: notification; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.notification ("numNotif", type, message, "dateCreation", lu) VALUES (1, 'new_album', 'Queen released a new album!', '2023-05-01', false);
INSERT INTO dataset.notification ("numNotif", type, message, "dateCreation", lu) VALUES (2, 'follow', 'You have a new follower!', '2023-04-15', true);
INSERT INTO dataset.notification ("numNotif", type, message, "dateCreation", lu) VALUES (3, 'new_playlist', 'A user you follow created a new playlist', '2023-06-10', false);


--
-- Data for Name: participe_a; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.participe_a ("numArt", "numGrp", role, "dateEntree", "dateSortie") VALUES (1, 1, 'singer', '1970-01-01', '1991-11-24');
INSERT INTO dataset.participe_a ("numArt", "numGrp", role, "dateEntree", "dateSortie") VALUES (2, 3, 'guitarist', '1966-10-01', '1970-09-18');
INSERT INTO dataset.participe_a ("numArt", "numGrp", role, "dateEntree", "dateSortie") VALUES (1, 2, 'singer', '1991-11-24', NULL);
INSERT INTO dataset.participe_a ("numArt", "numGrp", role, "dateEntree", "dateSortie") VALUES (2, 1, 'lead musician', '1970-09-18', NULL);
INSERT INTO dataset.participe_a ("numArt", "numGrp", role, "dateEntree", "dateSortie") VALUES (3, 1, 'producer', '2006-12-09', '1980-12-08');


--
-- Data for Name: playlist; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.playlist ("numPlay", "titrePlaylist", visibilite, description) VALUES (1, 'Classic Rock', 'public', 'A playlist of classic rock hits');
INSERT INTO dataset.playlist ("numPlay", "titrePlaylist", visibilite, description) VALUES (2, 'Relaxing Tunes', 'private', 'Soft and relaxing music');


--
-- Data for Name: publie; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.publie ("numGrp", "numAlb") VALUES (1, 1);
INSERT INTO dataset.publie ("numGrp", "numAlb") VALUES (3, 2);


--
-- Data for Name: recois; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.recois ("numUsr", "numNotif") VALUES (1, 1);
INSERT INTO dataset.recois ("numUsr", "numNotif") VALUES (2, 2);
INSERT INTO dataset.recois ("numUsr", "numNotif") VALUES (3, 3);


--
-- Data for Name: suit; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.suit ("idSuiveur", "idSuivi", "typeSuivi") VALUES (1, 3, 'artist_follow');
INSERT INTO dataset.suit ("idSuiveur", "idSuivi", "typeSuivi") VALUES (2, 1, 'user_follow');
INSERT INTO dataset.suit ("idSuiveur", "idSuivi", "typeSuivi") VALUES (3, 1, 'group_follow');
INSERT INTO dataset.suit ("idSuiveur", "idSuivi", "typeSuivi") VALUES (1, 2, 'user_follow');


--
-- Data for Name: utilisateur; Type: TABLE DATA; Schema: dataset; Owner: postgres
--

INSERT INTO dataset.utilisateur (pseudonyme, email, "motDePasse", "dateInscription", "numUsr") VALUES ('rockfan123', 'rockfan123@example.com', '$2b$12$swxMHxAA8/5OkvVrGnRYF.0fAoQgr1sanpDeqIJmn4lEqiwP96wme', '2023-01-10', 1);
INSERT INTO dataset.utilisateur (pseudonyme, email, "motDePasse", "dateInscription", "numUsr") VALUES ('musicLover', 'musiclover@example.com', '$2b$12$U.xWnrK8f/6mUXwjdcbtAOaNe.DBHGDpvoFpy.ZXR7b9v/6kTBZZS', '2023-02-15', 2);
INSERT INTO dataset.utilisateur (pseudonyme, email, "motDePasse", "dateInscription", "numUsr") VALUES ('johnDoe', 'johndoe@example.com', '$2b$12$dSAsLFomr6qMnaz9eleSE.yauE2SgNL/ovuRQYIjkaYWWhPLeKOce', '2023-03-20', 3);


--
-- Name: album_numAlb_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."album_numAlb_seq"', 3, true);


--
-- Name: artiste_numArt_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."artiste_numArt_seq"', 3, true);


--
-- Name: groupe_numGrp_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."groupe_numGrp_seq"', 3, true);


--
-- Name: morceau_numMorc_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."morceau_numMorc_seq"', 3, true);


--
-- Name: notification_numNotif_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."notification_numNotif_seq"', 3, true);


--
-- Name: playlist_numPlay_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."playlist_numPlay_seq"', 2, true);


--
-- Name: utilisateur_numUsr_seq; Type: SEQUENCE SET; Schema: dataset; Owner: postgres
--

SELECT pg_catalog.setval('dataset."utilisateur_numUsr_seq"', 3, true);


--
-- Name: album album_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.album
    ADD CONSTRAINT album_pk PRIMARY KEY ("numAlb");


--
-- Name: apparait_dans apparait_dans_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.apparait_dans
    ADD CONSTRAINT apparait_dans_pk PRIMARY KEY ("numArt", "numMorc", role);


--
-- Name: artiste artiste_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.artiste
    ADD CONSTRAINT artiste_pk PRIMARY KEY ("numArt");


--
-- Name: contient contient_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.contient
    ADD CONSTRAINT contient_pk PRIMARY KEY ("numAlb", "numMorc");


--
-- Name: cree cree_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.cree
    ADD CONSTRAINT cree_pk PRIMARY KEY ("numUsr", "numPlay");


--
-- Name: ecoute ecoute_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.ecoute
    ADD CONSTRAINT ecoute_pk PRIMARY KEY ("numUsr", "numMorc");


--
-- Name: groupe groupe_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.groupe
    ADD CONSTRAINT groupe_pk PRIMARY KEY ("numGrp");


--
-- Name: inclut inclut_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.inclut
    ADD CONSTRAINT inclut_pk PRIMARY KEY ("numPlay", "numMorc");


--
-- Name: joue joue_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.joue
    ADD CONSTRAINT joue_pk PRIMARY KEY ("numGrp", "numMorc");


--
-- Name: morceau morceau_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.morceau
    ADD CONSTRAINT morceau_pk PRIMARY KEY ("numMorc");


--
-- Name: notification notification_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.notification
    ADD CONSTRAINT notification_pk PRIMARY KEY ("numNotif");


--
-- Name: participe_a participe_a_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.participe_a
    ADD CONSTRAINT participe_a_pk PRIMARY KEY ("numArt", "numGrp", role);


--
-- Name: playlist playlist_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.playlist
    ADD CONSTRAINT playlist_pk PRIMARY KEY ("numPlay");


--
-- Name: publie publie_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.publie
    ADD CONSTRAINT publie_pk PRIMARY KEY ("numGrp", "numAlb");


--
-- Name: recois recois_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.recois
    ADD CONSTRAINT recois_pk PRIMARY KEY ("numUsr", "numNotif");


--
-- Name: suit suit_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.suit
    ADD CONSTRAINT suit_pk PRIMARY KEY ("idSuiveur", "idSuivi", "typeSuivi");


--
-- Name: utilisateur utilisateur_pk; Type: CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.utilisateur
    ADD CONSTRAINT utilisateur_pk PRIMARY KEY ("numUsr");


--
-- Name: album_numalb_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX album_numalb_uindex ON dataset.album USING btree ("numAlb");


--
-- Name: artiste_numart_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX artiste_numart_uindex ON dataset.artiste USING btree ("numArt");


--
-- Name: groupe_numgrp_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX groupe_numgrp_uindex ON dataset.groupe USING btree ("numGrp");


--
-- Name: morceau_nummorc_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX morceau_nummorc_uindex ON dataset.morceau USING btree ("numMorc");


--
-- Name: notification_numnotif_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX notification_numnotif_uindex ON dataset.notification USING btree ("numNotif");


--
-- Name: playlist_numplay_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX playlist_numplay_uindex ON dataset.playlist USING btree ("numPlay");


--
-- Name: utilisateur_email_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX utilisateur_email_uindex ON dataset.utilisateur USING btree (email);


--
-- Name: utilisateur_numusr_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX utilisateur_numusr_uindex ON dataset.utilisateur USING btree ("numUsr");


--
-- Name: utilisateur_pseudonyme_uindex; Type: INDEX; Schema: dataset; Owner: postgres
--

CREATE UNIQUE INDEX utilisateur_pseudonyme_uindex ON dataset.utilisateur USING btree (pseudonyme);


--
-- Name: apparait_dans apparait_dans_artiste_numart_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.apparait_dans
    ADD CONSTRAINT apparait_dans_artiste_numart_fk FOREIGN KEY ("numArt") REFERENCES dataset.artiste("numArt");


--
-- Name: apparait_dans apparait_dans_morceau_nummorc_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.apparait_dans
    ADD CONSTRAINT apparait_dans_morceau_nummorc_fk FOREIGN KEY ("numMorc") REFERENCES dataset.morceau("numMorc");


--
-- Name: contient contient_album_numalb_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.contient
    ADD CONSTRAINT contient_album_numalb_fk FOREIGN KEY ("numAlb") REFERENCES dataset.album("numAlb");


--
-- Name: contient contient_morceau_nummorc_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.contient
    ADD CONSTRAINT contient_morceau_nummorc_fk FOREIGN KEY ("numMorc") REFERENCES dataset.morceau("numMorc");


--
-- Name: cree cree_playlist_numplay_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.cree
    ADD CONSTRAINT cree_playlist_numplay_fk FOREIGN KEY ("numPlay") REFERENCES dataset.playlist("numPlay");


--
-- Name: cree cree_utilisateur_numusr_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.cree
    ADD CONSTRAINT cree_utilisateur_numusr_fk FOREIGN KEY ("numUsr") REFERENCES dataset.utilisateur("numUsr");


--
-- Name: ecoute ecoute_morceau_nummorc_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.ecoute
    ADD CONSTRAINT ecoute_morceau_nummorc_fk FOREIGN KEY ("numMorc") REFERENCES dataset.morceau("numMorc");


--
-- Name: ecoute ecoute_utilisateur_numusr_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.ecoute
    ADD CONSTRAINT ecoute_utilisateur_numusr_fk FOREIGN KEY ("numUsr") REFERENCES dataset.utilisateur("numUsr");


--
-- Name: inclut inclut_morceau_nummorc_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.inclut
    ADD CONSTRAINT inclut_morceau_nummorc_fk FOREIGN KEY ("numMorc") REFERENCES dataset.morceau("numMorc");


--
-- Name: inclut inclut_playlist_numplay_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.inclut
    ADD CONSTRAINT inclut_playlist_numplay_fk FOREIGN KEY ("numPlay") REFERENCES dataset.playlist("numPlay");


--
-- Name: joue joue_groupe_numgrp_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.joue
    ADD CONSTRAINT joue_groupe_numgrp_fk FOREIGN KEY ("numGrp") REFERENCES dataset.groupe("numGrp");


--
-- Name: joue joue_morceau_nummorc_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.joue
    ADD CONSTRAINT joue_morceau_nummorc_fk FOREIGN KEY ("numMorc") REFERENCES dataset.morceau("numMorc");


--
-- Name: participe_a participe_a_artiste_numart_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.participe_a
    ADD CONSTRAINT participe_a_artiste_numart_fk FOREIGN KEY ("numArt") REFERENCES dataset.artiste("numArt");


--
-- Name: participe_a participe_a_groupe_numgrp_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.participe_a
    ADD CONSTRAINT participe_a_groupe_numgrp_fk FOREIGN KEY ("numGrp") REFERENCES dataset.groupe("numGrp");


--
-- Name: publie publie_album_numalb_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.publie
    ADD CONSTRAINT publie_album_numalb_fk FOREIGN KEY ("numAlb") REFERENCES dataset.album("numAlb");


--
-- Name: publie publie_groupe_numgrp_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.publie
    ADD CONSTRAINT publie_groupe_numgrp_fk FOREIGN KEY ("numGrp") REFERENCES dataset.groupe("numGrp");


--
-- Name: recois recois_notification_numnotif_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.recois
    ADD CONSTRAINT recois_notification_numnotif_fk FOREIGN KEY ("numNotif") REFERENCES dataset.notification("numNotif");


--
-- Name: recois recois_utilisateur_numusr_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.recois
    ADD CONSTRAINT recois_utilisateur_numusr_fk FOREIGN KEY ("numUsr") REFERENCES dataset.utilisateur("numUsr");


--
-- Name: suit suit_utilisateur_artiste_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.suit
    ADD CONSTRAINT suit_utilisateur_artiste_fk FOREIGN KEY ("idSuivi") REFERENCES dataset.artiste("numArt");


--
-- Name: suit suit_utilisateur_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.suit
    ADD CONSTRAINT suit_utilisateur_fk FOREIGN KEY ("idSuiveur") REFERENCES dataset.utilisateur("numUsr");


--
-- Name: suit suit_utilisateur_groupe_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.suit
    ADD CONSTRAINT suit_utilisateur_groupe_fk FOREIGN KEY ("idSuivi") REFERENCES dataset.groupe("numGrp");


--
-- Name: suit suit_utilisateur_utilisateur_fk; Type: FK CONSTRAINT; Schema: dataset; Owner: postgres
--

ALTER TABLE ONLY dataset.suit
    ADD CONSTRAINT suit_utilisateur_utilisateur_fk FOREIGN KEY ("idSuivi") REFERENCES dataset.utilisateur("numUsr");


--
-- PostgreSQL database dump complete
--

