--
-- PostgreSQL database dump
--

\restrict wSWETfTsMlpK7DweWDifCuCHerx3wCziEi07ZTTsNTzdcy7FPWQvy46c4QmmN8u

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg13+1)
-- Dumped by pg_dump version 16.10 (Debian 16.10-1.pgdg13+1)

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
-- Name: menuitemcategory; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.menuitemcategory AS ENUM (
    'FOOD',
    'DRINK',
    'ALCOHOL'
);


ALTER TYPE public.menuitemcategory OWNER TO postgres;

--
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.orderstatus AS ENUM (
    'PENDING',
    'CONFIRMED',
    'PREPARING',
    'READY',
    'SERVED',
    'CANCELLED'
);


ALTER TYPE public.orderstatus OWNER TO postgres;

--
-- Name: ordertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.ordertype AS ENUM (
    'DINE_IN',
    'TAKEAWAY',
    'DELIVERY'
);


ALTER TYPE public.ordertype OWNER TO postgres;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userrole AS ENUM (
    'admin',
    'waiter',
    'kitchen',
    'bar'
);


ALTER TYPE public.userrole OWNER TO postgres;

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
-- Name: ingredients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingredients (
    id integer NOT NULL,
    name character varying,
    category character varying,
    unit character varying,
    current_stock double precision,
    minimum_stock double precision,
    cost_per_unit double precision,
    supplier character varying,
    last_updated timestamp without time zone
);


ALTER TABLE public.ingredients OWNER TO postgres;

--
-- Name: ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingredients_id_seq OWNER TO postgres;

--
-- Name: ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;


--
-- Name: invoices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices (
    id integer NOT NULL,
    invoice_number character varying,
    order_id integer,
    customer_name character varying,
    customer_phone character varying,
    customer_address character varying,
    order_type character varying,
    table_number character varying,
    subtotal double precision,
    tax double precision,
    total double precision,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    invoice_data text
);


ALTER TABLE public.invoices OWNER TO postgres;

--
-- Name: invoices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invoices_id_seq OWNER TO postgres;

--
-- Name: invoices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_id_seq OWNED BY public.invoices.id;


--
-- Name: item_ingredients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_ingredients (
    menu_item_id integer,
    ingredient_id integer,
    quantity double precision,
    unit character varying
);


ALTER TABLE public.item_ingredients OWNER TO postgres;

--
-- Name: kitchen_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kitchen_orders (
    id integer NOT NULL,
    table_number integer,
    order_type character varying,
    status character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    order_id integer
);


ALTER TABLE public.kitchen_orders OWNER TO postgres;

--
-- Name: kitchen_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kitchen_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kitchen_orders_id_seq OWNER TO postgres;

--
-- Name: kitchen_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kitchen_orders_id_seq OWNED BY public.kitchen_orders.id;


--
-- Name: menu_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menu_items (
    id integer NOT NULL,
    name character varying,
    price double precision,
    category public.menuitemcategory
);


ALTER TABLE public.menu_items OWNER TO postgres;

--
-- Name: menu_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menu_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.menu_items_id_seq OWNER TO postgres;

--
-- Name: menu_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menu_items_id_seq OWNED BY public.menu_items.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    menu_item_id integer,
    quantity integer,
    price double precision,
    special_requests character varying
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: order_staff_association; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_staff_association (
    order_id integer,
    user_id integer
);


