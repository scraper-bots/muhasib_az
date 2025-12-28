import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from pathlib import Path

# Set style for professional business charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']

# Load and clean data
df = pd.read_csv('accountants.csv')

# Clean salary column
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan
    match = re.search(r'(\d+)', str(salary_str))
    if match:
        return int(match.group(1))
    return 0

df['salary'] = df['min_salary'].apply(extract_salary)

# Clean age data (remove outliers)
df_clean = df[(df['age'] >= 18) & (df['age'] <= 70)].copy()

# Extract position type from position column
def extract_position_type(position_str):
    if pd.isna(position_str):
        return 'Other'
    position_lower = str(position_str).lower()
    if 'baş mühasib' in position_lower or 'bas muhasib' in position_lower:
        return 'Chief Accountant'
    elif 'köməkçi' in position_lower or 'köməkçisi' in position_lower or 'komekci' in position_lower:
        return 'Assistant Accountant'
    elif 'mühasib' in position_lower or 'muhasib' in position_lower:
        return 'Accountant'
    elif '1c' in position_lower:
        return '1C Operator'
    elif 'iqtisadçi' in position_lower or 'iqtisadci' in position_lower:
        return 'Economist'
    elif 'maliyyə' in position_lower:
        return 'Finance'
    else:
        return 'Other'

df_clean['position_type'] = df_clean['position'].apply(extract_position_type)

# Standardize city names
def standardize_city(city_str):
    if pd.isna(city_str):
        return 'Unknown'
    city_lower = str(city_str).lower().strip()
    if 'bak' in city_lower:  # Bakı, Baki, Baku
        return 'Baku'
    elif 'gəncə' in city_lower or 'gence' in city_lower:
        return 'Ganja'
    elif 'sumq' in city_lower:
        return 'Sumqayit'
    else:
        return city_str.strip()

df_clean['city_clean'] = df_clean['city'].apply(standardize_city)

# Create charts directory
Path('charts').mkdir(exist_ok=True)

print("Generating business insights charts...")

# ============================================================================
# CHART 1: Talent Pool Distribution by Gender
# ============================================================================
plt.figure(figsize=(10, 6))
gender_counts = df_clean[df_clean['gender'].isin(['Kişi', 'Qadın'])]['gender'].value_counts()
gender_labels = ['Male', 'Female']
bars = plt.bar(gender_labels, [gender_counts.get('Kişi', 0), gender_counts.get('Qadın', 0)],
               color=[colors[0], colors[1]], edgecolor='black', linewidth=1.2)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}\n({int(height/sum(gender_counts)*100)}%)',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Talent Pool Distribution by Gender', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.xlabel('Gender', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/01_gender_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 2: Geographic Concentration - Top 10 Cities
# ============================================================================
plt.figure(figsize=(12, 7))
top_cities = df_clean['city_clean'].value_counts().head(10)
bars = plt.barh(range(len(top_cities)), top_cities.values, color=colors[0], edgecolor='black', linewidth=1.2)
plt.yticks(range(len(top_cities)), top_cities.index, fontsize=11)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_cities.values)):
    plt.text(value + 5, i, f'{value} ({value/len(df_clean)*100:.1f}%)',
             va='center', fontsize=10, fontweight='bold')

