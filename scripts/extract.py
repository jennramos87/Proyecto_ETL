#libraries 
import pandas as pd
import os
from sqlalchemy import create_engine
from psycopg2 import connect, sql, errors
import unidecode


# Function to read an Excel file and create a DataFrame
def read_dataframe_from_excel(file_path):
    """
    Reads an Excel file and creates a DataFrame.

    Args:
    file_path (str): Path to the Excel file.

    Returns:
    DataFrame: A pandas DataFrame containing the data from the Excel file.
    """
    if not os.path.isfile(file_path):
        raise ValueError("The provided file_path must be a valid file.")

    try:
        df = pd.read_excel(file_path)
        print(f"File {file_path} read successfully.")
        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    


# Function to generate a list of DataFrames from Excel files
def extract_dataframes_from_excel(folder_path):
    """ 
    Extracts DataFrames from Excel files in a folder and returns a dictionary.

    Args:
    folder_path (str): Path to the folder containing the Excel files.

    Returns:
    dict: A dictionary with the file name as the key and the DataFrame as the value.
    """
    if not os.path.isdir(folder_path):
        raise ValueError("The provided folder_path must be a valid directory.")

    dataframes_dict = {}  # Create a dictionary to store DataFrames
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_excel(file_path, header=None)  # Read the Excel file
                df.columns = df.iloc[0]  # First row as header
                df = df[1:]  # Eliminate first row
                df.columns = df.columns.str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
                dataframes_dict[filename] = df  # Add the DataFrame to the dictionary
                print(f"File {filename} loaded successfully.")
            except Exception as e:
                print(f"Error loading file {filename}: {e}")

    if not dataframes_dict:  # Mensaje opcional si no se encontró ningún archivo Excel
        print("No se encontraron archivos Excel en el directorio especificado.")

    return dataframes_dict



# Function to extract a DataFrame from a CSV file
def extract_csv_to_dataframe(file_path, delimiter=','):
    """
    Extracts a DataFrame from a CSV file.

    Args:
    file_path (str): Path to the CSV file.
    delimiter (str): Delimiter used in the CSV file. Default is ','.

    Returns:
    DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    if not os.path.isfile(file_path):
        raise ValueError("The provided file_path must be a valid file.")

    try:
        df = pd.read_csv(file_path, sep=delimiter)
        pd.set_option('display.max_columns', None)  # Display all columns
        print(f"File {file_path} loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