ALTER TABLE public.order_staff_association OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    table_number integer,
    order_type public.ordertype,
    status public.orderstatus,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    special_requests character varying,
    created_by integer,
    total double precision,
    order_data json,
    table_id integer,
    customer_count integer,
    assigned_seats json,
    customer_name character varying,
    customer_phone character varying,
    delivery_address character varying,
    modifiers json
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: stock_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_transactions (
    id integer NOT NULL,
    ingredient_id integer,
    transaction_type character varying,
    quantity double precision,
    unit character varying,
    cost double precision,
    notes character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.stock_transactions OWNER TO postgres;

--
-- Name: stock_transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stock_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stock_transactions_id_seq OWNER TO postgres;

--
-- Name: stock_transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stock_transactions_id_seq OWNED BY public.stock_transactions.id;


--
-- Name: tables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tables (
    id integer NOT NULL,
    table_number integer,
    capacity integer,
    is_occupied boolean,
    current_order_id integer,
    status character varying,
    seats json
);


ALTER TABLE public.tables OWNER TO postgres;

--
-- Name: tables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tables_id_seq OWNER TO postgres;

--
-- Name: tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tables_id_seq OWNED BY public.tables.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    learning_path character varying,
    progress character varying,
    role public.userrole
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


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: invoices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices ALTER COLUMN id SET DEFAULT nextval('public.invoices_id_seq'::regclass);


--
-- Name: kitchen_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kitchen_orders ALTER COLUMN id SET DEFAULT nextval('public.kitchen_orders_id_seq'::regclass);


--
-- Name: menu_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_items ALTER COLUMN id SET DEFAULT nextval('public.menu_items_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: stock_transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_transactions ALTER COLUMN id SET DEFAULT nextval('public.stock_transactions_id_seq'::regclass);


--
-- Name: tables id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables ALTER COLUMN id SET DEFAULT nextval('public.tables_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
0007
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingredients (id, name, category, unit, current_stock, minimum_stock, cost_per_unit, supplier, last_updated) FROM stdin;
3	Fish	meat	kg	8	5	2	Local Supplier	2025-09-19 08:09:22.052981
1	Tomatoes	vegetable	kg	8	5	2.5	Local Farm	2025-09-22 08:54:50.126973
4	Duck Egg	meat	pieces	89	10	1	Local Farmar	2025-09-22 09:32:06.561942
2	Carrot	vegetable	kg	7	5	0.5	Market	2025-09-22 09:32:07.029862
\.


--
-- Data for Name: invoices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices (id, invoice_number, order_id, customer_name, customer_phone, customer_address, order_type, table_number, subtotal, tax, total, created_at, updated_at, invoice_data) FROM stdin;
1	INV-202509-0001	1	N/A	N/A	N/A	dine-in	N/A	17.98	0	17.98	2025-09-17 08:47:57.871321	2025-09-17 08:47:57.871325	[{"name": "Burger", "category": "grill", "price": 12.99, "quantity": 1}, {"name": "Fries", "category": "sides", "price": 4.99, "quantity": 1}]
2	INV-202509-0002	6	N/A	N/A	N/A	dine-in	N/A	11.98	0	11.98	2025-09-17 09:33:33.194448	2025-09-17 09:33:33.194458	[{"name": "Burger", "category": "food", "price": 8.99, "quantity": 1}, {"name": "Soda", "category": "drink", "price": 2.99, "quantity": 1}]
36	INV-202509-0003	2	Test Customer	\N	\N	dine-in	5	25.5	0	25.5	2025-09-22 08:41:04.103144	2025-09-22 08:41:04.103149	[{"name": "Pizza", "category": "Main Course", "price": 15.0, "quantity": 1}, {"name": "Salad", "category": "Sides", "price": 7.5, "quantity": 1}, {"name": "Soda", "category": "Drinks", "price": 3.0, "quantity": 1}]
37	INV-202509-0004	3	Test Customer 3	\N	\N	dine-in	7	30	0	30	2025-09-22 08:42:28.871364	2025-09-22 08:42:28.871368	[{"name": "Steak", "category": "Main Course", "price": 25.0, "quantity": 1}, {"name": "Wine", "category": "Drinks", "price": 5.0, "quantity": 1}]
38	INV-202509-0005	31	kyaw	7987899899	\N	takeaway	\N	2.99	0	2.99	2025-09-22 08:43:06.379257	2025-09-22 08:43:06.379261	[{"name": "Soda", "category": "drink", "price": 2.99, "quantity": 1}]
39	INV-202509-0006	4	Debug Customer	\N	\N	dine-in	10	45.5	0	45.5	2025-09-22 08:46:33.011531	2025-09-22 08:46:33.011536	[{"name": "Pizza", "category": "Main Course", "price": 20.0, "quantity": 1}, {"name": "Salad", "category": "Sides", "price": 10.0, "quantity": 1}, {"name": "Wine", "category": "Drinks", "price": 15.5, "quantity": 1}]
40	INV-202509-0007	5	Customer 5	\N	\N	dine-in	15	17.98	0	17.98	2025-09-22 08:47:57.123953	2025-09-22 08:47:57.123958	[{"name": "Burger", "category": "Main Course", "price": 12.99, "quantity": 1}, {"name": "Fries", "category": "Sides", "price": 4.99, "quantity": 1}]
41	INV-202509-0008	7	aung	4554445	yangon	OrderType.DELIVERY	\N	11.98	0	11.98	2025-09-22 08:51:19.703679	2025-09-22 08:51:19.703683	[{"name": "Burger", "category": "food", "price": 8.99, "quantity": 1}, {"name": "Soda", "category": "drink", "price": 2.99, "quantity": 1}]
42	INV-202509-0009	8	zawzaw	4545455	Yangon Hlaing	delivery	N/A	6.99	0	6.99	2025-09-22 09:13:43.420497	2025-09-22 09:13:43.420504	[{"name": "Tea Leaf Salad", "category": "food", "price": 6.99, "quantity": 1}]
43	INV-202509-0010	9	zawning	1231324123	N/A	takeaway	N/A	8.99	0	8.99	2025-09-22 09:13:48.141588	2025-09-22 09:13:48.141596	[{"name": "Burger", "category": "food", "price": 8.99, "quantity": 1}]
44	INV-202509-0011	36	N/A	N/A	N/A	dine_in	5	19.97	0	19.97	2025-09-22 09:13:56.77765	2025-09-22 09:13:56.777654	[{"name": "Burger", "category": "food", "price": 8.99, "quantity": 1}, {"name": "Soda", "category": "drink", "price": 2.99, "quantity": 1}, {"name": "Wine", "category": "alcohol", "price": 7.99, "quantity": 1}]
\.


--
-- Data for Name: item_ingredients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_ingredients (menu_item_id, ingredient_id, quantity, unit) FROM stdin;
1	1	1	kg
1	2	1	5
2	2	1	1
3	2	1	kg
11	3	1	kg
11	4	1	pieces
1	4	1	pieces
2	4	10	pieces
\.


--
-- Data for Name: kitchen_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kitchen_orders (id, table_number, order_type, status, created_at, updated_at, order_id) FROM stdin;
1	\N	\N	served	2025-09-17 09:08:12.099626	2025-09-17 09:09:35.097722	5
2	\N	\N	served	2025-09-17 09:32:26.974042	2025-09-17 09:33:11.598856	6
8	\N	\N	ready	2025-09-18 06:58:53.235061	2025-09-18 06:59:17.133977	12
6	\N	\N	served	2025-09-18 06:46:35.51351	2025-09-18 07:49:48.860989	10
9	\N	\N	preparing	2025-09-18 09:39:50.810307	2025-09-18 09:40:33.174546	13
5	\N	\N	ready	2025-09-18 02:53:52.901811	2025-09-18 10:01:28.47614	9
3	\N	\N	ready	2025-09-18 02:44:12.024913	2025-09-19 07:06:33.149465	7
7	\N	\N	ready	2025-09-18 06:50:17.968724	2025-09-19 07:06:34.161693	11
10	\N	\N	preparing	2025-09-19 07:01:15.121655	2025-09-19 07:06:36.146551	14
15	\N	\N	pending	2025-09-19 07:52:49.714683	2025-09-19 07:52:49.714687	19
16	\N	\N	pending	2025-09-19 08:03:30.956945	2025-09-19 08:03:30.95695	20
17	\N	\N	pending	2025-09-19 08:04:03.814603	2025-09-19 08:04:03.814606	21
18	\N	\N	pending	2025-09-19 08:08:30.090193	2025-09-19 08:08:30.090196	22
19	\N	\N	pending	2025-09-19 08:09:21.917758	2025-09-19 08:09:21.917762	23
20	\N	\N	pending	2025-09-19 08:15:46.931886	2025-09-19 08:15:46.931894	24
21	\N	\N	pending	2025-09-19 08:15:55.084733	2025-09-19 08:15:55.084739	25
22	\N	\N	pending	2025-09-19 08:15:56.396811	2025-09-19 08:15:56.396815	26
24	\N	\N	pending	2025-09-19 08:29:04.053185	2025-09-19 08:29:04.05319	28
25	\N	\N	pending	2025-09-19 08:29:06.890569	2025-09-19 08:29:06.890576	29
26	\N	\N	pending	2025-09-19 08:29:13.789565	2025-09-19 08:29:13.78957	30
4	\N	\N	ready	2025-09-18 02:46:34.109458	2025-09-19 08:36:53.838783	8
28	\N	\N	pending	2025-09-19 08:59:07.516058	2025-09-19 08:59:07.516062	32
29	\N	\N	pending	2025-09-19 08:59:19.293883	2025-09-19 08:59:19.293886	33
30	\N	\N	pending	2025-09-19 08:59:22.558444	2025-09-19 08:59:22.558448	34
14	\N	\N	preparing	2025-09-19 07:23:20.070375	2025-09-19 09:27:39.033053	18
11	\N	\N	ready	2025-09-19 07:05:10.222907	2025-09-19 09:27:46.945506	15
12	\N	\N	ready	2025-09-19 07:07:00.357935	2025-09-19 09:29:02.542222	16
13	\N	\N	ready	2025-09-19 07:08:16.904367	2025-09-19 09:29:05.801593	17
23	\N	\N	ready	2025-09-19 08:15:57.645615	2025-09-19 09:32:08.20148	27
27	\N	\N	served	2025-09-19 08:37:10.742598	2025-09-19 10:22:58.84389	31
31	\N	\N	pending	2025-09-19 10:27:30.989089	2025-09-19 10:27:30.989093	35
32	\N	\N	served	2025-09-22 08:54:49.824352	2025-09-22 08:56:08.457837	36
33	\N	\N	pending	2025-09-22 09:32:04.580673	2025-09-22 09:32:04.580687	37
\.


--
-- Data for Name: menu_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menu_items (id, name, price, category) FROM stdin;
1	Burger	8.99	FOOD
2	Pizza	12.99	FOOD
3	Salad	7.99	FOOD
4	Soda	2.99	DRINK
5	Coffee	3.99	DRINK
6	Tea Leaf Salad	6.99	FOOD
7	Chicken Curry	11.99	FOOD
8	Steak (Grill)	18.99	FOOD
9	Wine	7.99	ALCOHOL
10	Beer	5.99	ALCOHOL
11	Mohinga	4	FOOD
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, menu_item_id, quantity, price, special_requests) FROM stdin;
\.


--
-- Data for Name: order_staff_association; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_staff_association (order_id, user_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, table_number, order_type, status, created_at, updated_at, special_requests, created_by, total, order_data, table_id, customer_count, assigned_seats, customer_name, customer_phone, delivery_address, modifiers) FROM stdin;
1	\N	DINE_IN	PENDING	2025-09-17 08:37:42.050722	2025-09-17 08:37:42.050729	\N	\N	17.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 12.99, \\"category\\": \\"grill\\", \\"modifiers\\": []}, {\\"name\\": \\"Fries\\", \\"price\\": 4.99, \\"category\\": \\"sides\\", \\"modifiers\\": []}]"	\N	1	null	\N	\N	\N	null
2	\N	DINE_IN	PENDING	2025-09-17 08:41:54.810613	2025-09-17 08:41:54.810635	\N	\N	17.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 12.99, \\"category\\": \\"grill\\", \\"modifiers\\": []}, {\\"name\\": \\"Fries\\", \\"price\\": 4.99, \\"category\\": \\"sides\\", \\"modifiers\\": []}]"	\N	1	null	\N	\N	\N	null
3	\N	DINE_IN	PENDING	2025-09-17 08:49:41.241079	2025-09-17 08:49:41.241091	\N	\N	17.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 12.99, \\"category\\": \\"grill\\", \\"modifiers\\": []}, {\\"name\\": \\"Fries\\", \\"price\\": 4.99, \\"category\\": \\"sides\\", \\"modifiers\\": []}]"	\N	1	null	\N	\N	\N	null
4	\N	DINE_IN	PENDING	2025-09-17 08:54:43.354343	2025-09-17 08:54:43.354357	\N	\N	17.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 12.99, \\"category\\": \\"grill\\", \\"modifiers\\": []}, {\\"name\\": \\"Fries\\", \\"price\\": 4.99, \\"category\\": \\"sides\\", \\"modifiers\\": []}]"	\N	1	null	\N	\N	\N	null
5	\N	DINE_IN	PENDING	2025-09-17 09:08:12.011548	2025-09-17 09:08:12.011559	\N	\N	17.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 12.99, \\"category\\": \\"grill\\", \\"modifiers\\": []}, {\\"name\\": \\"Fries\\", \\"price\\": 4.99, \\"category\\": \\"sides\\", \\"modifiers\\": []}]"	\N	1	null	\N	\N	\N	null
6	3	DELIVERY	PENDING	2025-09-17 09:32:26.07167	2025-09-17 09:32:26.07176	\N	\N	11.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}, {\\"name\\": \\"Soda\\", \\"price\\": 2.99, \\"category\\": \\"drink\\", \\"modifiers\\": []}]"	\N	1	null	kyawmyohlaing	444455888\\	yangong hlaing township	null
7	\N	DELIVERY	PENDING	2025-09-18 02:44:11.921164	2025-09-18 02:44:11.921174	\N	\N	11.98	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}, {\\"name\\": \\"Soda\\", \\"price\\": 2.99, \\"category\\": \\"drink\\", \\"modifiers\\": []}]"	\N	1	null	aung	4554445	yangon	null
8	\N	DELIVERY	PENDING	2025-09-18 02:46:34.074209	2025-09-18 02:46:34.074212	\N	\N	6.99	"[{\\"name\\": \\"Tea Leaf Salad\\", \\"price\\": 6.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	zawzaw	4545455	Yangon Hlaing	null
9	\N	TAKEAWAY	PENDING	2025-09-18 02:53:52.804733	2025-09-18 02:53:52.804736	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	zawning	1231324123		null
10	3	DINE_IN	PENDING	2025-09-18 06:46:35.362607	2025-09-18 06:46:35.362611	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	3	1	null				null
11	4	DINE_IN	PENDING	2025-09-18 06:50:17.953623	2025-09-18 06:50:17.953627	\N	\N	19.97	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": [\\"cheek\\"]}, {\\"name\\": \\"Soda\\", \\"price\\": 2.99, \\"category\\": \\"drink\\", \\"modifiers\\": [\\"no sugar\\"]}, {\\"name\\": \\"Wine\\", \\"price\\": 7.99, \\"category\\": \\"alcohol\\", \\"modifiers\\": [\\"no alohol\\"]}]"	\N	1	null				null
12	3	DINE_IN	PENDING	2025-09-18 06:58:53.051078	2025-09-18 06:58:53.18278	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	2	1	null				null
13	4	DINE_IN	PENDING	2025-09-18 09:39:50.722525	2025-09-18 09:39:50.768769	\N	\N	12.99	"[{\\"name\\": \\"Pizza\\", \\"price\\": 12.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	3	1	null				null
14	4	DINE_IN	PENDING	2025-09-19 07:01:14.991524	2025-09-19 07:01:15.098748	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	3	1	null				null
15	\N	TAKEAWAY	PENDING	2025-09-19 07:05:10.207078	2025-09-19 07:05:10.207082	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	kyaw	45445445		null
16	\N	TAKEAWAY	PENDING	2025-09-19 07:07:00.340487	2025-09-19 07:07:00.340491	\N	\N	11.99	"[{\\"name\\": \\"Chicken Curry\\", \\"price\\": 11.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	aung	12123123		null
17	\N	DELIVERY	PENDING	2025-09-19 07:08:16.854981	2025-09-19 07:08:16.854984	\N	\N	12.99	"[{\\"name\\": \\"Pizza\\", \\"price\\": 12.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	aungaung	333333	yangon hlaing	null
18	3	DINE_IN	PENDING	2025-09-19 07:23:19.933685	2025-09-19 07:23:20.035021	\N	\N	12.99	"[{\\"name\\": \\"Pizza\\", \\"price\\": 12.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	2	1	null				null
19	3	DINE_IN	PENDING	2025-09-19 07:52:49.426384	2025-09-19 07:52:49.679204	\N	\N	4	"[{\\"name\\": \\"Mohinga\\", \\"price\\": 4.0, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	2	1	null				null
20	1	DINE_IN	PENDING	2025-09-19 08:03:30.78064	2025-09-19 08:03:30.887763	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Test Customer	123-456-7890	\N	null
21	1	DINE_IN	PENDING	2025-09-19 08:04:03.784047	2025-09-19 08:04:03.798792	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Stock Test Customer	123-456-7890	\N	null
22	1	DINE_IN	PENDING	2025-09-19 08:08:30.054895	2025-09-19 08:08:30.073644	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Stock Test Customer	123-456-7890	\N	null
23	2	DINE_IN	PENDING	2025-09-19 08:09:21.896813	2025-09-19 08:09:21.905658	\N	\N	4	"[{\\"name\\": \\"Mohinga\\", \\"price\\": 4.0, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	4	1	null				null
24	1	DINE_IN	PENDING	2025-09-19 08:15:46.371349	2025-09-19 08:15:46.631229	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Stock Test Customer	123-456-7890	\N	null
25	1	DINE_IN	PENDING	2025-09-19 08:15:55.056485	2025-09-19 08:15:55.072039	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Test Customer	123-456-7890	\N	null
26	\N	TAKEAWAY	PENDING	2025-09-19 08:15:56.356586	2025-09-19 08:15:56.356591	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	\N	null
27	\N	DELIVERY	PENDING	2025-09-19 08:15:57.634135	2025-09-19 08:15:57.634139	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	123 Test Street, Test City	null
28	1	DINE_IN	PENDING	2025-09-19 08:29:03.295027	2025-09-19 08:29:03.907846	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Test Customer	123-456-7890	\N	null
29	\N	TAKEAWAY	PENDING	2025-09-19 08:29:06.708539	2025-09-19 08:29:06.708544	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	\N	null
30	\N	DELIVERY	PENDING	2025-09-19 08:29:12.604183	2025-09-19 08:29:12.604188	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	123 Test Street, Test City	null
31	\N	TAKEAWAY	PENDING	2025-09-19 08:37:10.69904	2025-09-19 08:37:10.69905	\N	\N	2.99	"[{\\"name\\": \\"Soda\\", \\"price\\": 2.99, \\"category\\": \\"drink\\", \\"modifiers\\": []}]"	\N	1	null	kyaw	7987899899		null
32	1	DINE_IN	PENDING	2025-09-19 08:59:07.300475	2025-09-19 08:59:07.412941	\N	\N	5.99	"[{\\"name\\": \\"Test Item\\", \\"price\\": 5.99, \\"category\\": \\"test\\", \\"modifiers\\": []}]"	1	1	null	\N	123-456-7890	\N	null
33	\N	TAKEAWAY	PENDING	2025-09-19 08:59:19.257358	2025-09-19 08:59:19.257363	\N	\N	5.99	"[{\\"name\\": \\"Test Item\\", \\"price\\": 5.99, \\"category\\": \\"test\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	\N	null
34	\N	DELIVERY	PENDING	2025-09-19 08:59:22.545277	2025-09-19 08:59:22.545281	\N	\N	5.99	"[{\\"name\\": \\"Test Item\\", \\"price\\": 5.99, \\"category\\": \\"test\\", \\"modifiers\\": []}]"	\N	1	null	Test Customer	123-456-7890	123 Test Street	null
35	1	DINE_IN	PENDING	2025-09-19 10:27:30.800751	2025-09-19 10:27:30.91836	\N	\N	8.99	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	1	1	null	Stock Test Customer	123-456-7890	\N	null
36	5	DINE_IN	PENDING	2025-09-22 08:54:49.713501	2025-09-22 08:54:49.777919	\N	\N	19.97	"[{\\"name\\": \\"Burger\\", \\"price\\": 8.99, \\"category\\": \\"food\\", \\"modifiers\\": []}, {\\"name\\": \\"Soda\\", \\"price\\": 2.99, \\"category\\": \\"drink\\", \\"modifiers\\": []}, {\\"name\\": \\"Wine\\", \\"price\\": 7.99, \\"category\\": \\"alcohol\\", \\"modifiers\\": []}]"	5	1	null				null
37	3	DINE_IN	PENDING	2025-09-22 09:32:04.231337	2025-09-22 09:32:04.350169	\N	\N	12.99	"[{\\"name\\": \\"Pizza\\", \\"price\\": 12.99, \\"category\\": \\"food\\", \\"modifiers\\": []}]"	2	1	null				null
\.


