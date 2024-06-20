# %% [markdown]
# 
# # Course: **Generative AI for Data Science**
# 
# ## Session: **LAB_Building Systems with ChatGPT API**

# %%
import os
import sqlite3
import textwrap
from openai import AzureOpenAI
from dotenv import load_dotenv

_ = load_dotenv(r'env.txt') # read local .env file

# %% [markdown]
# ### Cliente y funciones

# %% [markdown]
# > A lo largo de este curso, utilizaremos el modelo  `gpt-35-turbo-0301` desplegado en **AZURE** . 

# %%
# Azure BBVA Client
bbva_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
model = 'gpt-35-turbo-0301' # model = "deployment_name". Siempre confirmar con el proveedor por el nombre del modelo exacto
# model = 'gpt-4-0613'



def get_chat_response(messages, 
                      model=model,
                      temperature=0,
                      max_tokens=450,
                      seed = None):

    response = bbva_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        seed=seed
        
    )
    return response.choices[0].message.content, response


# %%
prompt = [
    {"role": "system", "content": "Eres un asistente útil diseñado para producir JSON."},
    {"role": "user", "content": "¿Quién ganó la UEFA Champions League en 2022?"}
  ]

# %%
response = get_chat_response(messages= prompt)
response[0]




def wrap_text(text, width=100):
    return textwrap.fill(str(text), width)



def db_connection(db_name):
    # Crear una conexión a la base de datos (esto también crea la base de datos si no existe)
    conn = sqlite3.connect(db_name)

    # Crear un cursor
    cursor = conn.cursor()
    
    return conn, cursor



    # %%
