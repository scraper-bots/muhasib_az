#!/usr/bin/env python3
"""
Remove duplicate records from muhasib_accountants.csv
"""

import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_duplicates():
    """Remove duplicate records from the CSV file"""
    
    # Read the CSV file
    logger.info("Reading CSV file...")
    df = pd.read_csv('muhasib_accountants.csv')
    
    original_count = len(df)
    logger.info(f"Original record count: {original_count}")
    
    # Check for duplicates based on ID
    logger.info("Checking for duplicate IDs...")
    duplicate_ids = df[df.duplicated(subset=['id'], keep=False)]
    if not duplicate_ids.empty:
        logger.info(f"Found {len(duplicate_ids)} records with duplicate IDs:")
        print(duplicate_ids[['id', 'name', 'phone']].to_string())
    
    # Remove duplicates based on ID (keep first occurrence)
    df_cleaned = df.drop_duplicates(subset=['id'], keep='first')
    
    # Check for duplicates based on phone number (excluding empty phones)
    logger.info("Checking for duplicate phone numbers...")
    df_with_phone = df_cleaned[df_cleaned['phone'].notna() & (df_cleaned['phone'] != '')]
    duplicate_phones = df_with_phone[df_with_phone.duplicated(subset=['phone'], keep=False)]
    if not duplicate_phones.empty:
        logger.info(f"Found {len(duplicate_phones)} records with duplicate phone numbers:")
        print(duplicate_phones[['id', 'name', 'phone']].to_string())
    
    # Check for duplicates based on email (excluding empty emails)
    logger.info("Checking for duplicate emails...")
    df_with_email = df_cleaned[df_cleaned['email'].notna() & (df_cleaned['email'] != '')]
    duplicate_emails = df_with_email[df_with_email.duplicated(subset=['email'], keep=False)]
    if not duplicate_emails.empty:
        logger.info(f"Found {len(duplicate_emails)} records with duplicate emails:")
        print(duplicate_emails[['id', 'name', 'email']].to_string())
    
    # Check for potential duplicates based on name similarity
    logger.info("Checking for duplicate names...")
    duplicate_names = df_cleaned[df_cleaned.duplicated(subset=['name'], keep=False)]
    if not duplicate_names.empty:
        logger.info(f"Found {len(duplicate_names)} records with duplicate names:")
        print(duplicate_names[['id', 'name', 'phone', 'email']].to_string())
    
    cleaned_count = len(df_cleaned)
    removed_count = original_count - cleaned_count
    
    logger.info(f"Cleaned record count: {cleaned_count}")
    logger.info(f"Removed {removed_count} duplicate records")
    
    if removed_count > 0:
        # Save cleaned data
        df_cleaned.to_csv('muhasib_accountants_cleaned.csv', index=False)
        logger.info("Cleaned data saved to muhasib_accountants_cleaned.csv")
    else:
        logger.info("No duplicates found. Original file is clean.")
    
    # Generate summary statistics
    logger.info("Summary statistics:")
    logger.info(f"Total unique accountants: {cleaned_count}")
    logger.info(f"Records with phone numbers: {df_cleaned['phone'].notna().sum()}")
    logger.info(f"Records with email addresses: {df_cleaned['email'].notna().sum()}")
    logger.info(f"Records from Bakı: {df_cleaned['city'].str.contains('Bak', case=False, na=False).sum()}")
    
    # Show city distribution
    city_counts = df_cleaned['city'].value_counts().head(10)
    logger.info("Top 10 cities:")
    print(city_counts.to_string())

if __name__ == "__main__":
    remove_duplicates()