import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load local data
df = pd.read_csv('../data/processed/churn_cleaned.csv')

# Churn distribution
sns.countplot(data=df, x='Churn')
plt.title("Churn Count")
plt.savefig("../data/processed/churn_count.png")
plt.clf()

# Age distribution
sns.histplot(df['Age'], kde=True)
plt.title("Age Distribution")
plt.savefig("../data/processed/age_distribution.png")
plt.clf()

# Tenure distribution
sns.histplot(df['Tenure'], bins=10)
plt.title("Tenure Distribution")
plt.savefig("../data/processed/tenure_distribution.png")
plt.clf()

# Card type analysis (NumOfProducts)
sns.countplot(data=df, x='NumOfProducts', hue='Churn')
plt.title("Product Count vs Churn")
plt.savefig("../data/processed/product_churn.png")
plt.clf()

# Correlation matrix
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.savefig("../data/processed/correlation_matrix.png")
plt.clf()

print("EDA visualizations saved in /data/processed/")