schema = """

CREATE TABLE actor (
actor_id numeric NOT NULL ,
first_name VARCHAR(45) NOT NULL,
last_name VARCHAR(45) NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (actor_id)
)
;

CREATE  INDEX idx_actor_last_name ON actor(last_name)
;

CREATE TRIGGER actor_trigger_ai AFTER INSERT ON actor
BEGIN
UPDATE actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER actor_trigger_au AFTER UPDATE ON actor
BEGIN
UPDATE actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table country
--

CREATE TABLE country (
country_id SMALLINT NOT NULL,
country VARCHAR(50) NOT NULL,
last_update TIMESTAMP,
PRIMARY KEY  (country_id)
)
;

CREATE TRIGGER country_trigger_ai AFTER INSERT ON country
BEGIN
UPDATE country SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER country_trigger_au AFTER UPDATE ON country
BEGIN
UPDATE country SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table city
--

CREATE TABLE city (
city_id int NOT NULL,
city VARCHAR(50) NOT NULL,
country_id SMALLINT NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (city_id),
CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;
CREATE  INDEX idx_fk_country_id ON city(country_id)
;

CREATE TRIGGER city_trigger_ai AFTER INSERT ON city
BEGIN
UPDATE city SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER city_trigger_au AFTER UPDATE ON city
BEGIN
UPDATE city SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table address
--

CREATE TABLE address (
address_id int NOT NULL,
address VARCHAR(50) NOT NULL,
address2 VARCHAR(50) DEFAULT NULL,
district VARCHAR(20) NOT NULL,
city_id INT  NOT NULL,
postal_code VARCHAR(10) DEFAULT NULL,
phone VARCHAR(20) NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (address_id),
CONSTRAINT fk_address_city FOREIGN KEY (city_id) REFERENCES city (city_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;

CREATE  INDEX idx_fk_city_id ON address(city_id)
;

CREATE TRIGGER address_trigger_ai AFTER INSERT ON address
BEGIN
UPDATE address SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER address_trigger_au AFTER UPDATE ON address
BEGIN
UPDATE address SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table language
--

CREATE TABLE language (
language_id SMALLINT NOT NULL ,
name CHAR(20) NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY (language_id)
)
;

CREATE TRIGGER language_trigger_ai AFTER INSERT ON language
BEGIN
UPDATE language SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER language_trigger_au AFTER UPDATE ON language
BEGIN
UPDATE language SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table category
--

CREATE TABLE category (
category_id SMALLINT NOT NULL,
name VARCHAR(25) NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (category_id)
);

CREATE TRIGGER category_trigger_ai AFTER INSERT ON category
BEGIN
UPDATE category SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER category_trigger_au AFTER UPDATE ON category
BEGIN
UPDATE category SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table customer
--

CREATE TABLE customer (
customer_id INT NOT NULL,
store_id INT NOT NULL,
first_name VARCHAR(45) NOT NULL,
last_name VARCHAR(45) NOT NULL,
email VARCHAR(50) DEFAULT NULL,
address_id INT NOT NULL,
active CHAR(1) DEFAULT 'Y' NOT NULL,
create_date TIMESTAMP NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (customer_id),
CONSTRAINT fk_customer_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE NO ACTION ON UPDATE CASCADE,
CONSTRAINT fk_customer_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;

CREATE  INDEX idx_customer_fk_store_id ON customer(store_id)
;
CREATE  INDEX idx_customer_fk_address_id ON customer(address_id)
;
CREATE  INDEX idx_customer_last_name ON customer(last_name)
;

CREATE TRIGGER customer_trigger_ai AFTER INSERT ON customer
BEGIN
UPDATE customer SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER customer_trigger_au AFTER UPDATE ON customer
BEGIN
UPDATE customer SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table film
--

CREATE TABLE film (
film_id int NOT NULL,
title VARCHAR(255) NOT NULL,
description BLOB SUB_TYPE TEXT DEFAULT NULL,
release_year VARCHAR(4) DEFAULT NULL,
language_id SMALLINT NOT NULL,
original_language_id SMALLINT DEFAULT NULL,
rental_duration SMALLINT  DEFAULT 3 NOT NULL,
rental_rate DECIMAL(4,2) DEFAULT 4.99 NOT NULL,
length SMALLINT DEFAULT NULL,
replacement_cost DECIMAL(5,2) DEFAULT 19.99 NOT NULL,
rating VARCHAR(10) DEFAULT 'G',
special_features VARCHAR(100) DEFAULT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (film_id),
CONSTRAINT CHECK_special_features CHECK(special_features is null or
                                                        special_features like '%Trailers%' or
                                                        special_features like '%Commentaries%' or
                                                        special_features like '%Deleted Scenes%' or
                                                        special_features like '%Behind the Scenes%'),
CONSTRAINT CHECK_special_rating CHECK(rating in ('G','PG','PG-13','R','NC-17')),
CONSTRAINT fk_film_language FOREIGN KEY (language_id) REFERENCES language (language_id) ,
CONSTRAINT fk_film_language_original FOREIGN KEY (original_language_id) REFERENCES language (language_id)
)
;
CREATE  INDEX idx_fk_language_id ON film(language_id)
;
CREATE  INDEX idx_fk_original_language_id ON film(original_language_id)
;

CREATE TRIGGER film_trigger_ai AFTER INSERT ON film
BEGIN
UPDATE film SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER film_trigger_au AFTER UPDATE ON film
BEGIN
UPDATE film SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table film_actor
--

CREATE TABLE film_actor (
actor_id INT NOT NULL,
film_id  INT NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (actor_id,film_id),
CONSTRAINT fk_film_actor_actor FOREIGN KEY (actor_id) REFERENCES actor (actor_id) ON DELETE NO ACTION ON UPDATE CASCADE,
CONSTRAINT fk_film_actor_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;

CREATE  INDEX idx_fk_film_actor_film ON film_actor(film_id)
;

CREATE  INDEX idx_fk_film_actor_actor ON film_actor(actor_id) 
;

CREATE TRIGGER film_actor_trigger_ai AFTER INSERT ON film_actor
BEGIN
UPDATE film_actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER film_actor_trigger_au AFTER UPDATE ON film_actor
BEGIN
UPDATE film_actor SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;


--
-- Table structure for table film_category
--

CREATE TABLE film_category (
film_id INT NOT NULL,
category_id SMALLINT  NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY (film_id, category_id),
CONSTRAINT fk_film_category_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE NO ACTION ON UPDATE CASCADE,
CONSTRAINT fk_film_category_category FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;

CREATE  INDEX idx_fk_film_category_film ON film_category(film_id)
;

CREATE  INDEX idx_fk_film_category_category ON film_category(category_id)
;

CREATE TRIGGER film_category_trigger_ai AFTER INSERT ON film_category
BEGIN
UPDATE film_category SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER film_category_trigger_au AFTER UPDATE ON film_category
BEGIN
UPDATE film_category SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table film_text
--

CREATE TABLE film_text (
film_id SMALLINT NOT NULL,
title VARCHAR(255) NOT NULL,
description BLOB SUB_TYPE TEXT,
PRIMARY KEY  (film_id)
)
;

--
-- Table structure for table inventory
--

CREATE TABLE inventory (
inventory_id INT NOT NULL,
film_id INT NOT NULL,
store_id INT NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (inventory_id),
CONSTRAINT fk_inventory_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE NO ACTION ON UPDATE CASCADE,
CONSTRAINT fk_inventory_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;

CREATE  INDEX idx_fk_film_id ON inventory(film_id)
;

CREATE  INDEX idx_fk_film_id_store_id ON inventory(store_id,film_id)
;

CREATE TRIGGER inventory_trigger_ai AFTER INSERT ON inventory
BEGIN
UPDATE inventory SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER inventory_trigger_au AFTER UPDATE ON inventory
BEGIN
UPDATE inventory SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table staff
--

CREATE TABLE staff (
staff_id SMALLINT NOT NULL,
first_name VARCHAR(45) NOT NULL,
last_name VARCHAR(45) NOT NULL,
address_id INT NOT NULL,
picture BLOB DEFAULT NULL,
email VARCHAR(50) DEFAULT NULL,
store_id INT NOT NULL,
active SMALLINT DEFAULT 1 NOT NULL,
username VARCHAR(16) NOT NULL,
password VARCHAR(40) DEFAULT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (staff_id),
CONSTRAINT fk_staff_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE NO ACTION ON UPDATE CASCADE,
CONSTRAINT fk_staff_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE NO ACTION ON UPDATE CASCADE
)
;
CREATE  INDEX idx_fk_staff_store_id ON staff(store_id)
;

CREATE  INDEX idx_fk_staff_address_id ON staff(address_id)
;

CREATE TRIGGER staff_trigger_ai AFTER INSERT ON staff
BEGIN
UPDATE staff SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER staff_trigger_au AFTER UPDATE ON staff
BEGIN
UPDATE staff SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table store
--

CREATE TABLE store (
store_id INT NOT NULL,
manager_staff_id SMALLINT NOT NULL,
address_id INT NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (store_id),
CONSTRAINT fk_store_staff FOREIGN KEY (manager_staff_id) REFERENCES staff (staff_id) ,
CONSTRAINT fk_store_address FOREIGN KEY (address_id) REFERENCES address (address_id)
)
;

CREATE  INDEX idx_store_fk_manager_staff_id ON store(manager_staff_id)
;

CREATE  INDEX idx_fk_store_address ON store(address_id)
;

CREATE TRIGGER store_trigger_ai AFTER INSERT ON store
BEGIN
UPDATE store SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER store_trigger_au AFTER UPDATE ON store
BEGIN
UPDATE store SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

--
-- Table structure for table payment
--

CREATE TABLE payment (
payment_id int NOT NULL,
customer_id INT  NOT NULL,
staff_id SMALLINT NOT NULL,
rental_id INT DEFAULT NULL,
amount DECIMAL(5,2) NOT NULL,
payment_date TIMESTAMP NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY  (payment_id),
CONSTRAINT fk_payment_rental FOREIGN KEY (rental_id) REFERENCES rental (rental_id) ON DELETE SET NULL ON UPDATE CASCADE,
CONSTRAINT fk_payment_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ,
CONSTRAINT fk_payment_staff FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
)
;
CREATE  INDEX idx_fk_staff_id ON payment(staff_id)
;
CREATE  INDEX idx_fk_customer_id ON payment(customer_id)
;

CREATE TRIGGER payment_trigger_ai AFTER INSERT ON payment
BEGIN
UPDATE payment SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER payment_trigger_au AFTER UPDATE ON payment
BEGIN
UPDATE payment SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TABLE rental (
rental_id INT NOT NULL,
rental_date TIMESTAMP NOT NULL,
inventory_id INT  NOT NULL,
customer_id INT  NOT NULL,
return_date TIMESTAMP DEFAULT NULL,
staff_id SMALLINT  NOT NULL,
last_update TIMESTAMP NOT NULL,
PRIMARY KEY (rental_id),
CONSTRAINT fk_rental_staff FOREIGN KEY (staff_id) REFERENCES staff (staff_id) ,
CONSTRAINT fk_rental_inventory FOREIGN KEY (inventory_id) REFERENCES inventory (inventory_id) ,
CONSTRAINT fk_rental_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
)
;
CREATE INDEX idx_rental_fk_inventory_id ON rental(inventory_id)
;
CREATE INDEX idx_rental_fk_customer_id ON rental(customer_id)
;
CREATE INDEX idx_rental_fk_staff_id ON rental(staff_id)
;
CREATE UNIQUE INDEX   idx_rental_uq  ON rental (rental_date,inventory_id,customer_id)
;

CREATE TRIGGER rental_trigger_ai AFTER INSERT ON rental
BEGIN
UPDATE rental SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;

CREATE TRIGGER rental_trigger_au AFTER UPDATE ON rental
BEGIN
UPDATE rental SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
END
;
--
-- View structure for view customer_list
--

CREATE VIEW customer_list
AS
SELECT cu.customer_id AS ID,
    cu.first_name||' '||cu.last_name AS name,
    a.address AS address,
    a.postal_code AS zip_code,
    a.phone AS phone,
    city.city AS city,
    country.country AS country,
    case when cu.active=1 then 'active' else '' end AS notes,
    cu.store_id AS SID
FROM customer AS cu JOIN address AS a ON cu.address_id = a.address_id JOIN city ON a.city_id = city.city_id
    JOIN country ON city.country_id = country.country_id
;
--
-- View structure for view film_list
--

CREATE VIEW film_list
AS
SELECT film.film_id AS FID,
    film.title AS title,
    film.description AS description,
    category.name AS category,
    film.rental_rate AS price,
    film.length AS length,
    film.rating AS rating,
    actor.first_name||' '||actor.last_name AS actors
FROM category LEFT JOIN film_category ON category.category_id = film_category.category_id LEFT JOIN film ON film_category.film_id = film.film_id
        JOIN film_actor ON film.film_id = film_actor.film_id
    JOIN actor ON film_actor.actor_id = actor.actor_id
;

--
-- View structure for view staff_list
--

CREATE VIEW staff_list
AS
SELECT s.staff_id AS ID,
    s.first_name||' '||s.last_name AS name,
    a.address AS address,
    a.postal_code AS zip_code,
    a.phone AS phone,
    city.city AS city,
    country.country AS country,
    s.store_id AS SID
FROM staff AS s JOIN address AS a ON s.address_id = a.address_id JOIN city ON a.city_id = city.city_id
    JOIN country ON city.country_id = country.country_id
;
--
-- View structure for view sales_by_store
--

CREATE VIEW sales_by_store
AS
SELECT
s.store_id
,c.city||','||cy.country AS store
,m.first_name||' '||m.last_name AS manager
,SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN store AS s ON i.store_id = s.store_id
INNER JOIN address AS a ON s.address_id = a.address_id
INNER JOIN city AS c ON a.city_id = c.city_id
INNER JOIN country AS cy ON c.country_id = cy.country_id
INNER JOIN staff AS m ON s.manager_staff_id = m.staff_id
GROUP BY  
s.store_id
, c.city||','||cy.country
, m.first_name||' '||m.last_name
;
--
-- View structure for view sales_by_film_category
--
-- Note that total sales will add up to >100% because
-- some titles belong to more than 1 category
--

CREATE VIEW sales_by_film_category
AS
SELECT
c.name AS category
, SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN film AS f ON i.film_id = f.film_id
INNER JOIN film_category AS fc ON f.film_id = fc.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
GROUP BY c.name
;"""