plt.title('Geographic Distribution of Accounting Talent', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.ylabel('City', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_geographic_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 3: Salary Distribution Analysis
# ============================================================================
plt.figure(figsize=(14, 7))
salary_filtered = df_clean[df_clean['salary'] > 0]['salary']

# Create salary bins
bins = [0, 300, 500, 700, 1000, 1500, 2000, 3600]
labels = ['<300', '300-500', '500-700', '700-1000', '1000-1500', '1500-2000', '2000+']
salary_binned = pd.cut(salary_filtered, bins=bins, labels=labels, include_lowest=True)
salary_counts = salary_binned.value_counts().sort_index()

bars = plt.bar(range(len(salary_counts)), salary_counts.values,
               color=colors[2], edgecolor='black', linewidth=1.2)
plt.xticks(range(len(salary_counts)), salary_counts.index, rotation=0)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}\n({int(height/len(salary_filtered)*100)}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title('Salary Expectations Distribution (AZN Monthly)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Salary Range (AZN)', fontsize=12, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.axhline(y=salary_counts.mean(), color='red', linestyle='--', linewidth=2, label=f'Average: {salary_counts.mean():.0f} candidates')
plt.legend()
plt.tight_layout()
plt.savefig('charts/03_salary_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 4: Age Distribution of Talent Pool
# ============================================================================
plt.figure(figsize=(14, 7))
age_bins = [18, 25, 30, 35, 40, 45, 50, 55, 70]
age_labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55+']
age_binned = pd.cut(df_clean['age'], bins=age_bins, labels=age_labels, include_lowest=True)
age_counts = age_binned.value_counts().sort_index()

bars = plt.bar(range(len(age_counts)), age_counts.values,
               color=colors[3], edgecolor='black', linewidth=1.2)
plt.xticks(range(len(age_counts)), age_counts.index, rotation=45)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title('Age Distribution of Accounting Professionals', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age Range', fontsize=12, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/04_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 5: Salary Expectations by Position Type
# ============================================================================
plt.figure(figsize=(14, 7))
position_salary = df_clean[df_clean['salary'] > 0].groupby('position_type')['salary'].agg(['mean', 'median', 'count'])
position_salary = position_salary[position_salary['count'] >= 10].sort_values('mean', ascending=True)

x = np.arange(len(position_salary))
width = 0.35

bars1 = plt.barh(x - width/2, position_salary['mean'], width, label='Average',
                 color=colors[0], edgecolor='black', linewidth=1.2)
bars2 = plt.barh(x + width/2, position_salary['median'], width, label='Median',
                 color=colors[1], edgecolor='black', linewidth=1.2)

plt.yticks(x, position_salary.index, fontsize=11)
plt.xlabel('Salary (AZN)', fontsize=12, fontweight='bold')
plt.ylabel('Position Type', fontsize=12, fontweight='bold')
plt.title('Salary Expectations by Position Type', fontsize=16, fontweight='bold', pad=20)
plt.legend(fontsize=11)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        plt.text(width_val + 20, bar.get_y() + bar.get_height()/2.,
                 f'{int(width_val)}',
                 va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/05_salary_by_position.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 6: Availability by Marital Status
# ============================================================================
plt.figure(figsize=(10, 6))
marital_counts = df_clean[df_clean['marital_status'].isin(['Subay', 'Ailəli'])]['marital_status'].value_counts()
marital_labels = ['Single', 'Married']
values = [marital_counts.get('Subay', 0), marital_counts.get('Ailəli', 0)]
bars = plt.bar(marital_labels, values, color=[colors[4], colors[2]],
               edgecolor='black', linewidth=1.2)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}\n({int(height/sum(values)*100)}%)',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Candidate Availability by Marital Status', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.xlabel('Marital Status', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/06_marital_status.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 7: Position Type Distribution in Market
# ============================================================================
plt.figure(figsize=(12, 7))
position_dist = df_clean['position_type'].value_counts()
bars = plt.barh(range(len(position_dist)), position_dist.values,
                color=colors[0], edgecolor='black', linewidth=1.2)
plt.yticks(range(len(position_dist)), position_dist.index, fontsize=11)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, position_dist.values)):
    plt.text(value + 3, i, f'{value} ({value/len(df_clean)*100:.1f}%)',
             va='center', fontsize=10, fontweight='bold')

plt.title('Talent Pool Composition by Role', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.ylabel('Position Type', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/07_position_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 8: Salary vs Age Analysis
# ============================================================================
plt.figure(figsize=(14, 7))
age_salary = df_clean[df_clean['salary'] > 0].groupby(pd.cut(df_clean[df_clean['salary'] > 0]['age'],
                                                               bins=[18, 25, 30, 35, 40, 45, 50, 70],
                                                               labels=['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50+']))['salary'].mean()

plt.plot(range(len(age_salary)), age_salary.values, marker='o', linewidth=3,
         markersize=10, color=colors[0], markerfacecolor=colors[1], markeredgewidth=2, markeredgecolor=colors[0])
plt.xticks(range(len(age_salary)), age_salary.index, rotation=45)

# Add value labels
for i, value in enumerate(age_salary.values):
    plt.text(i, value + 30, f'{int(value)} AZN',
             ha='center', fontsize=10, fontweight='bold')

plt.title('Average Salary Expectations by Age Group', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age Range', fontsize=12, fontweight='bold')
plt.ylabel('Average Salary (AZN)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/08_salary_vs_age.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 9: Gender Distribution by Position Type
# ============================================================================
plt.figure(figsize=(14, 7))
gender_position = pd.crosstab(df_clean[df_clean['gender'].isin(['Kişi', 'Qadın'])]['position_type'],
                               df_clean[df_clean['gender'].isin(['Kişi', 'Qadın'])]['gender'])
gender_position = gender_position[gender_position.sum(axis=1) >= 10].sort_values('Kişi', ascending=True)

x = np.arange(len(gender_position))
width = 0.35

bars1 = plt.barh(x - width/2, gender_position['Kişi'], width, label='Male',
                 color=colors[0], edgecolor='black', linewidth=1.2)
bars2 = plt.barh(x + width/2, gender_position['Qadın'], width, label='Female',
                 color=colors[1], edgecolor='black', linewidth=1.2)

plt.yticks(x, gender_position.index, fontsize=11)
plt.xlabel('Number of Candidates', fontsize=12, fontweight='bold')
plt.ylabel('Position Type', fontsize=12, fontweight='bold')
plt.title('Gender Distribution Across Position Types', fontsize=16, fontweight='bold', pad=20)
plt.legend(fontsize=11)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        if width_val > 0:
            plt.text(width_val + 2, bar.get_y() + bar.get_height()/2.,
                     f'{int(width_val)}',
                     va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/09_gender_by_position.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("CHART GENERATION COMPLETE")
print("="*60)
print(f"\n9 business insight charts generated in 'charts/' directory")
print("\nGenerated charts:")
print("  1. Gender Distribution")
print("  2. Geographic Distribution")
print("  3. Salary Distribution")
print("  4. Age Distribution")
print("  5. Salary by Position Type")
print("  6. Marital Status Distribution")
print("  7. Position Type Distribution")
print("  8. Salary vs Age Trends")
print("  9. Gender Distribution by Position")
print("\nAll charts saved as high-resolution PNG files (300 DPI)")
