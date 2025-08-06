import pandas as pd  
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import pickle

# load data
df = pd.read_csv('../data/processed/churn_cleaned.csv')

# separate labels and target
x = df.drop(['CustomerID', 'Churn'], axis=1)
y = df['Churn']


# Identify categorical & numerical columns
categorical_cols = x.select_dtypes(include='object').columns.tolist()
numerical_cols = x.select_dtypes(include=['int64', 'float64']).columns.tolist()

print('Category : ',categorical_cols)
print('\nNumber cols: ', numerical_cols)

# one hot encoding
encoder = OneHotEncoder(drop='first', sparse_output=False)  # Set sparse=False for dense output
x_cat = pd.DataFrame(
    encoder.fit_transform(x[categorical_cols]),
    columns=encoder.get_feature_names_out(categorical_cols),
    index=x.index  # Ensure index alignment
)

# min max scaler
scaler = MinMaxScaler()
x_num = pd.DataFrame(
    scaler.fit_transform(x[numerical_cols]),
    columns=numerical_cols,
    index=x.index 
)

with open('../model/encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)
with open('../model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# final feature set
x_processed = pd.concat([x_num, x_cat], axis = 1)

# save for model training
x_processed.to_csv('../data/processed/x_processed.csv', index = False)
y.to_csv('../data/processed/y_labels.csv', index=False)

print('Feature engg complete.')
