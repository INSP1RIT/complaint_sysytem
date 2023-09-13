--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

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
-- Name: roletype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roletype AS ENUM (
    'approver',
    'complainer',
    'admin'
);


ALTER TYPE public.roletype OWNER TO postgres;

--
-- Name: state; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.state AS ENUM (
    'pending',
    'approved',
    'rejected'
);


ALTER TYPE public.state OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: complaints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaints (
    id integer NOT NULL,
    title character varying(120) NOT NULL,
    description text NOT NULL,
    photo_url character varying(200) NOT NULL,
    amount double precision NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    status public.state DEFAULT 'pending'::public.state NOT NULL,
    complainer_id integer NOT NULL
);


ALTER TABLE public.complaints OWNER TO postgres;

--
-- Name: complaints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.complaints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.complaints_id_seq OWNER TO postgres;

--
-- Name: complaints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.complaints_id_seq OWNED BY public.complaints.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(120),
    password character varying(255),
    first_name character varying(200),
    last_name character varying(200),
    phone character varying(20),
    role public.roletype DEFAULT 'complainer'::public.roletype NOT NULL,
    iban character varying(200)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: complaints id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints ALTER COLUMN id SET DEFAULT nextval('public.complaints_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
aa43d80ae573
\.


--
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaints (id, title, description, photo_url, amount, created_at, status, complainer_id) FROM stdin;
2	iPhone was broken	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 14:51:35.366945	pending	7
3	iPhone was broken	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 14:53:29.806409	pending	7
4	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:13:47.896002	pending	7
5	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:35:53.044823	pending	7
6	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:36:21.62724	pending	7
7	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:37:47.220373	pending	7
8	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:39:15.240899	pending	7
10	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:45:22.952738	pending	7
11	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:47:37.342796	approved	7
9	iPhone was broken and iMac	stupid bitches, you gave me stolen iPhone that was broken	1@ya.ru	10000	2023-09-08 15:44:56.647446	approved	7
13	test complaint	test description	https://complaint-system-bucket-main.s3.eu-central-1.amazonaws.com/1918c53f-9d41-4e61-aaa9-857b0a2bdf58.jpg	30000	2023-09-11 10:39:50.538673	pending	15
14	bitches	new sofa	https://complaint-system-bucket-main.s3.eu-central-1.amazonaws.com/79b5349c-d34d-4d5b-b02f-ce371628b960.jpg	30000	2023-09-11 10:49:34.240684	approved	15
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password, first_name, last_name, phone, role, iban) FROM stdin;
1	nigga@gmail.com	$2b$12$rXpzKHQ5CF0Mf6SPHJxI.O65amqeWDQtsjvFJ6Q8nJFDf6q.8i1dC	Nigga	Niggovich	79822345670	complainer	AL47 2121 1009 0000 0002 3569 87411
3	niggazzz@gmail.com	$2b$12$YI03CqZySW1Ma4m21./c6.3HO0MaLmoRn3XQ68uCBfKDv/Ou38Y8a	Nigga	Chernii	79822315670	complainer	AL47 2121 1009 0000 0002 3369 87411
12	niggarechek@gmail.com	$2b$12$DuGGU0lKYjN/4Dq7mP3GpOEjxSnBvwRfWUkPTVMzVIdinITKkI5Xe	Nigga	Gansta	79822315620	complainer	AL47 2121 1009 0000 0002 3369 87411
7	test@gmail.com	$2b$12$2UETVQb9cJ1byIrzXrALiOcsHRPkBMLnbcvB2Q4GQ6njjRW19bENC	AJ	Kuzya	79024569102	admin	AL47 2121 1009 0000 0002 3369 87411
4	niggarek@gmail.com	$2b$12$h3lDU0vZid1fBO9C821mieEw8I8wpVb8PUEMmiew4hINgXQHqc1ZG	Nigga	Gansta	79822315620	approver	AL47 2121 1009 0000 0002 3369 87411
14	admin@gmail.com	$2b$12$sq7fhJImP1LwbylWJuZnGuxWBkdz/hL8O1/EN8MCYFRl4inoSHYua	Nigga	Admin	79023456711	admin	LU 28 001 94006447500003
13	alex@gmail.com	$2b$12$t5BOoGy5yvxa.R2pPmjmJeTRfF4HXc7UvE0BldxmiSieD3iZMq7pe	Alex	Abisher	79022345678	approver	AL47 2121 1009 0000 0002 3369 87411
15	complainer@gmail.com	$2b$12$9So1P8BectwHWK16W.JSJu/3anQJVnVJK2HPsOqEbOSBFP7NWu68O	Stupid	Complainer	799312345467	complainer	BY20 OLMP 3135 0000 0010 0000 0933
\.


--
-- Name: complaints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.complaints_id_seq', 14, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 15, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: complaints complaints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: complaints complaints_complainer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_complainer_id_fkey FOREIGN KEY (complainer_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

