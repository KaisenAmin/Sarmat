import argparse
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from colorama import init, Fore
from .base import Base
from .user import User
from .server import Server
from .user_server import user_server_table
from .log import Log

init(autoreset=True)

def create_connection():
    try:
        global password, username, host

        conn = psycopg2.connect(
                dbname="postgres",
                user=username,
                host=host,
                password=password
            )
        conn.autocommit = True

        cursor = conn.cursor()

        return conn, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(Fore.RED + str(error))


def create_db(db_name: str):
    try:
        conn, cursor = create_connection()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")

        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(Fore.GREEN + f"{db_name} Database are created")
        else:
            print(Fore.YELLOW + f"{db_name} Database exist")    

        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(Fore.RED + str(error))


def create_table(engine, table_name: str):
    # Reflect existing tables
    Base.metadata.reflect(engine)

    if table_name in Base.metadata.tables:
        Base.metadata.tables[table_name].create(bind=engine, checkfirst=True)
        print(Fore.GREEN + f"Table {table_name} has been created.")

    else:
        print(Fore.YELLOW + f"Table {table_name} not found in SQLAlchemy models.")


def delete_table(db_url: str, table_name: str):
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as curs:
                curs.execute(f"SELECT to_regclass('{table_name}')")
                exists = curs.fetchone()[0] is not None
                if exists:
                    curs.execute(f"DROP TABLE {table_name}")
                    print(Fore.GREEN + f"Table {table_name} has been dropped.")
                else:
                    print(Fore.YELLOW + f"Table {table_name} does not exist.")
            conn.commit()

    except Exception as error:
        print(Fore.RED + str(error))


def list_tables(db_url: str):
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as curs:
                curs.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = curs.fetchall()
                print(Fore.GREEN + "Tables in the database:")
                for table in tables:
                    print(Fore.CYAN + "- " + table[0])
            conn.commit()

    except Exception as error:
        print(Fore.RED + str(error))


def list_tables_columns(db_url: str):
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as curs:
                curs.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = curs.fetchall()
                print(Fore.GREEN + "Tables in the database:")
                for table in tables:
                    print(Fore.GREEN + "- " + table[0])
                    curs.execute("""
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_name = %s
                    """, (table[0],))
                    columns = curs.fetchall()
                    for column in columns:
                        print(Fore.CYAN + f"   - {column[0]} ({column[1]})")
            conn.commit()

    except Exception as error:
        print(Fore.RED + str(error))


def delete_all_tables(db_url: str):
    question: str = input(Fore.RED + "WHAT THE FUCK YOU REALLY WANT TO DELETE ALL TABLES(DATA)???(YES|NO) : ")
    if question.lower() == 'yes':
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as curs:
                curs.execute("DROP SCHEMA IF EXISTS public CASCADE")
                curs.execute("CREATE SCHEMA public")
            conn.commit()
        print(Fore.RED + "all tables are deleted")


def create_db_tables(db_name: str):
    create_db(db_name)
    Base.metadata.create_all(bind=engine)
    print(Fore.GREEN + "all tables are created")


def get_table_size(db_url: str, table_name: str = None):
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as curs:
                if table_name:
                    curs.execute("""
                        SELECT 
                            '%s' AS "Table",
                            pg_size_pretty(pg_total_relation_size('%s')) AS "Size"
                    """ % (table_name, table_name))
                else:
                    curs.execute("""
                        SELECT 
                            table_name AS "Table",
                            pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')) AS "Size"
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                    """)
                results = curs.fetchall()
                print(Fore.GREEN + "Table Sizes:")
                for result in results:
                    print(Fore.CYAN + f"- \"{result[0]}\": {result[1]}")
            conn.commit()

    except Exception as error:
        print(Fore.RED + str(error))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Postgres database.')
    parser.add_argument('-d', '--dbname', required=True, help='The name of the database.')
    parser.add_argument('-u', '--username', required=True, help='The username of the database.')
    parser.add_argument('-p', '--password', required=True, help='The password of the database.')
    parser.add_argument('-ho', '--host', required=True, help='The host of the database.')
    parser.add_argument('-c', '--create', action='store_true', help='Create the database and all tables.')
    parser.add_argument('-del', '--delete', action='store_true', help='Delete the all tables in database.')
    parser.add_argument('-dt', '--delete_table', help='Delete a specific table in the database.')
    parser.add_argument('-ct', '--create_table', help='Create a specific table in the database.')
    parser.add_argument('-lt', '--list_tables', action='store_true', help='List all tables in the database.')
    parser.add_argument('-ltc', '--list_tables_columns', action='store_true', help='List all tables in the database and columns.')
    parser.add_argument('-s', '--size', nargs='?', const='all', help='Get the size of a specific table or all tables.')


    args = parser.parse_args()

    db_name: str = args.dbname
    password: str = args.password
    host: str = args.host 
    username: str = args.username 

    try:
        DATABASE_URL = f"postgresql://{username}:{password}@{host}/{db_name}"
        engine = create_engine(DATABASE_URL)

        if args.create:
            create_db_tables(DATABASE_URL)

        if args.delete:
            delete_all_tables(DATABASE_URL)

        if args.delete_table:
            delete_table(DATABASE_URL, args.delete_table)

        if args.delete:
            delete_all_tables(DATABASE_URL)

        if args.delete_table:
            delete_table(DATABASE_URL, args.delete_table)
            
        if args.create_table:
            create_table(engine, args.create_table)

        if args.list_tables:
            list_tables(DATABASE_URL)

        if args.list_tables_columns:
            list_tables_columns(DATABASE_URL)

        if args.size != "all":
            get_table_size(DATABASE_URL, args.size)
        else:
            get_table_size(DATABASE_URL)
        

    except Exception as error:
        print(Fore.RED + str(error))


    