--
-- Data for Name: stock_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stock_transactions (id, ingredient_id, transaction_type, quantity, unit, cost, notes, created_at) FROM stdin;
1	1	usage	7	kg	\N	\N	2025-09-18 09:52:25.048402
2	3	usage	1	kg	\N	\N	2025-09-19 07:52:50.011975
3	1	usage	1	kg	\N	\N	2025-09-19 07:57:55.230149
4	2	usage	1	5	\N	\N	2025-09-19 08:03:31.360715
5	1	usage	1	kg	\N	\N	2025-09-19 08:03:31.49365
6	2	usage	1	5	\N	\N	2025-09-19 08:04:03.97583
7	1	usage	1	kg	\N	\N	2025-09-19 08:04:04.066819
8	2	usage	1	5	\N	\N	2025-09-19 08:08:30.276469
9	1	usage	1	kg	\N	\N	2025-09-19 08:08:30.325275
10	3	usage	1	kg	\N	\N	2025-09-19 08:09:22.055221
11	4	usage	1	pieces	\N	\N	2025-09-19 08:09:22.096667
12	2	usage	1	5	\N	\N	2025-09-19 08:15:47.755385
13	1	usage	1	kg	\N	\N	2025-09-19 08:15:47.862579
14	2	usage	1	5	\N	\N	2025-09-19 08:15:55.259914
15	1	usage	1	kg	\N	\N	2025-09-19 08:15:55.291105
16	2	usage	1	5	\N	\N	2025-09-19 08:15:56.561491
17	1	usage	1	kg	\N	\N	2025-09-19 08:15:56.591626
18	2	usage	1	5	\N	\N	2025-09-19 08:15:57.803532
19	1	usage	1	kg	\N	\N	2025-09-19 08:15:57.833641
20	2	usage	1	5	\N	\N	2025-09-19 08:29:04.816781
21	1	usage	1	kg	\N	\N	2025-09-19 08:29:04.931023
22	2	usage	1	5	\N	\N	2025-09-19 08:29:07.721639
23	1	usage	1	kg	\N	\N	2025-09-19 08:29:08.844072
24	2	usage	1	5	\N	\N	2025-09-19 08:29:16.328568
25	1	usage	1	kg	\N	\N	2025-09-19 08:29:30.744928
26	2	purchase	10	kg	5	\N	2025-09-19 08:30:36.534447
27	1	usage	1	kg	\N	\N	2025-09-19 10:27:31.366179
28	2	usage	1	5	\N	\N	2025-09-19 10:27:31.439302
29	1	usage	1	kg	\N	\N	2025-09-22 08:54:50.134224
30	2	usage	1	5	\N	\N	2025-09-22 08:54:50.206773
31	4	usage	10	pieces	\N	\N	2025-09-22 09:32:06.802252
32	2	usage	1	1	\N	\N	2025-09-22 09:32:07.031914
\.


