import pandas as pd
import mysql.connector
import pickle

# DB Config 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '16122003',
    'database': 'exl'
}

# Fetch test data
conn = mysql.connector.connect(**db_config)
query = "SELECT * FROM customers"
df = pd.read_sql(query, conn)
original_ids = df['CustomerID'].values

# Preprocessing 
x = df.drop(['CustomerID', 'Churn'], axis=1)

# Split by type
categorical_cols = x.select_dtypes(include='object').columns.tolist()
numerical_cols = x.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Load encoder and scaler from training
with open('../model/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
with open('../model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


# Transform using loaded encoder and scaler
X_cat = pd.DataFrame(encoder.transform(x[categorical_cols]), columns=encoder.get_feature_names_out(categorical_cols))
X_num = pd.DataFrame(scaler.transform(x[numerical_cols]), columns=numerical_cols)

X_processed = pd.concat([X_num, X_cat], axis=1)

# Predict 
with open('../model/churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

predictions = model.predict(X_processed)

# Create table if not exists 
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS churn_predictions (
        CustomerID VARCHAR(20),
        Churn_Prediction INT
    )
""")
conn.commit()

# insert into prediction
for cid, pred in zip(original_ids, predictions):
    cursor.execute("REPLACE INTO churn_predictions (CustomerID, Churn_Prediction) VALUES (%s, %s)", (cid, int(pred)))

conn.commit()
cursor.close()
conn.close()

print("Predictions stored successfully in churn_predictions table.")