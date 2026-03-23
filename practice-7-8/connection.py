import sys
from config import load_config
from psycopg2.extensions import connection
from psycopg2 import connect, DatabaseError

def create_connection(config: dict[str, str] = load_config()) -> connection:
    try:
        with connect(**config) as connection:
            print("\033[92m[connected to the database]\033[0m\n")
            return connection
    except DatabaseError as error:
        print(f"\033[91m[{str(error).strip().replace(" FATAL: ", "")}]\033[0m\n")
        sys.exit(1)
