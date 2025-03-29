
import psycopg2
from etl_config import load_config

# Function to connect to the database

def connect_to_db():
    # Load the configuration from the elt_config file
    config = load_config()
    db_config = config["database"]

    # Extract the credentials from the configuration
    conn = psycopg2.connect(
        dbname=db_config["database_name"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )
    conn.autocommit = True
    return conn