--
-- Data for Name: tables; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tables (id, table_number, capacity, is_occupied, current_order_id, status, seats) FROM stdin;
4	2	4	t	23	occupied	[{"seat_number": 1, "status": "available", "customer_name": null}, {"seat_number": 2, "status": "available", "customer_name": null}, {"seat_number": 3, "status": "available", "customer_name": null}, {"seat_number": 4, "status": "available", "customer_name": null}]
1	1	4	t	35	occupied	[{"seat_number": 1, "status": "available", "customer_name": null}, {"seat_number": 2, "status": "available", "customer_name": null}, {"seat_number": 3, "status": "available", "customer_name": null}, {"seat_number": 4, "status": "available", "customer_name": null}]
3	4	8	t	14	occupied	[{"seat_number": 1, "status": "available", "customer_name": null}, {"seat_number": 2, "status": "available", "customer_name": null}, {"seat_number": 3, "status": "available", "customer_name": null}, {"seat_number": 4, "status": "available", "customer_name": null}, {"seat_number": 5, "status": "available", "customer_name": null}, {"seat_number": 6, "status": "available", "customer_name": null}, {"seat_number": 7, "status": "available", "customer_name": null}, {"seat_number": 8, "status": "available", "customer_name": null}]
5	5	4	t	36	occupied	[{"seat_number": 1, "status": "available", "customer_name": null}, {"seat_number": 2, "status": "available", "customer_name": null}, {"seat_number": 3, "status": "available", "customer_name": null}, {"seat_number": 4, "status": "available", "customer_name": null}]
2	3	8	t	37	occupied	[{"seat_number": 1, "status": "available", "customer_name": null}, {"seat_number": 2, "status": "available", "customer_name": null}, {"seat_number": 3, "status": "available", "customer_name": null}, {"seat_number": 4, "status": "available", "customer_name": null}, {"seat_number": 5, "status": "available", "customer_name": null}, {"seat_number": 6, "status": "available", "customer_name": null}, {"seat_number": 7, "status": "available", "customer_name": null}, {"seat_number": 8, "status": "available", "customer_name": null}]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, hashed_password, learning_path, progress, role) FROM stdin;
1	Example User	user@example.com	$2b$12$AufmuYsiDKAjCgOcIpUtg.EQeQuiFSvHCxml0ykfJ6dajPoRWiTvq	\N	\N	\N
\.


