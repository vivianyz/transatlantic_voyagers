#!/usr/bin/env python3
"""
Passenger Data Generator for Trans-Atlantic Voyagers
===================================================

This script generates realistic passenger data based on input criteria:
- Gender
- Age
- Occupation status (with occupation category or family relation)
- Year of travel
- Country of origin

Outputs:
- Ship name
- Itinerary
- Number of passengers (q_psgrs)
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PassengerGenerator:
    def __init__(self):
        """Initialize the passenger generator with data loading"""
        print("Loading Trans-Atlantic Voyagers data...")
        self.load_data()
        self.setup_age_occupation_rules()
        
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
        
        print(f"Loaded {len(self.passengers):,} passenger records")
        print(f"Loaded {len(self.occupations):,} occupation categories")
        print(f"Loaded {len(self.voyages):,} voyage records")
        print(f"Loaded {len(self.ships):,} ship records")
        print(f"Loaded {len(self.routes):,} route records")
    
    def setup_age_occupation_rules(self):
        """Setup age-appropriate occupation and family role rules"""
        # Age-appropriate occupation categories
        self.age_occupation_rules = {
            'child': (0, 12, ['No occupation']),
            'teen': (13, 17, ['No occupation', 'Manufacturing and mining', 'Service and hospitality']),
            'young_adult': (18, 25, ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 'Trade and commerce', 'Agriculture']),
            'adult': (26, 65, ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 'Trade and commerce', 'Agriculture', 'Government', 'Education, sciences', 'Arts, entertainment, sports', 'Construction', 'Transportation and communication', 'Production of food and drink', 'Leather, textiles, garments', 'Printing and journalism', 'Faith-related']),
            'elderly': (66, 100, ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 'Trade and commerce', 'Agriculture', 'Government', 'Education, sciences', 'Arts, entertainment, sports'])
        }
        
        # Age-appropriate family roles
        self.age_family_rules = {
            'child': ['Child', 'Son', 'Daughter', 'Infant'],
            'teen': ['Child', 'Son', 'Daughter', 'Student'],
            'young_adult': ['Head', 'Son', 'Daughter', 'Student', 'Servant'],
            'adult': ['Head', 'Wife', 'Husband', 'Son', 'Daughter', 'Servant', 'Relative'],
            'elderly': ['Head', 'Wife', 'Husband', 'Relative']
        }
        
        # Get unique occupation groups
        self.occupation_groups = self.occupations['occ_grp'].dropna().unique().tolist()
        
    def get_age_category(self, age):
        """Determine age category for occupation/family role selection"""
        for category, (min_age, max_age, _) in self.age_occupation_rules.items():
            if min_age <= age <= max_age:
                return category
        return 'adult'  # default
    
    def validate_age_occupation_consistency(self, age, occupation_group, family_role):
        """Ensure age is consistent with occupation and family role"""
        age_category = self.get_age_category(age)
        
        # Check if occupation is appropriate for age
        if occupation_group != 'No occupation':
            allowed_occupations = self.age_occupation_rules[age_category][2]
            if occupation_group not in allowed_occupations:
                return False
        
        # Check if family role is appropriate for age
        allowed_family_roles = self.age_family_rules[age_category]
        if family_role not in allowed_family_roles:
            return False
            
        return True
    
    def get_available_years(self):
        """Get available years from the dataset"""
        return sorted(self.voyages['arv_yr'].unique())
    
    def get_available_countries(self):
        """Get available countries of origin from the dataset"""
        # Extract countries from residence data
        countries = self.passengers['lres'].dropna().unique()
        return sorted(countries)
    
    def generate_passenger_data(self, gender, age, has_occupation, arv_yr, country_of_origin):
        """
        Generate passenger data based on input criteria
        
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
        
        # Get age category
        age_category = self.get_age_category(age)
        
        # Determine occupation or family role
        if has_occupation:
            # Select occupation group appropriate for age
            allowed_occupations = self.age_occupation_rules[age_category][2]
            occupation_group = random.choice(allowed_occupations)
            family_role = None
        else:
            # Select family role appropriate for age
            allowed_family_roles = self.age_family_rules[age_category]
            family_role = random.choice(allowed_family_roles)
            occupation_group = 'No occupation'
        
        # Find voyages for the specified year
        year_voyages = self.voyages_with_routes[self.voyages_with_routes['arv_yr'] == arv_yr]
        
        if len(year_voyages) == 0:
            raise ValueError(f"No voyages found for year {arv_yr}")
        
        # Select a random voyage from the year
        selected_voyage = year_voyages.sample(n=1).iloc[0]
        
        # Generate passenger data
        passenger_data = {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': occupation_group,
            'family_role': family_role,
            'arv_yr': arv_yr,
            'country_of_origin': country_of_origin,
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'q_psgrs': selected_voyage['q_psgrs'],
            'port_arrival': selected_voyage['port_arv'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data
    
    def generate_multiple_passengers(self, num_passengers=5):
        """Generate multiple random passengers for demonstration"""
        results = []
        
        available_years = self.get_available_years()
        available_countries = self.get_available_countries()
        
        for i in range(num_passengers):
            # Random parameters
            gender = random.choice(['M', 'F'])
            age = random.randint(1, 80)
            has_occupation = random.choice([True, False])
            arv_yr = random.choice(available_years)
            country_of_origin = random.choice(available_countries)
            
            try:
                passenger_data = self.generate_passenger_data(
                    gender, age, has_occupation, arv_yr, country_of_origin
                )
                results.append(passenger_data)
            except ValueError as e:
                print(f"Error generating passenger {i+1}: {e}")
                continue
        
        return results
    
    def print_passenger_summary(self, passenger_data):
        """Print a formatted summary of the generated passenger data"""
        print("\n" + "="*60)
        print("GENERATED PASSENGER DATA")
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
        print("VOYAGE DETAILS")
        print("-"*40)
        print(f"Ship Name: {passenger_data['ship_name']}")
        print(f"Itinerary: {passenger_data['itinerary']}")
        print(f"Number of Passengers: {passenger_data['q_psgrs']}")
        print(f"Port of Arrival: {passenger_data['port_arrival']}")
        print(f"Voyage ID: {passenger_data['voyage_id']}")
        print("="*60)

def main():
    """Main function to demonstrate the passenger generator"""
    print("Trans-Atlantic Voyagers Passenger Data Generator")
    print("="*50)
    
    # Initialize generator
    generator = PassengerGenerator()
    
    # Example 1: Generate a specific passenger
    print("\nExample 1: Specific Passenger Generation")
    print("-"*40)
    
    try:
        passenger1 = generator.generate_passenger_data(
            gender='M',
            age=25,
            has_occupation=True,
            arv_yr=1890,
            country_of_origin='Russia'
        )
        generator.print_passenger_summary(passenger1)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 2: Generate a family member (no occupation)
    print("\nExample 2: Family Member Generation")
    print("-"*40)
    
    try:
        passenger2 = generator.generate_passenger_data(
            gender='F',
            age=8,
            has_occupation=False,
            arv_yr=1885,
            country_of_origin='Poland'
        )
        generator.print_passenger_summary(passenger2)
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 3: Generate multiple random passengers
    print("\nExample 3: Multiple Random Passengers")
    print("-"*40)
    
    random_passengers = generator.generate_multiple_passengers(3)
    for i, passenger in enumerate(random_passengers, 1):
        print(f"\nPassenger {i}:")
        generator.print_passenger_summary(passenger)
    
    # Show available options
    print("\n" + "="*50)
    print("AVAILABLE OPTIONS")
    print("="*50)
    print(f"Available Years: {len(generator.get_available_years())} years")
    print(f"Sample Years: {generator.get_available_years()[:10]}...")
    print(f"Available Countries: {len(generator.get_available_countries())} countries")
    print(f"Sample Countries: {generator.get_available_countries()[:10]}...")
    print(f"Occupation Groups: {len(generator.occupation_groups)} categories")
    print(f"Sample Groups: {generator.occupation_groups[:10]}...")

if __name__ == "__main__":
    main()