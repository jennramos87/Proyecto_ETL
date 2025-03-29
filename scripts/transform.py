
import pandas as pd
import re
import logging
from sqlalchemy.types import Integer, String, DateTime, Float

logging.basicConfig(level=logging.INFO)



# Function to clean and standardize column names
def standardize_column_names(df):
    """
    Standardizes column names by converting them to lowercase, removing accents, 
    replacing spaces with underscores, and removing special characters.
    
    Args:
        df (pd.DataFrame): DataFrame to process.
    
    Returns:
        pd.DataFrame: DataFrame with standardized column names.
    """
    def remove_accents(input_str):
        return re.sub(r'[áàäâã]', 'a', 
               re.sub(r'[éèëê]', 'e', 
               re.sub(r'[íìïî]', 'i', 
               re.sub(r'[óòöôõ]', 'o', 
               re.sub(r'[úùüû]', 'u', input_str.lower())))))

    df.columns = [remove_accents(col).replace(" ", "_").replace("-", "_").replace(r"[^a-zA-Z0-9_]", "") for col in df.columns]
    return df



# funtion to show the empties values in the DataFrame
def show_empty_values(df):
    """
    Shows the number of empty values in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze.
    """
    empty_values = df.isnull().sum() # Count the number of empty values in each column
    print(empty_values[empty_values > 0]) # Print columns with empty values
    


# funtion to eliminate the empty rows in the DataFrame
def drop_empty_rows(df):
    """
    Drops the rows with empty values in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: DataFrame without empty rows.
    """
    return df.dropna()



def drop_unnecessary_columns_programs_df(df):
    """
    Cleans the programs DataFrame by creating a copy and dropping unnecessary columns.

    Args:
        df (pd.DataFrame): Original DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame with selected columns.
    """
    df = standardize_column_names(df.copy())
    columns_to_drop = [
        'codigo_institucion', 'codigo_anterior_icfes', 'titulo_otorgado', 'justificacion',
        'justificacion_detallada', 'fecha_ejecutoria', 'resolucion_de_aprobacion',
        'fecha_de_resolucion', 'programa_en_convenio', 'vigencia_transitoria', 'vigencia_años',
        'observacion_decreto_1174_23'
    ]
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=columns_to_drop, inplace=True)
    return df


# Funtion to drop the rows with empty values in the DataFrame based on a threshold
def drop_empty_rows_by_threshold(df, threshold=0.1):
    """
    Drops the rows with empty values in the DataFrame based on a threshold.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
        threshold (float): Threshold as a fraction of the total number of columns.
    
    Returns:
        pd.DataFrame: DataFrame without rows that have empty values exceeding the threshold.
    """
    min_non_na_values = int(threshold * df.shape[1])
    return df.dropna(thresh=min_non_na_values)



# Funtion to remove the special characters from the column names in the DataFrame
def clean_special_characters(df):
    """
    Removes special characters from column names in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: DataFrame with cleaned column names.
    """
    df.columns = df.columns.str.replace(r"[^a-zA-Z\d\Ññ]+", "", regex=True)
    return df



# funtion to replace the NaN values with a default value in the DataFrame
def replace_nan_values(df, value=0):
    """
    Replaces NaN values with a default value in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
        value (int): Default value to replace NaN values.
    
    Returns:
        pd.DataFrame: DataFrame with NaN values replaced.
    """
    return df.fillna(value)



# funtion to convert the columns to integers in the DataFrame
def convert_columns_to_int(df, column):
    """
    Converts a single specified numeric column to integers in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to convert.
        column (str): Name of the column to convert to integers.
    
    Returns:
        pd.DataFrame: DataFrame with the specified column converted to integers, or unchanged if the column is not found.
    """
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df[column] = df[column].astype(pd.Int64Dtype())
    
    return df



# Function to add gender description to the DataFrame
def add_gender_description(df):
    """
    Adds the 'SEXO' column to the DataFrame based on the values of 'ID SEXO'.
    
    Args:
        df (pd.DataFrame): Original DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with the new 'SEXO' column.
    """
    df['SEXO'] = df['ID SEXO'].apply(lambda x: 'Masculino' if x == 1 else 'Femenino' if x == 2 else 'Desconocido')
    return df



