#!/usr/bin/env python3
"""
The Tsar's Trans-Atlantic Voyagers: Passenger Data Visualization
================================================================

This script provides comprehensive visualizations of the passenger data from the 
Trans-Atlantic Voyagers database, documenting migration from the Russian Empire 
to the United States (1834-1897).

Dataset Overview:
- 527,394 passenger records
- Time period: 1834-1897 (63 years)
- Geographic coverage: Belarus, Finland, Poland, Russian Federation, Ukraine
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('default')
sns.set_palette("husl")

def load_data():
    """Load all necessary datasets"""
    print("Loading datasets...")
    
    # Load main passenger data
    passengers = pd.read_csv('dataverse_files/ttav_passengers.csv')
    print(f"Passengers loaded: {len(passengers):,} records")
    
    # Load supporting datasets
    occupations = pd.read_csv('dataverse_files/ttav_occupations.csv')
    voyages = pd.read_csv('dataverse_files/ttav_voyages.csv')
    
    print(f"Occupations: {len(occupations):,} categories")
    print(f"Voyages: {len(voyages):,} records")
    
    return passengers, occupations, voyages

def preprocess_data(passengers, occupations, voyages):
    """Preprocess and merge datasets"""
    print("\nPreprocessing data...")
    
    # Merge passengers with voyage data to get arrival years
    passengers_with_years = passengers.merge(voyages[['MID', 'arv_yr']], on='MID', how='left')
    print(f"Merged with voyages: {len(passengers_with_years):,} records")
    
    # Merge with occupations data
    passengers_full = passengers_with_years.merge(occupations, on='occID', how='left')
    print(f"Full dataset with occupations: {len(passengers_full):,} records")
    
    # Clean age data (remove extreme outliers)
    passengers_full = passengers_full[passengers_full['age'] <= 100]
    print(f"After age filtering: {len(passengers_full):,} records")
    
    # Add decade column
    passengers_full['decade'] = (passengers_full['arv_yr'] // 10) * 10
    
    return passengers_full

def create_demographic_analysis(passengers_full):
    """Create demographic visualizations"""
    print("\n=== Creating Demographic Analysis ===")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gender pie chart
    gender_counts = passengers_full['sex'].value_counts()
    ax1.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Gender Distribution', fontsize=14, fontweight='bold')
    
    # Age distribution by gender
    male_ages = passengers_full[passengers_full['sex'] == 'M']['age'].dropna()
    female_ages = passengers_full[passengers_full['sex'] == 'F']['age'].dropna()
    
    ax2.boxplot([male_ages, female_ages], labels=['Male', 'Female'])
    ax2.set_title('Age Distribution by Gender')
    ax2.set_ylabel('Age')
    
    # Age histogram
    ax3.hist(passengers_full['age'].dropna(), bins=50, alpha=0.7, edgecolor='black')
    ax3.set_title('Age Distribution of All Passengers')
    ax3.set_xlabel('Age')
    ax3.set_ylabel('Frequency')
    ax3.axvline(passengers_full['age'].mean(), color='red', linestyle='--', 
               label=f'Mean: {passengers_full["age"].mean():.1f}')
    ax3.legend()
    
    # Family role distribution
    family_roles = passengers_full['fam_role'].value_counts().head(10)
    ax4.barh(family_roles.index, family_roles.values)
    ax4.set_title('Top 10 Family Roles')
    ax4.set_xlabel('Count')
    
    plt.tight_layout()
    plt.savefig('demographic_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Average age: {passengers_full['age'].mean():.1f} years")
    print(f"Median age: {passengers_full['age'].median():.1f} years")
    print(f"Gender ratio (M/F): {gender_counts['M']/gender_counts['F']:.2f}")
    
    return gender_counts

def create_temporal_analysis(passengers_full):
    """Create temporal migration pattern visualizations"""
    print("\n=== Creating Temporal Analysis ===")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Annual migration counts
    yearly_migration = passengers_full.groupby('arv_yr').size()
    ax1.plot(yearly_migration.index, yearly_migration.values, marker='o', linewidth=2, markersize=4)
    ax1.set_title('Annual Migration from Russian Empire to USA (1834-1897)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Passengers')
    ax1.grid(True, alpha=0.3)
    
    # Add major historical events as vertical lines
    historical_events = {
        1861: 'Emancipation of Serfs',
        1881: 'Alexander II Assassination',
        1891: 'Russian Famine'
    }
    
    for year, event in historical_events.items():
        if year in yearly_migration.index:
            ax1.axvline(x=year, color='red', linestyle='--', alpha=0.7)
            ax1.text(year, ax1.get_ylim()[1]*0.9, event, rotation=90, 
                    verticalalignment='top', fontsize=9)
    
    # Decade-wise migration with gender breakdown
    decade_gender = passengers_full.groupby(['decade', 'sex']).size().unstack(fill_value=0)
    decade_gender.plot(kind='bar', stacked=True, ax=ax2, color=['lightblue', 'pink'])
    ax2.set_title('Migration by Decade and Gender', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Decade')
    ax2.set_ylabel('Number of Passengers')
    ax2.legend(title='Gender')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('temporal_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print decade statistics
    print("\n=== MIGRATION STATISTICS BY DECADE ===")
    decade_stats = passengers_full.groupby('decade').agg({
        'ID': 'count',
        'age': 'mean'
    }).round(1)
    decade_stats.columns = ['Passenger Count', 'Average Age']
    print(decade_stats)
    
    return yearly_migration

def create_occupational_analysis(passengers_full):
    """Create occupational analysis visualizations"""
    print("\n=== Creating Occupational Analysis ===")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
    
    # Top 15 specific occupations
    top_occupations = passengers_full['occ_nm'].value_counts().head(15)
    ax1.barh(top_occupations.index, top_occupations.values)
    ax1.set_title('Top 15 Specific Occupations', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Number of Passengers')
    
    # Occupational categories
    occ_categories = passengers_full['occ_ctg'].value_counts().head(10)
    ax2.pie(occ_categories.values, labels=occ_categories.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Top 10 Occupational Categories', fontsize=14, fontweight='bold')
    
    # Occupational groups
    occ_groups = passengers_full['occ_grp'].value_counts()
    ax3.bar(range(len(occ_groups)), occ_groups.values)
    ax3.set_title('Occupational Groups', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Occupational Group')
    ax3.set_ylabel('Number of Passengers')
    ax3.set_xticks(range(len(occ_groups)))
    ax3.set_xticklabels(occ_groups.index, rotation=45, ha='right')
    
    # Age distribution by major occupational groups
    major_occ_groups = passengers_full['occ_grp'].value_counts().head(5).index
    occ_age_data = [passengers_full[passengers_full['occ_grp'] == group]['age'].dropna() 
                    for group in major_occ_groups]
    
    ax4.boxplot(occ_age_data, labels=major_occ_groups)
    ax4.set_title('Age Distribution by Major Occupational Groups', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Occupational Group')
    ax4.set_ylabel('Age')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('occupational_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("=== OCCUPATIONAL STATISTICS ===")
    print(f"Total unique occupations: {passengers_full['occ_nm'].nunique():,}")
    print(f"Total occupational categories: {passengers_full['occ_ctg'].nunique():,}")
    print(f"Total occupational groups: {passengers_full['occ_grp'].nunique():,}")

def generate_summary_report(passengers_full, gender_counts, yearly_migration):
    """Generate comprehensive summary report"""
    print("\n" + "="*60)
    print("=== THE TSAR'S TRANS-ATLANTIC VOYAGERS: KEY INSIGHTS ===")
    print("="*60)
    
    print(f"\n📊 DATASET OVERVIEW:")
    print(f"   • Total passengers: {len(passengers_full):,}")
    print(f"   • Time period: {passengers_full['arv_yr'].min()}-{passengers_full['arv_yr'].max()} ({passengers_full['arv_yr'].max() - passengers_full['arv_yr'].min() + 1} years)")
    print(f"   • Peak migration year: {yearly_migration.idxmax()} ({yearly_migration.max():,} passengers)")
    
    print(f"\n👥 DEMOGRAPHICS:")
    print(f"   • Average age: {passengers_full['age'].mean():.1f} years")
    print(f"   • Gender distribution: {gender_counts['M']:,} male ({gender_counts['M']/len(passengers_full)*100:.1f}%), {gender_counts['F']:,} female ({gender_counts['F']/len(passengers_full)*100:.1f}%)")
    print(f"   • Most common family role: {passengers_full['fam_role'].mode().iloc[0]}")
    
    print(f"\n💼 OCCUPATIONS:")
    print(f"   • Total unique occupations: {passengers_full['occ_nm'].nunique():,}")
    print(f"   • Most common occupation: {passengers_full['occ_nm'].mode().iloc[0]}")
    print(f"   • Most common occupational group: {passengers_full['occ_grp'].mode().iloc[0]}")
    
    print(f"\n🚢 TRAVEL PATTERNS:")
    passage_pct = passengers_full['pasg'].value_counts(normalize=True) * 100
    print(f"   • Steerage passengers: {passage_pct.get('steerage', 0):.1f}%")
    print(f"   • Cabin passengers: {passage_pct.get('cabin', 0):.1f}%")
    
    print(f"\n📚 LITERACY:")
    literacy_stats = passengers_full['litr'].value_counts(normalize=True) * 100
    for status, pct in literacy_stats.head().items():
        print(f"   • {status}: {pct:.1f}%")
    
    print("\n" + "="*60)
    print("Analysis complete! Generated visualization files:")
    print("   • demographic_analysis.png")
    print("   • temporal_analysis.png") 
    print("   • occupational_analysis.png")

def main():
    """Main execution function"""
    print("="*60)
    print("THE TSAR'S TRANS-ATLANTIC VOYAGERS")
    print("Passenger Data Visualization Analysis")
    print("="*60)
    
    # Load and preprocess data
    passengers, occupations, voyages = load_data()
    passengers_full = preprocess_data(passengers, occupations, voyages)
    
    # Create visualizations
    gender_counts = create_demographic_analysis(passengers_full)
    yearly_migration = create_temporal_analysis(passengers_full)
    create_occupational_analysis(passengers_full)
    
    # Generate summary report
    generate_summary_report(passengers_full, gender_counts, yearly_migration)

if __name__ == "__main__":
    main()