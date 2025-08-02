#!/usr/bin/env python3
"""
Trans-Atlantic Voyagers Data Integration
========================================

This script joins all relevant tables into a unified dataset:
- passengers: Core passenger information
- voyages: Voyage details and dates
- travelgroups: Travel group information
- occupations: Occupation categories and groups
- lkresidences: Last known residences with geographic data
- routes: Route information and itineraries
- ships: Ship details and operational periods

The result is a comprehensive dataset ready for analysis.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_all_tables():
    """Load all relevant tables from the dataverse files"""
    print("="*60)
    print("TRANS-ATLANTIC VOYAGERS DATA INTEGRATION")
    print("="*60)
    print("\nLoading all tables...")
    
    # Load all tables
    tables = {}
    
    try:
        tables['passengers'] = pd.read_csv('dataverse_files/ttav_passengers.csv')
        print(f"✓ Passengers: {len(tables['passengers']):,} records")
        
        tables['voyages'] = pd.read_csv('dataverse_files/ttav_voyages.csv')
        print(f"✓ Voyages: {len(tables['voyages']):,} records")
        
        tables['travelgroups'] = pd.read_csv('dataverse_files/ttav_trvgroups.csv')
        print(f"✓ Travel Groups: {len(tables['travelgroups']):,} records")
        
        tables['occupations'] = pd.read_csv('dataverse_files/ttav_occupations.csv')
        print(f"✓ Occupations: {len(tables['occupations']):,} records")
        
        tables['lkresidences'] = pd.read_csv('dataverse_files/ttav_lkresidences.csv')
        print(f"✓ Last Known Residences: {len(tables['lkresidences']):,} records")
        
        tables['routes'] = pd.read_csv('dataverse_files/ttav_routes.csv')
        print(f"✓ Routes: {len(tables['routes']):,} records")
        
        tables['ships'] = pd.read_csv('dataverse_files/ttav_ships.csv')
        print(f"✓ Ships: {len(tables['ships']):,} records")
        
        print(f"\n📊 Total tables loaded: {len(tables)}")
        
    except FileNotFoundError as e:
        print(f"❌ Error loading file: {e}")
        return None
    
    return tables

def examine_relationships(tables):
    """Examine the relationships between tables"""
    print("\n" + "="*60)
    print("EXAMINING TABLE RELATIONSHIPS")
    print("="*60)
    
    # Key relationships
    relationships = {
        'MID (Manifest ID)': ['passengers', 'voyages'],
        'travel_grpID': ['passengers', 'travelgroups'],
        'occID (Occupation ID)': ['passengers', 'occupations'],
        'lkrID (Last Known Residence ID)': ['passengers', 'lkresidences'],
        'routeID': ['voyages', 'routes'],
        'shipID': ['voyages', 'ships']
    }
    
    print("\n🔗 Key Relationships:")
    for key, table_list in relationships.items():
        print(f"   {key}: {' ↔ '.join(table_list)}")
    
    # Check for missing values in key columns
    print("\n🔍 Missing Values in Key Columns:")
    key_columns = {
        'passengers': ['MID', 'travel_grpID', 'occID', 'lkrID'],
        'voyages': ['MID', 'routeID', 'shipID']
    }
    
    for table_name, columns in key_columns.items():
        if table_name in tables:
            table = tables[table_name]
            print(f"\n   {table_name.upper()}:")
            for col in columns:
                if col in table.columns:
                    missing = table[col].isnull().sum()
                    missing_pct = (missing / len(table)) * 100
                    print(f"     {col}: {missing:,} missing ({missing_pct:.1f}%)")

def create_unified_dataset(tables):
    """Create a unified dataset by joining all relevant tables"""
    print("\n" + "="*60)
    print("CREATING UNIFIED DATASET")
    print("="*60)
    
    # Start with passengers as the base table
    unified = tables['passengers'].copy()
    print(f"\n1️⃣ Base table (passengers): {len(unified):,} records")
    
    # Join with voyages (MID)
    print("\n2️⃣ Joining with voyages...")
    before_count = len(unified)
    unified = unified.merge(
        tables['voyages'], 
        on='MID', 
        how='left', 
        suffixes=('', '_voyage')
    )
    after_count = len(unified)
    print(f"   After voyages join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    # Join with travel groups (travel_grpID)
    print("\n3️⃣ Joining with travel groups...")
    before_count = len(unified)
    unified = unified.merge(
        tables['travelgroups'], 
        on='travel_grpID', 
        how='left', 
        suffixes=('', '_trvgrp')
    )
    after_count = len(unified)
    print(f"   After travel groups join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    # Join with occupations (occID)
    print("\n4️⃣ Joining with occupations...")
    before_count = len(unified)
    unified = unified.merge(
        tables['occupations'], 
        on='occID', 
        how='left', 
        suffixes=('', '_occ')
    )
    after_count = len(unified)
    print(f"   After occupations join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    # Join with last known residences (lkrID)
    print("\n5️⃣ Joining with last known residences...")
    before_count = len(unified)
    unified = unified.merge(
        tables['lkresidences'], 
        on='lkrID', 
        how='left', 
        suffixes=('', '_lkr')
    )
    after_count = len(unified)
    print(f"   After residences join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    # Join with routes (routeID)
    print("\n6️⃣ Joining with routes...")
    before_count = len(unified)
    unified = unified.merge(
        tables['routes'], 
        on='routeID', 
        how='left', 
        suffixes=('', '_route')
    )
    after_count = len(unified)
    print(f"   After routes join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    # Join with ships (shipID)
    print("\n7️⃣ Joining with ships...")
    before_count = len(unified)
    unified = unified.merge(
        tables['ships'], 
        on='shipID', 
        how='left', 
        suffixes=('', '_ship')
    )
    after_count = len(unified)
    print(f"   After ships join: {after_count:,} records")
    if after_count != before_count:
        print(f"   ⚠️  Record count changed by {after_count - before_count:,}")
    
    print(f"\n✅ Final unified dataset: {len(unified):,} records with {len(unified.columns)} columns")
    
    return unified

def analyze_unified_dataset(unified):
    """Analyze the unified dataset"""
    print("\n" + "="*60)
    print("UNIFIED DATASET ANALYSIS")
    print("="*60)
    
    print(f"\n📊 Dataset Overview:")
    print(f"   Total records: {len(unified):,}")
    print(f"   Total columns: {len(unified.columns)}")
    print(f"   Memory usage: {unified.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Column categories
    column_categories = {
        'Passenger Info': ['ID', 'ln', 'fn', 'age', 'sex', 'litr', 'fam_role', 'pasg', 'goal', 'condtn'],
        'Voyage Info': ['MID', 'arv_date', 'arv_yr', 'q_psgrs', 'avg_crss'],
        'Travel Group': ['travel_grpID', 'travel_grp', 'travel_grp_size'],
        'Occupation': ['occID', 'occ_nm', 'occ_ctg', 'occ_grp'],
        'Residence': ['lkrID', 'lres', 'resdn', 'count', 'sptl_unit', 'tsar_trty', 'geonm_crd', 'geonm_lat', 'geonm_long'],
        'Route': ['routeID', 'ships', 'vygs', 'vygs_ship', 'itinry', 'port_arv'],
        'Ship': ['shipID', 'ship', 'start_yr', 'end_yr', 'sail_yrs']
    }
    
    print(f"\n📋 Column Categories:")
    for category, columns in column_categories.items():
        available_cols = [col for col in columns if col in unified.columns]
        print(f"   {category}: {len(available_cols)} columns")
        if len(available_cols) < len(columns):
            missing_cols = [col for col in columns if col not in unified.columns]
            print(f"      Missing: {missing_cols}")
    
    # Data completeness
    print(f"\n🔍 Data Completeness (Top 10 columns with missing data):")
    missing_data = unified.isnull().sum()
    missing_pct = (missing_data / len(unified)) * 100
    missing_summary = pd.DataFrame({
        'Missing_Count': missing_data,
        'Missing_Percentage': missing_pct
    }).sort_values('Missing_Count', ascending=False)
    
    top_missing = missing_summary[missing_summary['Missing_Count'] > 0].head(10)
    for col, row in top_missing.iterrows():
        print(f"   {col}: {row['Missing_Count']:,} ({row['Missing_Percentage']:.1f}%)")
    
    # Sample of the unified dataset
    print(f"\n📝 Sample Records (first 3 rows):")
    sample_cols = ['ID', 'ln', 'fn', 'age', 'sex', 'arv_yr', 'occ_nm', 'ship', 'port_arv']
    available_sample_cols = [col for col in sample_cols if col in unified.columns]
    print(unified[available_sample_cols].head(3).to_string(index=False))
    
    return missing_summary

def export_unified_dataset(unified):
    """Export the unified dataset"""
    print("\n" + "="*60)
    print("EXPORTING UNIFIED DATASET")
    print("="*60)
    
    # Export full dataset
    output_file = 'ttav_unified_dataset.csv'
    unified.to_csv(output_file, index=False)
    print(f"✅ Full unified dataset exported to: {output_file}")
    print(f"   Size: {len(unified):,} records × {len(unified.columns)} columns")
    
    # Export a sample for quick analysis
    sample_size = min(10000, len(unified))
    sample_file = 'ttav_unified_sample.csv'
    unified.sample(n=sample_size, random_state=42).to_csv(sample_file, index=False)
    print(f"✅ Sample dataset exported to: {sample_file}")
    print(f"   Size: {sample_size:,} records × {len(unified.columns)} columns")
    
    # Export column documentation
    doc_file = 'ttav_unified_columns.txt'
    with open(doc_file, 'w') as f:
        f.write("TRANS-ATLANTIC VOYAGERS UNIFIED DATASET\n")
        f.write("Column Documentation\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total Records: {len(unified):,}\n")
        f.write(f"Total Columns: {len(unified.columns)}\n\n")
        
        f.write("COLUMNS:\n")
        for i, col in enumerate(unified.columns, 1):
            dtype = str(unified.dtypes[col])
            non_null = unified[col].count()
            null_count = unified[col].isnull().sum()
            null_pct = (null_count / len(unified)) * 100
            
            f.write(f"{i:3d}. {col:<25} | {dtype:<10} | {non_null:>8} non-null | {null_pct:5.1f}% missing\n")
    
    print(f"✅ Column documentation exported to: {doc_file}")
    
    return output_file, sample_file, doc_file

def main():
    """Main execution function"""
    # Load all tables
    tables = load_all_tables()
    if tables is None:
        print("❌ Failed to load tables. Exiting.")
        return
    
    # Examine relationships
    examine_relationships(tables)
    
    # Create unified dataset
    unified = create_unified_dataset(tables)
    
    # Analyze unified dataset
    missing_summary = analyze_unified_dataset(unified)
    
    # Export unified dataset
    output_files = export_unified_dataset(unified)
    
    print("\n" + "="*60)
    print("DATA INTEGRATION COMPLETE! 🎉")
    print("="*60)
    print(f"\n📁 Generated Files:")
    for file in output_files:
        print(f"   • {file}")
    
    print(f"\n📈 Integration Summary:")
    print(f"   • Original passengers: {len(tables['passengers']):,}")
    print(f"   • Final unified records: {len(unified):,}")
    print(f"   • Total columns: {len(unified.columns)}")
    print(f"   • Tables integrated: 7 (passengers, voyages, travelgroups, occupations, residences, routes, ships)")
    
    print(f"\n🚀 Ready for analysis!")
    print(f"   Use 'ttav_unified_dataset.csv' for comprehensive analysis")
    print(f"   Use 'ttav_unified_sample.csv' for quick exploration")

if __name__ == "__main__":
    main()