# %%
prompt = [ {"role": "system", "content": f"""Eres un asistente útil diseñado para crear consultas SQL para SQLite3, tu salida solo será la consulta SQL, 
        si no conoces la consulta genera una consulta que conozcas pero de sola un elemento. La base de datos tiene como nombre sakila_master su schema 
        se encuantra a continuación entre los delimitadores ###: 
        
        ### 
        {schema}
        ###
        
        A continuación entren los delimitadores ### te muestro un ejemplo de consulta SQL con su pregunta y el output q debes crear debes crear:
        ###
        
        
        Pregunta1: Consulta para obtener todos los actores con apellido 'DAVIS'
        QUERY: SELECT * FROM actor WHERE last_name = 'DAVIS';
        
        Pregunta2: Consulta para listar todas las ciudades y sus respectivos países
        QUERY: SELECT city.city, country.country
        FROM city
        JOIN country ON city.country_id = country.country_id;
        
        Pregunta3: Consulta para obtener los primeros 10 clientes ordenados por apellido
        QUERY: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
        ###
        
        
        Para la conformación de la QUERY la prioridad es la eficiencia y la correctitud de la misma.
        tu salida debe ser solamente la QUERY SQL que responda a la pregunta.                            
        """}]

prompt = [
    {
        "role": "system",
        "content": f"""
        You are a helpful assistant designed to create SQL queries for SQLite3. Your output will only be the SQL query. If you do not know the query, generate a query you know but with only one element. The database is named sakila_master and its schema is provided below between the delimiters ###:
        
        ###
        {schema}
        ###
        
        Below, between the delimiters ###, I will show you an example of an SQL query with its question and the output you should create:
        ###
        
        Question1: Query to get all actors with the last name 'DAVIS'
        QUERY: SELECT * FROM actor WHERE last_name = 'DAVIS';
        
        Question2: Query to list all cities and their respective countries
        QUERY: SELECT city.city, country.country
        FROM city
        JOIN country ON city.country_id = country.country_id;
        
        Question3: Query to get the first 10 customers ordered by last name
        QUERY: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
        ###
        
        For the formation of the QUERY, the priority is efficiency and correctness.
        Your output should only be the SQL QUERY that answers the question.
        """
    }
]