--
-- Name: ingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingredients_id_seq', 4, true);


--
-- Name: invoices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_id_seq', 44, true);


--
-- Name: kitchen_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kitchen_orders_id_seq', 33, true);


--
-- Name: menu_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menu_items_id_seq', 11, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 37, true);


--
-- Name: stock_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stock_transactions_id_seq', 32, true);


--
-- Name: tables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tables_id_seq', 5, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- Name: invoices invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);


--
-- Name: kitchen_orders kitchen_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kitchen_orders
    ADD CONSTRAINT kitchen_orders_pkey PRIMARY KEY (id);


--
-- Name: menu_items menu_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_items
    ADD CONSTRAINT menu_items_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: stock_transactions stock_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_transactions
    ADD CONSTRAINT stock_transactions_pkey PRIMARY KEY (id);


--
-- Name: tables tables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_pkey PRIMARY KEY (id);


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
-- Name: ix_ingredients_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ingredients_id ON public.ingredients USING btree (id);


--
-- Name: ix_ingredients_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_ingredients_name ON public.ingredients USING btree (name);


--
-- Name: ix_invoices_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_invoices_id ON public.invoices USING btree (id);


--
-- Name: ix_invoices_invoice_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_invoices_invoice_number ON public.invoices USING btree (invoice_number);


