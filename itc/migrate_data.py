import pandas as pd
from sqlalchemy import create_engine

# Load the Excel data
file_path = 'sample_data.xlsx'
data = pd.read_excel(file_path, sheet_name='Responses')

# Clean column names for SQL compatibility
data.columns = [
    's_no', 'submitted_time', 'tl', 'ds', 'outlet_name', 'soh', 'number_of_packets'
]

# PostgreSQL connection details
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'
DB_HOST = 'localhost'
DB_PORT = '5454'
DB_NAME = 'mydatabase'

# Create a PostgreSQL connection string
connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# Insert data into the table
data.to_sql('tracker_responses', engine, if_exists='append', index=False)

print("Data has been successfully inserted into the PostgreSQL table.")
