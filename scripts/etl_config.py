# libraries
import yaml
import psycopg2 
from psycopg2 import sql
import pandas as pd


##############################
# Funtion to load configuration of database
def load_config(file_path="D:/JENN/Maestria IACD/ETL/ETL-Class-Project/config.yaml"):
    with open(file_path, "r") as file: # open the file on reading mode ("r")
        return yaml.safe_load(file) # load the file using yaml safe load and return the file content


DATABASE_CREDENTIALS = load_config()["database"] # Variable to load the database credentials from the config file

# Rutas de fuentes de datos
DATA_SOURCES = {
    "FIRST_COURSE": "D:/JENN/Maestria IACD/ETL/ETL-Class-Project/data/raw/1erCurso",
    "ENROLLMENT": "D:/JENN/Maestria IACD/ETL/ETL-Class-Project/data/raw/MEN_MATRICULA_ESTADISTICA_ES_20250222.csv",
    "PROGRAMS": "D:/JENN/Maestria IACD/ETL/ETL-Class-Project/data/raw/Programs.xlsx"
}

# Keywords used to filter columns on Frist Course data
KEYWORDS_1STCOURSE = ['SNIES', 'SEXO', 'AÑO', 'ANO', 'PRIMER', 'CURSO', 'SEMESTRE']

# Centralized configuration to a modular ETL.
# This configuration can be loaded from a file or defined in the code.
# In this case, it is define it in the code.
# The configuration specifies the tasks to be executed and their description.
# The configuration also specifies the log level and the output directory.
# the log level can be "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL".
# The output directory is the directory where the output files will be saved.
# The configuration is a dictionary with two keys:
# - etl_tasks: dictionary with the tasks to be executed.    
# - general_settings: dictionary with the log level and the output directory.
# Each task is a dictionary with two keys:
# - enabled: boolean that indicates if the task is enabled.
# - description: string with the description of the task.


# ETL Task configuration
# allows to enable or disable stages of the ETL process without modifying the main flow, 
# which is useful in dynamic projects or during testing.
ETL_TASKS = {
    "extract": {
        "enabled": True,
        "description": "Extraer datos de las fuentes especificadas."
    },
    "transform": {
        "enabled": True,
        "description": "Transformar los datos según las reglas de negocio."
    },
    "load": {
        "enabled": True,
        "description": "Cargar los datos transformados en el destino."
    }
}

# Logs configuration: allows to configure the log level and the output file for the logs.
LOGGING_CONFIG = {
    "log_file": "D:/JENN/Maestria IACD/ETL/ETL-Class-Project/logs/etl.log",
    "log_level": "INFO"
}