import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

# Load processed features
x = pd.read_csv('../data/processed/x_processed.csv')
y = pd.read_csv('../data/processed/y_labels.csv').values.ravel() # flatens multidmensional array 

# # splitting
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

# train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train,y_train)

# predict and evaluate
y_pred = model.predict(x_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# The error occurs because your target variable (y_test) contains more than two classes, but precision_score and recall_score default to average='binary'
f1 = f1_score(y_test, y_pred, average='macro')
prec = precision_score(y_test, y_pred, average='macro')
rec = recall_score(y_test, y_pred, average='macro')


# top 3 Feature Importances 
feature_importances = pd.Series(model.feature_importances_, index=x.columns)
top_features = feature_importances.sort_values(ascending=False).head(3)

# save model
with open('../model/churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# save results
with open('../model/model_metrics.txt', 'w') as f:
    f.write(f"Model: Random Forest\n")
    f.write(f"Accuracy: {acc:.4f}\n")
    f.write(f"Precision: {prec:.4f}\n")
    f.write(f"Recall: {rec:.4f}\n")
    f.write(f"F1 score: {f1:.4f}\n")
    f.write("Confusion Matrix:\n")
    f.write(str(cm) + "\n")
    f.write("Top 3 Important Features:\n")
    f.write(top_features.to_string())

print("Model training and evaluation on test set complete.")