# Project: Higher education indicators
The project aims to conduct a data analysis to compare figures and historical trends of first-semester enrollments and total enrollment in academic programs at the national level. The National Ministry of Education publishes annual figures, providing consolidated values.
## Required Libraries
- Python 3.x
- pandas
- Jupyter
- SQLAlchemy
- PyYAML
- psycopg2
- Unidecode
- Openpyxl
- os
- re
- unicodedata
- matplotlib
- mplfinance

## Instructions
After creating the virtual environment, please install the libraries in the terminal ussing `pip` 
```bash
pip install pandas jupyter sqlalchemy pyyaml psycopg2 unidecode
```
It is not necessary to install `os` and `re` because they are modules that come with Python.

In the "initial scripts" folder, the initial versions of the scripts developed prior to the automation process were stored. Meanwhile, the "scripts" folder contains the finalized files used for automating the ETL process. This organization ensures a clear distinction between prototype development and the fully automated pipeline
