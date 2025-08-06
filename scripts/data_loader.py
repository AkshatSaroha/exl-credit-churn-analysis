import pandas as pd  
import mysql.connector

df = pd.read_csv('../data/processed/churn_cleaned.csv')
# print('CSV Data Preview:\n', df.head())

# MySQL DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '16122003',
    'database': 'exl'
}

# connecting to db
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS customers (
    CustomerID VARCHAR(20),
    Gender VARCHAR(10),
    Age FLOAT,
    Tenure FLOAT,
    Balance FLOAT,
    NumOfProducts FLOAT,
    HasCrCard FLOAT,
    IsActiveMember FLOAT,
    EstimatedSalary FLOAT,
    Churn FLOAT
)
"""

cursor.execute(create_table_query)
conn.commit()

# Upload data row by row
for _, row in df.iterrows():
    insert_query = """
    INSERT INTO customers (CustomerID, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Churn)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("Data uploaded successfully!")

# Validate upload
cursor.execute("SELECT COUNT(*) FROM customers")
count = cursor.fetchone()[0]
print("Total records in DB:", count)

cursor.close()
conn.close()


# --------------------------- to upload on aws --------------------------------------

# import pandas as pd  
# import mysql.connector

# # MySQL DB config
# db_config = {
#     'host': '',
#     'user': '',
#     'password': '',
#     'database': ''
# }

# # connecting to db
# conn = mysql.connector.connect(**db_config)
# cursor = conn.cursor()

# create_table_query = """
# CREATE TABLE IF NOT EXISTS customers (
#     CustomerID VARCHAR(20),
#     Gender VARCHAR(10),
#     Age FLOAT,
#     Tenure FLOAT,
#     Balance FLOAT,
#     NumOfProducts FLOAT,
#     HasCrCard FLOAT,
#     IsActiveMember FLOAT,
#     EstimatedSalary FLOAT,
#     Churn FLOAT
# )
# """

# cursor.execute(create_table_query)
# conn.commit()

# # Data to insert
# customer_data = [
#     ('CUST0001', 'Male', 45, 3, 120000.5, 2, 1, 1, 50000, 0),
#     ('CUST0002', 'Female', 33, 1, 34000.0, 1, 0, 1, 62000, 1),
#     ('CUST0003', 'Male', 52, 6, 58000.0, 3, 1, 0, 85000, 0),
#     ('CUST0004', 'Female', 40, 4, 0.0, 1, 1, 0, 42000, 1),
#     ('CUST0005', 'Male', 28, 2, 99000.0, 2, 0, 1, 37000, 1),
#     ('CUST0006', 'Female', 35, 5, 40000.75, 2, 1, 1, 90000, 0),
#     ('CUST0007', 'Male', 60, 7, 150000.0, 4, 1, 0, 76000, 0),
#     ('CUST0008', 'Female', 48, 3, 85000.0, 3, 0, 0, 66000, 1),
#     ('CUST0009', 'Male', 39, 2, 22000.2, 1, 1, 1, 58000, 0),
#     ('CUST0010', 'Female', 50, 4, 76000.9, 2, 1, 1, 47000, 1)
# ]

# # Insert query
# insert_query = """
#     INSERT INTO customers (CustomerID, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Churn)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """

# # Insert rows one by one
# for row in customer_data:
#     cursor.execute(insert_query, row)

# conn.commit()
# cursor.close()
# conn.close()

# print("Data inserted successfully!")