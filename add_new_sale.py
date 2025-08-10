# add_new_sale.py

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import random


DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL)

def add_sale():
    
   
    product_id = random.choice([101, 102, 103])
    
   
    quantity_sold = random.randint(10, 70) 
    
    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  
    new_sale_df = pd.DataFrame([{
        'date': sale_date,
        'product_id': product_id,
        'quantity_sold': quantity_sold
    }])


    try:
        with engine.connect() as connection:
            
            new_sale_df.to_sql('sales', con=connection, if_exists='append', index=False)
        
        print(f"✅ Successfully added new sale: Product {product_id}, Quantity {quantity_sold} at {sale_date}")

    except Exception as e:
        print(f"❌ An error occurred while adding the sale: {e}")

if __name__ == "__main__":
    add_sale()