--
-- Name: ix_kitchen_orders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_kitchen_orders_id ON public.kitchen_orders USING btree (id);


--
-- Name: ix_menu_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_menu_items_id ON public.menu_items USING btree (id);


--
-- Name: ix_menu_items_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_menu_items_name ON public.menu_items USING btree (name);


--
-- Name: ix_order_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_id ON public.order_items USING btree (id);


--
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- Name: ix_stock_transactions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stock_transactions_id ON public.stock_transactions USING btree (id);


--
-- Name: ix_tables_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tables_id ON public.tables USING btree (id);


--
-- Name: ix_tables_table_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_tables_table_number ON public.tables USING btree (table_number);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_name ON public.users USING btree (username);


--
-- Name: kitchen_orders fk_kitchen_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kitchen_orders
    ADD CONSTRAINT fk_kitchen_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: invoices invoices_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: item_ingredients item_ingredients_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_ingredients
    ADD CONSTRAINT item_ingredients_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id);


--
-- Name: item_ingredients item_ingredients_menu_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_ingredients
    ADD CONSTRAINT item_ingredients_menu_item_id_fkey FOREIGN KEY (menu_item_id) REFERENCES public.menu_items(id);


--
-- Name: order_items order_items_menu_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_menu_item_id_fkey FOREIGN KEY (menu_item_id) REFERENCES public.menu_items(id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: order_staff_association order_staff_association_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_staff_association
    ADD CONSTRAINT order_staff_association_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: order_staff_association order_staff_association_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_staff_association
    ADD CONSTRAINT order_staff_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: orders orders_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: orders orders_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- Name: stock_transactions stock_transactions_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_transactions
    ADD CONSTRAINT stock_transactions_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id);


--
-- Name: tables tables_current_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_current_order_id_fkey FOREIGN KEY (current_order_id) REFERENCES public.orders(id);


--
-- PostgreSQL database dump complete
--

\unrestrict wSWETfTsMlpK7DweWDifCuCHerx3wCziEi07ZTTsNTzdcy7FPWQvy46c4QmmN8u

