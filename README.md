# Project: Higher education indicator
The project aims to conduct a data analysis to compare figures and historical trends of first-semester enrollments and total enrollment in academic programs at the national level. The National Ministry of Education publishes annual figures, providing consolidated values.

# Problem Description
Higher education enrollment trends are crucial for understanding the evolution of academic programs and making informed decisions. However, raw data provided by the Ministerio Nacional de Educación is not readily structured for direct analysis. The figures on first-semester enrollments and total enrollment are published annually, but they require extraction, transformation, and consolidation to enable meaningful comparisons over time. Without proper processing, identifying trends, anomalies, or insights becomes challenging for policymakers and educational institutions.

The project addresses these challenges by creating a structured dataset that facilitates historical comparisons of enrollment patterns. By processing and organizing the data, it becomes possible to analyze variations in student enrollment across different years and programs. This analysis can provide valuable insights into the effectiveness of enrollments strategies, shifts in student preferences, and potential areas requiring intervention to improve access to higher education.

## Context
Higher education institutions in Colombia periodically submit enrollment and student retention indicators to the Ministerio Nacional de Educación. This information is publicly accessible; however, only very general figures are available at the national and departmental levels. The Ministry of Education also requires academic programs to conduct comparative analyses on the evolution of indicators such as the number of applicants, admitted students, first-year enrollees, and total student enrollment. This is to demonstrate that the academic program will have demand and meets educational needs. However, although the information is publicly available, historical records do not have a standardized format, and the large volume of data makes processing and analysis difficult.

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
## Instructions
After creating the virtual environment, please install the libraries in the terminal ussing `pip` 
```bash
pip install pandas jupyter sqlalchemy pyyaml psycopg2 unidecode
```
It is not necessary to install `os` and `re` because they are modules that come with Python.