# Function to rename specific columns in the DataFrame
def rename_columns(df):
    """
        Renames specific columns in the DataFrame.
        
        Args:
            df (pd.DataFrame): Original DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame with renamed columns.
        """
    df = df.rename(columns = {
        'CODIGO \nSNIES DEL\nPROGRAMA': 'CODIGO_SNIES_DEL_PROGRAMA',
        'CODIGO SNIES DEL PROGRAMA': 'CODIGO_SNIES_DEL_PROGRAMA',
        'MATRICULADOS PRIMER CURSO': 'PRIMER_CURSO',
        'PRIMER CURSO 2017': 'PRIMER_CURSO',
        'PRIMER CURSO 2018': 'PRIMER_CURSO',
        'PRIMER CURSO 2019': 'PRIMER_CURSO',
        'PRIMER CURSO': 'PRIMER_CURSO',
        'ANO': 'AÑO',
        'AO': 'AÑO'
    })
    return df



################# Compose Functions to transform the 1st course dataframes #################
  


def select_columns_of_interest(dataframes):
    """
    Selects the columns of interest from a list of DataFrames.
    
    Args:
        dataframes (list): List of DataFrames to process.
    
    Returns:
        list: List of DataFrames with the selected columns.
    """
    selected_columns_df = []
    for df in dataframes:

        df = add_gender_description(df)
        df = rename_columns(df)
        columns_of_interest = ['CODIGO_SNIES_DEL_PROGRAMA', 'AÑO', 'SEXO', 'PRIMER_CURSO', 'SEMESTRE']
        df = df[columns_of_interest]
        selected_columns_df.append(df)
    return selected_columns_df



# Function to join multiple DataFrames
def join_dataframes(dataframes):
    """
    Joins multiple DataFrames into a single DataFrame and displays the result in the console.
    
    Args:
        dataframes (list): List of DataFrames to join.
    
    Returns:
        pd.DataFrame: Joined DataFrame. If the input list is empty, returns an empty DataFrame.
    """
    # Reset index for each DataFrame to avoid duplicate indices
    dataframes = [df.reset_index(drop=True) for df in dataframes]
    joined_df = pd.concat(dataframes, ignore_index=True, sort=False, verify_integrity=False)
    print("Joined DataFrame:")
    print(joined_df.head())  # Display the first few rows of the joined DataFrame
    return joined_df


# Function to do format transformations in the 1st course dataframes
def transform_1st_course_join_df(df):
    """
    Applies a series of transformations to a list of DataFrames.
    """
    initial_row_count = df.shape[0]
    df = drop_empty_rows_by_threshold(df, 0.1)
    df = clean_special_characters(df)
    # Numeric columns
    columns = ['CODIGO_SNIES_DEL_PROGRAMA', 'AÑO', 'PRIMER_CURSO', 'SEMESTRE']
    
    for column in columns:
        if column in df.columns:
            
            df[column] = replace_nan_values(df[column])
            df = convert_columns_to_int(df, column)

    final_row_count = df.shape[0]
    # Calculate and display the total rows removed
    rows_removed = initial_row_count - final_row_count
    logging.info(f"Total rows removed: {rows_removed}")

    return df



############# compose functions to transform Programs #########################


def data_type_programs_df(df):

    num_columns = ['codigo_institucion_padre', 'registro_unico', 'codigo_snies_del_programa',
                    'numero_creditos', 'numero_periodos_de_duracion', 'costo_matricula_estud_nuevos']
    text_columns = ['nombre_institucion', 'sector', 'nombre_del_programa']
    cat_columns = ['estado_institucion', 'caracter_academico', 'estado_programa', 'reconocimiento_del_ministerio',
                    'cine_f_2013_ac_campo_amplio', 'cine_f_2013_ac_campo_especific', 'cine_f_2013_ac_campo_detallado',
                    'area_de_conocimiento', 'nucleo_basico_del_conocimiento', 'nivel_academico', 'nivel_de_formacion',
                    'modalidad', 'periodicidad', 'se_ofrece_por_ciclos_propedeut', 'periodicidad_admisiones',
                    'departamento_oferta_programa', 'municipio_oferta_programa']
    date_columns = ['fecha_de_registro_en_snies']

    # Adjust numeric columns
    for col in num_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(pd.Int64Dtype())

    # Adjust text columns
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Adjust categorical columns
    for col in cat_columns:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # Adjust date columns
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df



