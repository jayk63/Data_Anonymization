import streamlit as st
import mysql.connector
import psycopg2
import anon
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta


fake = Faker()

def random_integer(max_value):
    return random.randint(0, max_value)


def fake_email():
    return fake.email()

def fake_first_name(value):
    fake = Faker()
    return fake.first_name()

def fake_last_name(value):
    return fake.last_name()

def fake_address():
    return fake.street_address()

def fake_city():
    return fake.city()

def fake_country():
    return fake.country()

def fake_postcode():
    return fake.postcode()

def random_zip():
    return str(random.randint(10000, 99999))

def generalize_daterange():
    return '2020-01-01 to 2020-12-31'

def generalize_numrange():
    return '1 to 100'

def generalize_timestamp():
    return '2020-01-01 00:00:00'

def partial_masking(data):
    return data[:4] + '*' * (len(data) - 4)

def full_masking(data):
    return '*' * len(data)

def randomized_date():
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2020-12-31', '%Y-%m-%d')
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

def convert_to_Confidential(data):
    return 'Confidential'

def random_mobile_number():
    return ''.join(random.choices('0123456789', k=10))

def Random_String():
    return fake.random_letters(length=10)

def Random_In(data):
    return random.choice(data)


def connect_to_mysql(connection_url):
    try:
        conn = mysql.connector.connect(
            host=connection_url['host'],
            port=connection_url['port'],
            user=connection_url['user'],
            password=connection_url['password'],
            database=connection_url['database']
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return conn, tables, None
    except mysql.connector.Error as e:
        return None, [], f"Error connecting to MySQL database: {e}"

def connect_to_postgres(connection_url):
    try:
        conn = psycopg2.connect(
            host=connection_url['host'],
            port=connection_url['port'],
            user=connection_url['user'],
            password=connection_url['password'],
            database=connection_url['database']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        cursor.close()
        return conn, tables, None
    except psycopg2.Error as e:
        return None, [], f"Error connecting to PostgreSQL database: {e}"
   
def connect_to_main_database(connection_url):
    try:
        conn = psycopg2.connect(
            host=connection_url['host'],
            port=connection_url['port'],
            user=connection_url['user'],
            password=connection_url['password'],
            database=connection_url['database']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        cursor.close()
        return conn, tables, None
    except psycopg2.Error as e:
        return None, [], f"Error connecting to PostgreSQL database: {e}"


def main():
    
    st.title("Database Connection")
    # Input fields for connection parameters
    connection_type = st.radio("Select Database Type", ("MySQL", "PostgreSQL"))
    host = st.text_input("Host", "localhost")
    port = st.number_input("Port", value=3306 if connection_type == "MySQL" else 5432, step=1)
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database Name")

    connection_url = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database
    }

    if st.button("Connect"):
        if connection_type == "MySQL":
            conn, tables, error = connect_to_mysql(connection_url)
        elif connection_type == "PostgreSQL":
            conn, tables, error = connect_to_postgres(connection_url)
       
        if error:
            st.error(error)
        elif not tables:
            st.warning("No tables found in the selected database.")
        else:
            st.success("Connected to database successfully!")

            # Dropdown menu to select table
            selected_table = st.selectbox("Select Table", tables)
            st.write("You selected:", selected_table)


            connection_url_main = {
                'host': 'localhost',
                'port': '5432',
                'user': 'loki',
                'password': "123",
                'database': 'anonymizer2'
            }

            main_conn,tables_main,error = connect_to_main_database(connection_url_main)
            
            main_cursor = main_conn.cursor()


            querym = """
                SELECT * FROM policy_rule_details
                WHERE prule_id IN (SELECT prule_id FROM policy_rule_name 
                    WHERE pid IN (SELECT pid FROM user_mapping_details WHERE db_user = %s AND pid IN (
                            SELECT pid 
                            FROM policy 
                            WHERE conn_id = (
                                SELECT conn_id 
                                FROM connection_details 
                                WHERE db_name = %s
                            )
                        )
                    )
                    AND table_name = %s
                );
            """

            main_cursor.execute(querym, (user, database, selected_table))
            rows = main_cursor.fetchall()
            columns = [desc[0] for desc in main_cursor.description]
            main_df = pd.DataFrame(rows, columns=columns)
            main_cursor.close()
            st.write("Main Database tables:")
            st.write("")
            st.write("Postgress")
            st.dataframe(main_df)

            query = 'SELECT * FROM {}'.format(selected_table[0])
            user_df = pd.read_sql(query,conn)
            st.dataframe(user_df)
            conn.close()

            
            def apply_transformations_to_user_df(user_df, main_df):
                transformed_user_df = user_df.copy()
                print(main_df)
                for index, row in main_df.iterrows():
                    column_name = row['column_name']
                    function_name = row['function_name']
                                        
                    print("Applying transformation for column:", column_name)
                    print("Using function:", function_name)
                    
                    if function_name and column_name in transformed_user_df.columns:
                        function = globals().get(function_name)
                        if function is not None:  # Check if function exists
                            transformed_user_df[column_name] = transformed_user_df[column_name].apply(function)
                            print("Transformation applied successfully")

                return transformed_user_df




            transformed_user_df = apply_transformations_to_user_df(user_df, main_df)
            st.dataframe(transformed_user_df)


            


if __name__ == "__main__":
    main()





