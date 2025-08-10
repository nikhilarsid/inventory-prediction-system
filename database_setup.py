# database_setup.py

import pandas as pd
from sqlalchemy import create_engine, text

# --- 1. Define Database Configuration ---
# This will create a file named 'inventory.db' in our project folder.
DATABASE_URL = "sqlite:///inventory.db"
# The 'engine' is the entry point to our database.
engine = create_engine(DATABASE_URL)

print("Setting up the database...")

# --- 2. Load Initial Data from CSV ---
try:
    df = pd.read_csv('data/sales_data.csv')
    print("✅ sales_data.csv loaded successfully.")
except FileNotFoundError:
    print("❌ Error: sales_data.csv not found. Cannot initialize database.")
    exit()

# --- 3. Store Data in the Database ---
# We'll name our table 'sales'.
# 'if_exists='replace'' means if the table already exists, it will be dropped and recreated.
# This is useful for re-running the script, but be careful in a real production environment!
# 'index=False' means we won't write the pandas DataFrame index as a column in the table.
try:
    with engine.connect() as connection:
        df.to_sql('sales', con=connection, if_exists='replace', index=False)
        
        # Verify that the data was inserted
        result = connection.execute(text("SELECT COUNT(*) FROM sales"))
        count = result.scalar()
        print(f"✅ Database 'inventory.db' created and table 'sales' populated with {count} records.")

except Exception as e:
    print(f"❌ An error occurred during database setup: {e}")