def create_date_columns(df):
    """
    Creates year and month columns based on the 'fecha_de_registro_en_snies' column in the DataFrame.
    Assumes that the 'fecha_de_registro_en_snies' column is of datetime type.

    Args:
        df (pd.DataFrame): DataFrame to modify.

    Returns:
        pd.DataFrame: DataFrame with the new year and month columns added.
    """
    date_column = 'fecha_de_registro_en_snies'
    year_column_name = 'año_creacion_snies'
    month_column_name = 'mes_creacion_snies'

    if date_column in df.columns:
        df[year_column_name] = df[date_column].dt.year
        df[month_column_name] = df[date_column].dt.month
    return df


def transform_programs_df(df):

    df = drop_unnecessary_columns_programs_df(df)
    df = data_type_programs_df(df)
    df = create_date_columns(df)

    columns_whith_empty = ['registro_unico','costo_matricula_estud_nuevos']
    for col in columns_whith_empty:
        if col in df.columns:
                    df[col] = replace_nan_values(df[col])

    # Dejar en la tabla solo programas activos
    df = df[df['estado_programa'] == 'Activo']
    df = df.dropna(subset=['reconocimiento_del_ministerio'])

    # Replace null values with "No clasificado" in the specified columns
    columns_to_update = ['cine_f_2013_ac_campo_especific', 
                     'cine_f_2013_ac_campo_detallado',
                     'periodicidad',
                     'periodicidad_admisiones',
                     'departamento_oferta_programa',
                     'municipio_oferta_programa']

    # Add "No clasificado" to the categories of each column if it is of type 'category'
    for column in columns_to_update:
        if column in df.columns and df[column].dtype.name == 'category':
            df[column] = df[column].cat.add_categories("No clasificado")

    # Replace null values with "No clasificado"
    df[columns_to_update] = df[columns_to_update].fillna("No clasificado")
    if 'MODALIDAD' in df.columns:
        df['MODALIDAD'] = df['MODALIDAD'].replace({
            'Presencial-Virtual': 'Híbrida (Presencial-Virtual)',
            'Dual': 'Presencial-Dual',
            'A distancia': 'Presencial-A distancia'
        })


    return df


def create_ies_table(df_programs):
    """
    Creates a new table (DataFrame) for IES (Instituciones de Educación Superior) 
    by separating specific columns from the programs DataFrame.

    Args:
        df_programs (pd.DataFrame): Original programs DataFrame.

    Returns:
        pd.DataFrame: New DataFrame containing IES information.
    """
    # lista de columnas a separar en una nueva tabla
    tosepare_columns = ['codigo_institucion_padre', 'nombre_institucion', 
                        'estado_institucion', 'caracter_academico', 'sector']

    # Seleccionar las columnas requeridas y eliminar duplicados
    dim_ies_df = df_programs[tosepare_columns].drop_duplicates()

    # Ordenar por nombre de institución
    dim_ies_df = dim_ies_df.sort_values(by='nombre_institucion')

    # Reiniciar el índice después de ordenar
    # Resetting the index ensures a clean, sequential index after sorting, which is useful if the index is used for iteration or display purposes.
    dim_ies_df = dim_ies_df.reset_index(drop=True)
    
    return dim_ies_df


def extract_programs_table(df_programs):
    """
    Extracts the programs table by removing columns that were separated into the IES table,
    keeping only the primary key of IES in the programs DataFrame.

    Args:
        df_programs (pd.DataFrame): Original programs DataFrame.

    Returns:
        pd.DataFrame: Programs DataFrame with unnecessary columns removed.
    """
    # Drop the columns that were separated into the IES table, except the primary key
    dim_programs = df_programs.drop(columns=['nombre_institucion', 'estado_institucion', 'caracter_academico', 'sector'], inplace=False)

    return dim_programs
