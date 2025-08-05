import pandas as pd

# Load dataset
df = pd.read_csv('../data/raw/exl_credit_card_churn_data.csv')
print("Initial shape:", df.shape)

# Check nulls
null_counts = df.isnull().sum()
print("Missing values per column:\n", null_counts)

# Drop rows with missing target
df = df.dropna(subset=['Churn'])

# Fill or drop based on column type
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])  # Fill with mode
    else:
        df[col] = df[col].fillna(df[col].median())   # Fill with median

print("Shape after handling nulls:", df.shape)


# Define outlier limits using IQR method
def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return data[(data[column] >= lower) & (data[column] <= upper)]

# Apply outlier removal to selected numerical columns
numerical_cols = ['Age', 'Balance', 'EstimatedSalary']

for col in numerical_cols:
    original_shape = df.shape[0]
    df = remove_outliers_iqr(df, col)
    print(f"Removed {original_shape - df.shape[0]} outliers from {col}")

print("Final shape after outlier removal:", df.shape)

# Save cleaned data
df.to_csv('../data/processed/churn_cleaned.csv', index=False)
print(f"Cleaned data saved")
