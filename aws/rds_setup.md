# Aurora MySQL RDS Setup Guide

1. Launch RDS instance:
   - Engine: Amazon Aurora (MySQL Compatible)
   - DB Name: `exl_churn_db`
   - Table: `customers`

2. Inbound Rule:
   - Allow EC2 security group access to port 3306 (MySQL)

3. Create Table:
   Use the `data_loader.py` script to populate `customers` table.

4. Create new table for predictions:
   `churn_predictions` (CustomerID, Churn_Prediction)
