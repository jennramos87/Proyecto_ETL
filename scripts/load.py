import pandas as pd
import os
import sqlalchemy
from sqlalchemy.types import Integer, String, DateTime, Float
from sqlalchemy import create_engine
from psycopg2 import connect, sql, errors
import psycopg2
import unidecode


# Funtion to conect to the database
def connect_to_db(db_config):
    """
    Establishes a connection to the database using the credentials from the configuration file.

    Args:
        db_config (dict): Dictionary containing the database credentials.

    Returns:
        sqlalchemy.engine.base.Engine: Database connection object.
    """
    return create_engine(
        f'postgresql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["name"]}'
    )



# Creating the database
def create_new_database(db_config, new_db_name):
    """
    Creates a new database using the provided configuration and database name.

    Args:
        db_config (dict): Dictionary containing the database credentials.
        new_db_name (str): Name of the new database to create.

    Returns:
        None
    """
    try:
        # Connect to the default database (e.g., postgres)
        conn = connect(
            dbname="postgres",
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        conn.autocommit = True  # Enable autocommit for database creation

        # Create the new database
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
            print(f"Database '{new_db_name}' created successfully.")
    except errors.DuplicateDatabase:
        print(f"Database '{new_db_name}' already exists.")
    except Exception as e:
        print(f"Error creating the database '{new_db_name}': {e}")
    finally:
        # Check if conn exists and close it
        if 'conn' in locals() and conn:
            conn.close()


# Function to load multiple tables into the database
def load_dataframes_to_db(dataframes, engine):
    """
    Iterates over a dictionary of DataFrames and loads them into the database.

    Args:
        dataframes (dict): Dictionary with the file name as the key and the DataFrame as the value.
        engine (sqlalchemy.engine.base.Engine): Database connection object.

    Returns:
        list: List of table names that were loaded into the database.
    """
    if not isinstance(dataframes, dict):
        raise TypeError("The 'dataframes' argument must be a dictionary with file names as keys and DataFrames as values.")
    
    loaded_tables = []

    for file_name, df in dataframes.items():
        # Create the table name based on the file name
        table_name = f"tabla_{file_name.split('.')[0]}"
        print(f"Loading data {file_name} into the table '{table_name}'...")

        try:
            
            # Load the data frame into the data base
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Data loaded into the table '{table_name}' in the database.")
    
            # Add the table name to the list of loaded tables
            loaded_tables.append(table_name)
        except Exception as e:
            print(f"Error al cargar los datos en la tabla '{table_name}': {e}")
        
    return loaded_tables



# Funtion to Load the combination of 1stCourse dataframes into the database
def load_combined_1st_course_to_db(df, engine):
    """
    Loads the combined DataFrame of the 1st Course data into the database.

    Args:
        df (pd.DataFrame): DataFrame containing the combined data of the 1st Course.
        engine (sqlalchemy.engine.base.Engine): Database connection object.
    """
    # Nombre de la nueva tabla
    table_name = 'Historico_Primer_Curso'

    # Definir el tipo de dato de cada columna
    dtype = {
        'CODIGO SNIES DEL PROGRAMA': Integer(),
        'SEXO': String(),
        'AÑO': Integer(),
        'PRIMER_CURSO': Integer(),
        'SEMESTRE': Integer()
    }
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype)
        print(f"Data loaded into the table '{table_name}' in the database.")
    except Exception as e:
        print(f"Error loading data into the table '{table_name}': {e}")




#cargar archivo csv leido como tabala en la base de datos.
def load_enrollment_df_to_db(df, table_name, engine):
    """
    Loads a CSV file into the database as a table.

    Args:
        file_path (str): Path to the CSV file.
        table_name (str): Name of the table to create in the database.
        engine (sqlalchemy.engine.base.Engine): Database connection object.
    """
    # Define the table schema
    metadata = sqlalchemy.MetaData()

    matricula_table = sqlalchemy.Table('table_name', metadata,
        sqlalchemy.Column('codigo_institucion', sqlalchemy.Integer),
        sqlalchemy.Column('ies_padre', sqlalchemy.Integer),
        sqlalchemy.Column('institucion_educacion_superior', sqlalchemy.String),
        sqlalchemy.Column('principal_seccional', sqlalchemy.String),
        sqlalchemy.Column('id_sector', sqlalchemy.Integer),
        sqlalchemy.Column('id_caracter', sqlalchemy.Integer),
        sqlalchemy.Column('codigo_departamento_ies', sqlalchemy.Integer),
        sqlalchemy.Column('departamento_domicilio_ies', sqlalchemy.String),
        sqlalchemy.Column('codigo_municipio_ies', sqlalchemy.Integer),
        sqlalchemy.Column('municipio_domicilio_ies', sqlalchemy.String),
        sqlalchemy.Column('codigo_snies_programa', sqlalchemy.Integer),
        sqlalchemy.Column('programa_academico', sqlalchemy.String),
        sqlalchemy.Column('id_nivel', sqlalchemy.Integer),
        sqlalchemy.Column('id_nivel_formacion', sqlalchemy.Integer),
        sqlalchemy.Column('id_metodologia', sqlalchemy.Integer),
        sqlalchemy.Column('id_area', sqlalchemy.String),
        sqlalchemy.Column('id_nucleo', sqlalchemy.String),
        sqlalchemy.Column('nucleo_basico_conocimiento', sqlalchemy.String),
        sqlalchemy.Column('codigo_departamento_programa', sqlalchemy.Integer),
        sqlalchemy.Column('departamento_oferta_programa', sqlalchemy.String),
        sqlalchemy.Column('codigo_municipio_programa', sqlalchemy.Integer),
        sqlalchemy.Column('municipio_oferta_programa', sqlalchemy.String),
        sqlalchemy.Column('id_genero', sqlalchemy.Integer),
        sqlalchemy.Column('ano', sqlalchemy.Integer),
        sqlalchemy.Column('semestre', sqlalchemy.Integer),
        sqlalchemy.Column('total_matriculados', sqlalchemy.Integer)
    )

    # Create the table in the database
    metadata.create_all(engine)

    # Insert the data from the DataFrame into the table
    df.to_sql('table_name', engine, if_exists='replace', index=False)
    print("Data inserted successfully.")



# Function to read multiple tables from the database
def read_tables_from_db(tabla_names, engine):
    """
    Reads multiple tables from the database based on the provided list of names.

    Args:
        tabla_names (list): List of table names that were loaded into the database.
        engine (sqlalchemy.engine.base.Engine): Database connection object.

    Returns:
        list: List of DataFrames corresponding to the tables.
    """
    dataframes = []
    for table_name in tabla_names:
        try:
            df = pd.read_sql(f'SELECT * FROM "{table_name}"', con=engine)
            dataframes.append(df)
            print(f"Data successfully read from the table '{table_name}'.")
        except Exception as e:
            print(f"Error reading the table '{table_name}': {e}")
    
    return dataframes



# Function to upload any DataFrame to the database
def load_dataframe_to_db(df, table_name, engine, dtype=None):
    """
    Uploads a DataFrame to the database as a table.

    Args:
        df (pd.DataFrame): DataFrame to upload.
        table_name (str): Name of the table to create in the database.
        engine (sqlalchemy.engine.base.Engine): Database connection object.
        dtype (dict, optional): Dictionary specifying the data types for the table columns. Defaults to None.
    """
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype)
        print(f"DataFrame successfully uploaded to the table '{table_name}' in the database.")
    except Exception as e:
        print(f"Error uploading DataFrame to the table '{table_name}': {e}") 