import pandas as pd

# Load dataset
df = pd.read_csv('../data/raw/exl_credit_card_churn_data.csv')
print("Initial shape:", df.shape)

# Handle Missing Values

# Check nulls
null_counts = df.isnull().sum()
print("Missing values per column:\n", null_counts)

# Drop rows with missing target
df = df.dropna(subset=['Churn']) # empty
df = df[pd.to_numeric(df['Churn'], errors='coerce').notna()] # not numbrt
df['HasCrCard'] = df['HasCrCard'].astype(str).map({
    '0.0': 0.0, 
    '0': 0.0, 
    'No': 0.0,
    'Yes': 1.0,
    '1.0': 1.0,
    '1': 1.0
})

df['IsActiveMember'] = df['IsActiveMember'].astype(str).map({
    '0.0': 0.0, 
    '0': 0.0, 
    'No': 0.0,
    'Yes': 1.0,
    '1.0': 1.0,
    '1': 1.0
})

# Fill nulls
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].median())

# Handle Outliers

def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return data[(data[column] >= lower) & (data[column] <= upper)]

numerical_cols = ['Age', 'Balance', 'EstimatedSalary']

for col in numerical_cols:
    original = df.shape[0]
    df = remove_outliers_iqr(df, col)
    removed = original - df.shape[0]
    print(f"Removed {removed} outliers from {col}")

print("Final shape after cleaning:", df.shape)

# Save Cleaned Data 
df.to_csv('../data/processed/churn_cleaned.csv', index=False)
print(f"Cleaned data saved")
