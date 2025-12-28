import pandas as pd
import numpy as np
import re

# Load the dataset
df = pd.read_csv('accountants.csv')

print("="*60)
print("DATASET OVERVIEW")
print("="*60)
print(f"Total Records: {len(df)}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")

print("\n" + "="*60)
print("BASIC STATISTICS")
print("="*60)

# Clean min_salary column - extract numeric value from string like "(AZN): 350"
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan
    # Extract numbers from strings like "(AZN): 350" or "350"
    match = re.search(r'(\d+)', str(salary_str))
    if match:
        return int(match.group(1))
    return 0

df['salary_clean'] = df['min_salary'].apply(extract_salary)

print("\nSalary Statistics:")
print(f"Min Salary Range: {df['salary_clean'].min()} - {df['salary_clean'].max()} AZN")
print(f"Average Min Salary: {df['salary_clean'].mean():.2f} AZN")
print(f"Median Min Salary: {df['salary_clean'].median():.2f} AZN")

print("\nAge Statistics:")
print(f"Age Range: {df['age'].min()} - {df['age'].max()} years")
print(f"Average Age: {df['age'].mean():.2f} years")

print("\n" + "="*60)
print("DISTRIBUTION ANALYSIS")
print("="*60)

print("\nGender Distribution:")
print(df['gender'].value_counts())

print("\nMarital Status Distribution:")
print(df['marital_status'].value_counts())

print("\nTop 10 Cities:")
print(df['city'].value_counts().head(10))

print("\nTop 10 Categories:")
print(df['category'].value_counts().head(10))

print("\nTop 10 Positions:")
print(df['position'].value_counts().head(10))

print("\n" + "="*60)
print("NULL/MISSING VALUES")
print("="*60)
print(df.isnull().sum())
