#!/usr/bin/env python3
"""
Remove duplicate records based on phone numbers from muhasib_accountants.csv
Keep only the first occurrence of each phone number
"""

import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_phone_duplicates():
    """Remove duplicate records based on phone numbers"""
    
    # Read the CSV file
    logger.info("Reading CSV file...")
    df = pd.read_csv('muhasib_accountants.csv')
    
    original_count = len(df)
    logger.info(f"Original record count: {original_count}")
    
    # Show duplicate phone numbers before removal
    logger.info("Finding records with duplicate phone numbers...")
    df_with_phone = df[df['phone'].notna() & (df['phone'] != '')]
    duplicate_phones = df_with_phone[df_with_phone.duplicated(subset=['phone'], keep=False)]
    
    if not duplicate_phones.empty:
        logger.info(f"Found {len(duplicate_phones)} records with duplicate phone numbers:")
        # Group by phone to show which records will be kept/removed
        for phone, group in duplicate_phones.groupby('phone'):
            logger.info(f"\nPhone: {phone}")
            for idx, row in group.iterrows():
                status = "KEEP" if idx == group.index[0] else "REMOVE"
                logger.info(f"  {status}: ID={row['id']}, Name={row['name']}")
    
    # Remove duplicates based on phone number (keep first occurrence)
    logger.info("Removing duplicate phone numbers (keeping first occurrence)...")
    df_cleaned = df.drop_duplicates(subset=['phone'], keep='first')
    
    cleaned_count = len(df_cleaned)
    removed_count = original_count - cleaned_count
    
    logger.info(f"Cleaned record count: {cleaned_count}")
    logger.info(f"Removed {removed_count} duplicate phone records")
    
    if removed_count > 0:
        # Save cleaned data
        df_cleaned.to_csv('muhasib_accountants_no_phone_duplicates.csv', index=False)
        logger.info("Cleaned data saved to muhasib_accountants_no_phone_duplicates.csv")
        
        # Show what was removed
        logger.info("Summary of removed records:")
        removed_df = df[~df.index.isin(df_cleaned.index)]
        for idx, row in removed_df.iterrows():
            logger.info(f"Removed: ID={row['id']}, Name={row['name']}, Phone={row['phone']}")
    else:
        logger.info("No phone duplicates found. Original file is clean.")
    
    # Generate final statistics
    logger.info("\nFinal statistics:")
    logger.info(f"Total unique accountants: {cleaned_count}")
    logger.info(f"Unique phone numbers: {df_cleaned['phone'].nunique()}")
    logger.info(f"Records with phone numbers: {df_cleaned['phone'].notna().sum()}")

if __name__ == "__main__":
    remove_phone_duplicates()