def answer_query(message):

    prompt.append({"role": "user", "content": f"{message}"})
    response = get_chat_response(messages= prompt)
    return response[0]

def answer_table(cursor, query):
    try:
        cursor.execute(f"""
                   {query}
                   """)
        resultados = cursor.fetchmany(5)
        return resultados
    except Exception as e:
        return e

def check_query_message(message):
    """Función para verificar si un mensaje contiene una consulta SQL"""
    sys_prompt = [ {"role": "system", "content": """Eres un asistente útil diseñado para leer un mensaje y determinar si es solo una consulta SQL,
                tu salida solo será la consulta SQL encontrada, ignora todo el texto que no sea la consulta SQL.
                Ejemplos de mensaje:
                ###
                Mensaje: '''Claro aquí tienes la consulta SQL para obtener todos los actores con apellido 'DAVIS'
                 SELECT * FROM actor WHERE last_name = 'DAVIS';
                '''
                Output: SELECT * FROM actor WHERE last_name = 'DAVIS';
                
                Mensaje: '''Entendido te puedo ayudar con ello, la consulta es la siguiente:
                QUERY: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
                '''
                Output: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
                    
                Mensaje: '''Lo siento, como asistente de texto, no tengo la capacidad de mostrar visualmente el esquema de la base de datos. 
                Sin embargo, puedo ayudarte a entender el esquema de la base de datos basado en las declaraciones de creación de tablas que se proporcionan.
                '''
                Output: Consulta no encontrada
                ###
                Recuerda, solo puedes crear como salida la consulta SQL de tipo SELECT encontrada en el mensaje, nada extra.
                Si no hay una consulta SELECT, devuelve el texto: Consulta no encontrada"""}]
    
    sys_prompt = [
    {
        "role": "system",
        "content": """
        You are a helpful assistant designed to read a message and determine if it contains only an SQL query. Your output should only be the SQL query found, ignoring all text that is not the SQL query.

        Examples of messages:
        ###
        Message: '''Sure, here is the SQL query to get all actors with the last name 'DAVIS':
        SELECT * FROM actor WHERE last_name = 'DAVIS';
        '''
        Output: SELECT * FROM actor WHERE last_name = 'DAVIS';

        Message: '''Understood, I can help you with that, the query is as follows:
        QUERY: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
        '''
        Output: SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;

        Message: '''Sorry, as a text assistant, I don't have the ability to visually display the database schema. However, I can help you understand the database schema based on the provided table creation statements.
        '''
        Output: Query not found
        ###
        
        Remember, you can only output the SELECT SQL query found in the message, nothing extra.
        If there is no SELECT query, return the text: Query not found
        """
    }
]

    sys_prompt.append({"role": "user", "content": message})
    query_response = get_chat_response(messages= sys_prompt)
    return query_response[0]



if __name__ == "__main__":
    
    conn, cursor = db_connection('visual_interface_chat\sakila_master.db')
    print("Conexión a la base de datos exitosa")
    

    # # %%
    # # Hacer una consulta a la base de datos
    # cursor.execute('''
    # SELECT * FROM customer ORDER BY last_name ASC LIMIT 10;
    # ''')

    # # %%
    # resultados = cursor.fetchmany(5)
    # print(resultados)

    # # %%
    # # Obtener todos los resultados de la consulta
    # resultados = cursor.fetchall()
    # print(resultados)

    # %%
    prompt.append({"role": "user", "content": "Obtener todos los actores con apellido 'BERRY'"})
    response = get_chat_response(messages= prompt)
    print(response[0])

    # %%
    try:
        cursor.execute(f"""
                   {response[0]}
                   """)
        resultados = cursor.fetchmany(5)
        print(resultados)
    except Exception as e:
        print(e)
