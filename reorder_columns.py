#!/usr/bin/env python3
"""
Reorder CSV columns to put phone number first
"""

import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reorder_columns():
    """Reorder CSV columns to put phone number first"""
    
    # Read the cleaned CSV file
    logger.info("Reading cleaned CSV file...")
    df = pd.read_csv('muhasib_accountants_no_phone_duplicates.csv')
    
    logger.info(f"Current columns: {list(df.columns)}")
    
    # Define new column order with phone first
    new_column_order = [
        'phone',
        'id', 
        'name',
        'city',
        'email',
        'age',
        'gender',
        'marital_status',
        'category',
        'position',
        'min_salary',
        'education',
        'experience',
        'skills',
        'url'
    ]
    
    # Reorder columns
    df_reordered = df[new_column_order]
    
    # Save reordered data
    df_reordered.to_csv('muhasib_accountants_phone_first.csv', index=False)
    logger.info("Reordered data saved to muhasib_accountants_phone_first.csv")
    logger.info(f"New column order: {list(df_reordered.columns)}")
    
    # Show first few rows
    logger.info("First 3 rows of reordered data:")
    print(df_reordered.head(3).to_string())

if __name__ == "__main__":
    reorder_columns()