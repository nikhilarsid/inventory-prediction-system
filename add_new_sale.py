# add_new_sale.py

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import random

# --- 1. Database Configuration ---
DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL)

def add_sale():
    """
    Adds a single, new, random sales record to the database.
    """
    # --- 2. Generate Sample Data ---
    # Choose a random product ID from our existing products
    product_id = random.choice([101, 102, 103])
    
    # Generate a random quantity sold
    quantity_sold = random.randint(10, 70) 
    
    # Use the current date and time for the sale
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- 3. Create a DataFrame ---
    # We create a pandas DataFrame because it's the easiest way
    # to append data to a SQL table using to_sql.
    new_sale_df = pd.DataFrame([{
        'date': sale_date,
        'product_id': product_id,
        'quantity_sold': quantity_sold
    }])

    # --- 4. Append to Database ---
    try:
        with engine.connect() as connection:
            # Use to_sql with if_exists='append' to add the new row
            new_sale_df.to_sql('sales', con=connection, if_exists='append', index=False)
        
        print(f"✅ Successfully added new sale: Product {product_id}, Quantity {quantity_sold} at {sale_date}")

    except Exception as e:
        print(f"❌ An error occurred while adding the sale: {e}")

if __name__ == "__main__":
    add_sale()