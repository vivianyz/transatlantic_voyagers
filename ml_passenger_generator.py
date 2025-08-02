#!/usr/bin/env python3
"""
Machine Learning Enhanced Passenger Data Generator
================================================

This script uses clustering algorithms to enhance passenger data generation
and provides improved occupation/family role selection logic.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import warnings
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')

class MLPassengerGenerator:
    def __init__(self):
        """Initialize the ML-enhanced passenger generator"""
        print("Loading Trans-Atlantic Voyagers data...")
        self.load_data()
        self.setup_clustering()
        self.setup_occupation_family_logic()
        
    def load_data(self):
        """Load all necessary datasets"""
        # Load main datasets
        self.passengers = pd.read_csv('dataverse_files/ttav_passengers.csv')
        self.occupations = pd.read_csv('dataverse_files/ttav_occupations.csv')
        self.voyages = pd.read_csv('dataverse_files/ttav_voyages.csv')
        self.ships = pd.read_csv('dataverse_files/ttav_ships.csv')
        self.routes = pd.read_csv('dataverse_files/ttav_routes.csv')
        
        # Merge datasets for easier access
        self.voyages_with_ships = self.voyages.merge(self.ships, on='shipID', how='left')
        self.voyages_with_routes = self.voyages_with_ships.merge(self.routes, on='routeID', how='left')
        
        # Merge passengers with voyage data
        self.passengers_with_voyages = self.passengers.merge(
            self.voyages_with_routes[['MID', 'arv_yr', 'ship', 'itinry', 'q_psgrs', 'port_arv']], 
            on='MID', how='left'
        )
        
        print(f"Loaded {len(self.passengers):,} passenger records")
        print(f"Loaded {len(self.occupations):,} occupation categories")
        print(f"Loaded {len(self.voyages):,} voyage records")
        print(f"Loaded {len(self.ships):,} ship records")
        print(f"Loaded {len(self.routes):,} route records")
    
    def setup_clustering(self):
        """Setup clustering models for passenger segmentation"""
        print("\nSetting up clustering models...")
        
        # Prepare data for clustering
        clustering_data = self.prepare_clustering_data()
        
        # Create clusters based on demographic patterns
        self.passenger_clusters = self.create_passenger_clusters(clustering_data)
        
        # Create clusters based on voyage patterns
        self.voyage_clusters = self.create_voyage_clusters()
        
        print(f"Created {len(self.passenger_clusters)} passenger clusters")
        print(f"Created {len(self.voyage_clusters)} voyage clusters")
    
    def prepare_clustering_data(self):
        """Prepare data for clustering analysis"""
        # Clean and prepare passenger data
        clean_passengers = self.passengers_with_voyages.copy()
        
        # Remove rows with missing critical data
        clean_passengers = clean_passengers.dropna(subset=['age', 'sex', 'arv_yr'])
        
        # Create features for clustering
        clustering_features = pd.DataFrame()
        
        # Age features
        clustering_features['age'] = clean_passengers['age']
        clustering_features['age_group'] = pd.cut(clean_passengers['age'], 
                                                bins=[0, 12, 17, 25, 65, 100], 
                                                labels=['child', 'teen', 'young_adult', 'adult', 'elderly'])
        
        # Gender encoding
        clustering_features['gender_male'] = (clean_passengers['sex'] == 'M').astype(int)
        clustering_features['gender_female'] = (clean_passengers['sex'] == 'F').astype(int)
        
        # Year features
        clustering_features['year'] = clean_passengers['arv_yr']
        clustering_features['decade'] = (clean_passengers['arv_yr'] // 10) * 10
        
        # Occupation features
        clean_passengers_with_occ = clean_passengers.merge(self.occupations, on='occID', how='left')
        clustering_features['has_occupation'] = (clean_passengers_with_occ['occ_grp'] != 'No occupation').astype(int)
        
        # Voyage features
        clustering_features['passenger_count'] = clean_passengers['q_psgrs']
        clustering_features['voyage_size'] = pd.cut(clean_passengers['q_psgrs'], 
                                                  bins=[0, 50, 100, 200, 1000], 
                                                  labels=['small', 'medium', 'large', 'very_large'])
        
        return clustering_features
    
    def create_passenger_clusters(self, clustering_data):
        """Create passenger clusters using K-means"""
        # Prepare features for clustering
        features_for_clustering = clustering_data[['age', 'gender_male', 'gender_female', 'year', 'has_occupation']].copy()
        
        # Remove any remaining NaN values
        features_for_clustering = features_for_clustering.dropna()
        
        if len(features_for_clustering) == 0:
            print("Warning: No valid data for clustering, using fallback method")
            return self.create_fallback_clusters()
        
        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_for_clustering)
        
        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=3)
        features_pca = pca.fit_transform(features_scaled)
        
        # Create clusters
        kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(features_pca)
        
        # Add cluster information to original data
        clustering_data_clean = clustering_data.dropna(subset=['age', 'gender_male', 'gender_female', 'year', 'has_occupation'])
        clustering_data_clean['cluster'] = cluster_labels
        
        # Analyze clusters
        cluster_analysis = self.analyze_clusters(clustering_data_clean)
        
        return cluster_analysis
    
    def create_fallback_clusters(self):
        """Create fallback clusters when ML clustering fails"""
        print("Creating fallback clusters based on age groups...")
        
        # Create simple age-based clusters
        cluster_analysis = {
            0: {'size': 1000, 'avg_age': 8, 'age_std': 3, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.0, 'age_groups': {'child': 1000}},
            1: {'size': 1000, 'avg_age': 15, 'age_std': 2, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.2, 'age_groups': {'teen': 1000}},
            2: {'size': 1000, 'avg_age': 22, 'age_std': 3, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.6, 'age_groups': {'young_adult': 1000}},
            3: {'size': 1000, 'avg_age': 35, 'age_std': 10, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.8, 'age_groups': {'adult': 1000}},
            4: {'size': 1000, 'avg_age': 70, 'age_std': 8, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.3, 'age_groups': {'elderly': 1000}},
            5: {'size': 1000, 'avg_age': 45, 'age_std': 15, 'gender_distribution': 0.5, 'avg_year': 1880, 'occupation_rate': 0.7, 'age_groups': {'adult': 1000}}
        }
        
        return cluster_analysis
    
    def create_voyage_clusters(self):
        """Create voyage clusters based on route patterns"""
        # Group voyages by route characteristics
        voyage_features = self.voyages_with_routes.groupby('routeID').agg({
            'q_psgrs': ['mean', 'std', 'count'],
            'arv_yr': ['min', 'max'],
            'shipID': 'nunique'
        }).reset_index()
        
        # Flatten column names
        voyage_features.columns = ['routeID', 'avg_passengers', 'std_passengers', 'voyage_count', 
                                 'min_year', 'max_year', 'unique_ships']
        
        # Prepare features for clustering
        features_for_clustering = voyage_features[['avg_passengers', 'voyage_count', 'unique_ships']].copy()
        
        # Remove any NaN values
        features_for_clustering = features_for_clustering.dropna()
        
        if len(features_for_clustering) == 0:
            print("Warning: No valid voyage data for clustering, using fallback")
            return self.create_fallback_voyage_clusters()
        
        # Standardize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_for_clustering)
        
        # Create clusters
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        # Add cluster information
        voyage_features_clean = voyage_features.dropna(subset=['avg_passengers', 'voyage_count', 'unique_ships'])
        voyage_features_clean['cluster'] = cluster_labels
        
        return voyage_features_clean
    
    def create_fallback_voyage_clusters(self):
        """Create fallback voyage clusters when ML clustering fails"""
        print("Creating fallback voyage clusters...")
        
        # Create simple voyage clusters based on passenger count
        voyage_features = pd.DataFrame({
            'routeID': [1, 2, 3, 4],
            'avg_passengers': [50, 150, 300, 500],
            'std_passengers': [20, 50, 100, 150],
            'voyage_count': [10, 20, 30, 40],
            'min_year': [1834, 1834, 1834, 1834],
            'max_year': [1897, 1897, 1897, 1897],
            'unique_ships': [5, 10, 15, 20],
            'cluster': [0, 1, 2, 3]
        })
        
        return voyage_features
    
    def analyze_clusters(self, clustering_data):
        """Analyze cluster characteristics"""
        cluster_analysis = {}
        
        for cluster_id in clustering_data['cluster'].unique():
            cluster_data = clustering_data[clustering_data['cluster'] == cluster_id]
            
            analysis = {
                'size': len(cluster_data),
                'avg_age': cluster_data['age'].mean(),
                'age_std': cluster_data['age'].std(),
                'gender_distribution': cluster_data['gender_male'].mean(),
                'avg_year': cluster_data['year'].mean(),
                'occupation_rate': cluster_data['has_occupation'].mean(),
                'age_groups': cluster_data['age_group'].value_counts().to_dict()
            }
            
            cluster_analysis[cluster_id] = analysis
        
        return cluster_analysis
    
    def setup_occupation_family_logic(self):
        """Setup improved occupation and family role selection logic"""
        # Get all occupation groups from the dataset
        self.occupation_groups = self.occupations['occ_grp'].dropna().unique().tolist()
        
        # Get all family roles from the dataset
        self.family_roles = self.passengers['fam_role'].dropna().unique().tolist()
        
        # Create age-appropriate occupation mapping
        self.age_occupation_mapping = {
            'child': (0, 12, ['No occupation']),
            'teen': (13, 17, ['No occupation', 'Manufacturing and mining', 'Service and hospitality']),
            'young_adult': (18, 25, ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 
                                    'Trade and commerce', 'Agriculture']),
            'adult': (26, 65, self.occupation_groups),
            'elderly': (66, 100, ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 
                                 'Trade and commerce', 'Agriculture', 'Government', 'Education, sciences', 
                                 'Arts, entertainment, sports'])
        }
        
        # Create age-appropriate family role mapping
        self.age_family_mapping = {
            'child': ['Child', 'Son', 'Daughter', 'Infant'],
            'teen': ['Child', 'Son', 'Daughter', 'Student'],
            'young_adult': ['Head', 'Son', 'Daughter', 'Student', 'Servant'],
            'adult': ['Head', 'Wife', 'Husband', 'Son', 'Daughter', 'Servant', 'Relative'],
            'elderly': ['Head', 'Wife', 'Husband', 'Relative']
        }
        
        print(f"Available occupation groups: {len(self.occupation_groups)}")
        print(f"Available family roles: {len(self.family_roles)}")
    
    def get_age_category(self, age):
        """Determine age category for occupation/family role selection"""
        for category, (min_age, max_age, _) in self.age_occupation_mapping.items():
            if min_age <= age <= max_age:
                return category
        return 'adult'  # default
    
    def select_occupation_or_family_role(self, age, has_occupation, gender=None):
        """Select appropriate occupation or family role based on user input"""
        age_category = self.get_age_category(age)
        
        if has_occupation:
            # User has occupation - select from occupation groups
            available_occupations = self.age_occupation_mapping[age_category][2]
            # Filter out 'No occupation' since user has occupation
            available_occupations = [occ for occ in available_occupations if occ != 'No occupation']
            
            if not available_occupations:
                # Fallback to all occupation groups if none available for age
                available_occupations = [occ for occ in self.occupation_groups if occ != 'No occupation']
            
            selected_occupation = random.choice(available_occupations)
            return {'occupation_group': selected_occupation, 'family_role': None}
        else:
            # User has no occupation - select family role
            available_family_roles = self.age_family_mapping[age_category]
            
            # Consider gender for family roles if provided
            if gender:
                if gender == 'M':
                    # Prefer male family roles
                    male_roles = ['Son', 'Husband', 'Head', 'Relative']
                    available_family_roles = [role for role in available_family_roles if role in male_roles]
                elif gender == 'F':
                    # Prefer female family roles
                    female_roles = ['Daughter', 'Wife', 'Head', 'Relative']
                    available_family_roles = [role for role in available_family_roles if role in female_roles]
            
            if not available_family_roles:
                # Fallback to all family roles
                available_family_roles = self.family_roles
            
            selected_family_role = random.choice(available_family_roles)
            return {'occupation_group': 'No occupation', 'family_role': selected_family_role}
    
    def get_cluster_based_voyage(self, age, gender, year):
        """Get voyage based on cluster patterns"""
        # Find similar passengers in the dataset
        similar_passengers = self.passengers_with_voyages[
            (self.passengers_with_voyages['age'].between(age-5, age+5)) &
            (self.passengers_with_voyages['sex'] == gender) &
            (self.passengers_with_voyages['arv_yr'] == year)
        ]
        
        if len(similar_passengers) > 0:
            # Select from similar passengers
            selected_voyage = similar_passengers.sample(n=1).iloc[0]
        else:
            # Fallback to any voyage in the year
            year_voyages = self.voyages_with_routes[self.voyages_with_routes['arv_yr'] == year]
            if len(year_voyages) > 0:
                selected_voyage = year_voyages.sample(n=1).iloc[0]
            else:
                raise ValueError(f"No voyages found for year {year}")
        
        return selected_voyage
    
    def generate_passenger_data(self, gender, age, has_occupation, arv_yr, country_of_origin):
        """
        Generate passenger data using ML clustering and improved logic
        
        Args:
            gender (str): 'M' or 'F'
            age (int): Age of passenger
            has_occupation (bool): Whether the passenger has an occupation
            arv_yr (int): Year of arrival
            country_of_origin (str): Country of origin
            
        Returns:
            dict: Generated passenger data
        """
        # Validate inputs
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if age < 0 or age > 100:
            raise ValueError("Age must be between 0 and 100")
        
        if arv_yr not in self.get_available_years():
            raise ValueError(f"Year {arv_yr} not available in dataset")
        
        # Select occupation or family role based on user input
        role_selection = self.select_occupation_or_family_role(age, has_occupation, gender)
        
        # Get cluster-based voyage
        selected_voyage = self.get_cluster_based_voyage(age, gender, arv_yr)
        
        # Generate passenger data
        passenger_data = {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': role_selection['occupation_group'],
            'family_role': role_selection['family_role'],
            'arv_yr': arv_yr,
            'country_of_origin': country_of_origin,
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'q_psgrs': selected_voyage['q_psgrs'],
            'port_arrival': selected_voyage['port_arv'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data

    def generate_passenger_data_with_selections(self, gender, age, has_occupation, arv_yr, country_of_origin, occupation_group=None, family_role=None):
        """
        Generate passenger data using ML clustering with user-selected occupation/family role
        
        Args:
            gender (str): 'M' or 'F'
            age (int): Age of passenger
            has_occupation (bool): Whether the passenger has an occupation
            arv_yr (int): Year of arrival
            country_of_origin (str): Country of origin
            occupation_group (str): User-selected occupation group (if has occupation)
            family_role (str): User-selected family role (if no occupation)
            
        Returns:
            dict: Generated passenger data
        """
        # Validate inputs
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if age < 0 or age > 100:
            raise ValueError("Age must be between 0 and 100")
        
        if arv_yr not in self.get_available_years():
            raise ValueError(f"Year {arv_yr} not available in dataset")
        
        # Validate occupation/family role selections
        if has_occupation:
            if not occupation_group:
                raise ValueError("Occupation group is required when has occupation is true")
            if occupation_group not in self.occupation_groups:
                raise ValueError(f"Invalid occupation group: {occupation_group}")
        else:
            if not family_role:
                raise ValueError("Family role is required when has occupation is false")
            if family_role not in self.family_roles:
                raise ValueError(f"Invalid family role: {family_role}")
        
        # Get cluster-based voyage
        selected_voyage = self.get_cluster_based_voyage(age, gender, arv_yr)
        
        # Generate passenger data with user selections
        passenger_data = {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': occupation_group if has_occupation else 'No occupation',
            'family_role': family_role if not has_occupation else None,
            'arv_yr': arv_yr,
            'country_of_origin': country_of_origin,
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'q_psgrs': selected_voyage['q_psgrs'],
            'port_arrival': selected_voyage['port_arv'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data
    
    def get_available_years(self):
        """Get available years from the dataset"""
        return sorted(self.voyages['arv_yr'].unique())
    
    def get_available_countries(self):
        """Get available countries of origin from the dataset"""
        countries = self.passengers['lres'].dropna().unique()
        return sorted(countries)
    
    def get_cluster_statistics(self):
        """Get statistics about the clusters"""
        stats = {
            'passenger_clusters': len(self.passenger_clusters),
            'voyage_clusters': len(self.voyage_clusters),
            'cluster_details': self.passenger_clusters
        }
        return stats
    
    def print_passenger_summary(self, passenger_data):
        """Print a formatted summary of the generated passenger data"""
        print("\n" + "="*60)
        print("ML-ENHANCED PASSENGER DATA GENERATION")
        print("="*60)
        print(f"Gender: {passenger_data['gender']}")
        print(f"Age: {passenger_data['age']}")
        print(f"Has Occupation: {passenger_data['has_occupation']}")
        
        if passenger_data['has_occupation']:
            print(f"Occupation Group: {passenger_data['occupation_group']}")
        else:
            print(f"Family Role: {passenger_data['family_role']}")
        
        print(f"Year of Travel: {passenger_data['arv_yr']}")
        print(f"Country of Origin: {passenger_data['country_of_origin']}")
        print("\n" + "-"*40)
        print("CLUSTER-BASED VOYAGE DETAILS")
        print("-"*40)
        print(f"Ship Name: {passenger_data['ship_name']}")
        print(f"Itinerary: {passenger_data['itinerary']}")
        print(f"Number of Passengers: {passenger_data['q_psgrs']}")
        print(f"Port of Arrival: {passenger_data['port_arrival']}")
        print(f"Voyage ID: {passenger_data['voyage_id']}")
        print("="*60)

def main():
    """Main function to demonstrate the ML-enhanced passenger generator"""
    print("Machine Learning Enhanced Passenger Data Generator")
    print("="*60)
    
    # Initialize generator
    generator = MLPassengerGenerator()
    
    # Show cluster statistics
    print("\nCluster Analysis:")
    cluster_stats = generator.get_cluster_statistics()
    print(f"Passenger Clusters: {cluster_stats['passenger_clusters']}")
    print(f"Voyage Clusters: {cluster_stats['voyage_clusters']}")
    
    # Example 1: Generate a working adult male
    print("\nExample 1: Working Adult Male")
    print("-"*40)
    
    try:
        passenger1 = generator.generate_passenger_data(
            gender='M',
            age=30,
            has_occupation=True,
            arv_yr=1890,
            country_of_origin='POLAND'
        )
        generator.print_passenger_summary(passenger1)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 2: Generate a family member (no occupation)
    print("\nExample 2: Family Member (No Occupation)")
    print("-"*40)
    
    try:
        passenger2 = generator.generate_passenger_data(
            gender='F',
            age=25,
            has_occupation=False,
            arv_yr=1885,
            country_of_origin='RUSSIA'
        )
        generator.print_passenger_summary(passenger2)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 3: Generate a child (no occupation)
    print("\nExample 3: Child (No Occupation)")
    print("-"*40)
    
    try:
        passenger3 = generator.generate_passenger_data(
            gender='M',
            age=8,
            has_occupation=False,
            arv_yr=1890,
            country_of_origin='GERMANY'
        )
        generator.print_passenger_summary(passenger3)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()