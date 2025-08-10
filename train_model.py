# train_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///inventory.db"
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        # Use pandas to read the entire 'sales' table into a DataFrame
        df = pd.read_sql_table('sales', connection)
    print("✅ Sales data loaded successfully from database.")
except Exception as e:
    print(f"❌ Error loading data from database: {e}")
    print("Please run database_setup.py first to create and populate the database.")
    exit()



df['date'] = pd.to_datetime(df['date'])
df['day_of_year'] = df['date'].dt.dayofyear


models = {}
product_ids = df['product_id'].unique()

print(f"Found {len(product_ids)} unique products. Training a model for each...")

for product_id in product_ids:
    product_df = df[df['product_id'] == product_id]
    X = product_df[['day_of_year']]
    y = product_df['quantity_sold']

    # --- 4. Train the Model ---
    # This part remains the same
    model = LinearRegression()
    model.fit(X, y)
    models[product_id] = model
    print(f"  - Model for product_id {product_id} trained.")



model_filename = 'prediction_models.pkl'
joblib.dump(models, model_filename)

print(f"\n✅ All models trained and saved to '{model_filename}' successfully.")
