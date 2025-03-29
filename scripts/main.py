# libreries
import sys
import os
import pandas as pd
import numpy as np
import sqlalchemy as sa

# Add the "data" folder to the module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'data', 'scripts'))

# Import the libreries and needed modules
from etl_config import DATABASE_CREDENTIALS, DATA_SOURCES, ETL_TASKS, KEYWORDS_1STCOURSE, LOGGING_CONFIG
from extract import extract_dataframes_from_excel,extract_csv_to_dataframe,read_dataframe_from_excel
from load import connect_to_db, create_new_database, load_dataframes_to_db, load_dataframe_to_db, read_tables_from_db,load_combined_1st_course_to_db, load_enrollment_df_to_db
from transform import transform_1st_course_join_df, select_columns_of_interest, join_dataframes, transform_programs_df, create_ies_table,extract_programs_table

######################## ETL FLOW ########################

def main():

    ######### Extract  
    folder_path1 = DATA_SOURCES["FIRST_COURSE"]                          # Specify the path to the Excel folder
    Fst_course_files_dict = extract_dataframes_from_excel(folder_path1)  # Call the extraction function
    engine = connect_to_db(DATABASE_CREDENTIALS)                         # Connect to the database
    create_new_database(DATABASE_CREDENTIALS, 'ETL_Project')             # Create the database
    db_tables = load_dataframes_to_db(Fst_course_files_dict, engine)     # Load the tables into the database
    
    folder_path2 = DATA_SOURCES["ENROLLMENT"]                            # Specify the path to the CSV file
    enrollment_df = extract_csv_to_dataframe(folder_path2)               # Extract the data from the CSV file
    
    folder_path3 = DATA_SOURCES["PROGRAMS"]                              # Specify the path to the programs Excel file
    programs_df = read_dataframe_from_excel(folder_path3)
    load_dataframe_to_db(programs_df,"original_programs",engine)
    
    ######### Transform
    Fst_course_df_to_transform = read_tables_from_db(db_tables, engine)  # Read the tables from the database
    filtered_df = select_columns_of_interest(Fst_course_df_to_transform) # Select the columns of interest
    joindf = join_dataframes(filtered_df)                                # Join the data frames into a single data frame
    trasnformed_1s_course_df = transform_1st_course_join_df(joindf)      # Apply the transformations to the data frames
    
    transformed_programs = transform_programs_df(programs_df)           # Transform the programs data frame
    dim_ies_table = create_ies_table(transformed_programs)              # Create the IES table
    dim_programs = extract_programs_table(transformed_programs)         # Create the programs table
    
    ######### Load
    load_combined_1st_course_to_db(trasnformed_1s_course_df, engine)    # Load the transformed data frame into the database
    load_enrollment_df_to_db(enrollment_df, "Enrollment", engine)       # Load the data into the database
    load_dataframe_to_db(dim_programs,"dim_programs",engine)            # Load the programs data frame into the database
    load_dataframe_to_db(dim_ies_table,"dim_ies",engine)                # Load the IES table into the database   

if __name__ == "__main__":
    main()