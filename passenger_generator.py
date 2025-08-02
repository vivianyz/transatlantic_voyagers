#!/usr/bin/env python3
"""
Passenger Data Generator for Tsar's Trans-Atlantic Voyagers
==========================================================

This script generates passenger data based on input criteria:
- Gender
- Age
- Occupation status (with occupation category or family relation)
- Year of travel
- Country of origin

Output includes:
- Ship name
- Itinerary
- Passenger count
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PassengerGenerator:
    def __init__(self):
        """Initialize the passenger generator with all necessary data"""
        print("Loading datasets...")
        
        # Load all necessary datasets
        self.passengers = pd.read_csv('dataverse_files/ttav_passengers.csv')
        self.occupations = pd.read_csv('dataverse_files/ttav_occupations.csv')
        self.voyages = pd.read_csv('dataverse_files/ttav_voyages.csv')
        self.ships = pd.read_csv('dataverse_files/ttav_ships.csv')
        self.routes = pd.read_csv('dataverse_files/ttav_routes.csv')
        
        # Merge datasets for easier access
        self._prepare_data()
        
        print("Data loaded successfully!")
    
    def _prepare_data(self):
        """Prepare and merge datasets"""
        # Merge voyages with ships and routes
        self.voyages_full = self.voyages.merge(
            self.ships[['shipID', 'ship']], on='shipID', how='left'
        ).merge(
            self.routes[['routeID', 'itinry', 'port_arv']], on='routeID', how='left'
        )
        
        # Get unique occupation groups
        self.occupation_groups = self.occupations['occ_grp'].dropna().unique()
        
        # Get family roles from passenger data
        self.family_roles = self.passengers['fam_role'].dropna().unique()
        
        # Get countries of origin (using lres column)
        self.countries = self.passengers['lres'].dropna().unique()
    
    def validate_age_for_occupation(self, age, occupation_group):
        """Validate if age is appropriate for the occupation group"""
        age_ranges = {
            'Agriculture': (16, 70),
            'Manufacturing and mining': (14, 65),
            'Trade and commerce': (18, 75),
            'Service and hospitality': (16, 70),
            'Transportation and communication': (18, 70),
            'Construction': (16, 65),
            'Production of food and drink': (14, 70),
            'Leather, textiles, garments': (12, 65),
            'Printing and journalism': (16, 70),
            'Education, sciences': (20, 80),
            'Arts, entertainment, sports': (12, 75),
            'Government': (18, 80),
            'Faith-related': (20, 85),
            'Estate and household labor': (12, 70),
            'No occupation': (0, 100)
        }
        
        if occupation_group in age_ranges:
            min_age, max_age = age_ranges[occupation_group]
            return min_age <= age <= max_age
        return True  # Default to accepting any age
    
    def validate_age_for_family_role(self, age, family_role):
        """Validate if age is appropriate for the family role"""
        role_age_ranges = {
            'Head': (20, 80),
            'Wife': (16, 70),
            'Son': (0, 50),
            'Daughter': (0, 50),
            'Father': (30, 90),
            'Mother': (25, 85),
            'Brother': (0, 70),
            'Sister': (0, 70),
            'Grandfather': (50, 95),
            'Grandmother': (45, 90),
            'Uncle': (20, 85),
            'Aunt': (18, 85),
            'Cousin': (0, 70),
            'Nephew': (0, 60),
            'Niece': (0, 60),
            'Son-in-law': (18, 70),
            'Daughter-in-law': (16, 70),
            'Father-in-law': (35, 90),
            'Mother-in-law': (30, 85),
            'Stepfather': (25, 85),
            'Stepmother': (20, 80),
            'Stepson': (0, 60),
            'Stepdaughter': (0, 60),
            'Half-brother': (0, 70),
            'Half-sister': (0, 70),
            'Servant': (12, 70),
            'Boarder': (0, 80),
            'Lodger': (0, 80),
            'Friend': (0, 80),
            'Partner': (18, 80),
            'Employee': (14, 70),
            'Apprentice': (12, 25),
            'Student': (5, 30),
            'Child': (0, 18),
            'Infant': (0, 3),
            'Baby': (0, 2)
        }
        
        if family_role in role_age_ranges:
            min_age, max_age = role_age_ranges[family_role]
            return min_age <= age <= max_age
        return True  # Default to accepting any age
    
    def get_available_voyages(self, year):
        """Get available voyages for a specific year"""
        year_voyages = self.voyages_full[self.voyages_full['arv_yr'] == year]
        if len(year_voyages) == 0:
            # If no voyages in exact year, find closest year
            available_years = sorted(self.voyages_full['arv_yr'].unique())
            closest_year = min(available_years, key=lambda x: abs(x - year))
            print(f"No voyages found for year {year}. Using closest available year: {closest_year}")
            year_voyages = self.voyages_full[self.voyages_full['arv_yr'] == closest_year]
        
        return year_voyages
    
    def generate_passenger_data(self, gender, age, has_occupation, occupation_group=None, 
                              family_role=None, travel_year=None, country_of_origin=None):
        """
        Generate passenger data based on input criteria
        
        Args:
            gender (str): 'M' or 'F'
            age (int): Age of the passenger
            has_occupation (bool): Whether the passenger has an occupation
            occupation_group (str): Occupation group if has_occupation is True
            family_role (str): Family role if has_occupation is False
            travel_year (int): Year of travel
            country_of_origin (str): Country of origin
            
        Returns:
            dict: Generated passenger data
        """
        
        # Validate inputs
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120")
        
        # Validate occupation/family role based on age
        if has_occupation:
            if occupation_group is None:
                occupation_group = random.choice(self.occupation_groups)
            
            if not self.validate_age_for_occupation(age, occupation_group):
                print(f"Warning: Age {age} may not be appropriate for occupation group '{occupation_group}'")
        else:
            if family_role is None:
                family_role = random.choice(self.family_roles)
            
            if not self.validate_age_for_family_role(age, family_role):
                print(f"Warning: Age {age} may not be appropriate for family role '{family_role}'")
        
        # Get available voyages for the travel year
        if travel_year is None:
            travel_year = random.choice(self.voyages_full['arv_yr'].unique())
        
        available_voyages = self.get_available_voyages(travel_year)
        
        if len(available_voyages) == 0:
            raise ValueError(f"No voyages available for year {travel_year}")
        
        # Select a random voyage
        selected_voyage = available_voyages.sample(n=1).iloc[0]
        
        # Generate passenger data
        passenger_data = {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': occupation_group if has_occupation else None,
            'family_role': family_role if not has_occupation else None,
            'travel_year': selected_voyage['arv_yr'],
            'country_of_origin': country_of_origin,
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'arrival_port': selected_voyage['port_arv'],
            'passenger_count': selected_voyage['q_psgrs'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data
    
    def generate_multiple_passengers(self, num_passengers=1, **kwargs):
        """Generate multiple passenger records"""
        passengers = []
        
        for i in range(num_passengers):
            # Generate random values for unspecified parameters
            gender = kwargs.get('gender', random.choice(['M', 'F']))
            age = kwargs.get('age', random.randint(1, 80))
            has_occupation = kwargs.get('has_occupation', random.choice([True, False]))
            
            if has_occupation:
                occupation_group = kwargs.get('occupation_group', random.choice(self.occupation_groups))
                family_role = None
            else:
                occupation_group = None
                family_role = kwargs.get('family_role', random.choice(self.family_roles))
            
            travel_year = kwargs.get('travel_year', random.choice(self.voyages_full['arv_yr'].unique()))
            country_of_origin = kwargs.get('country_of_origin', random.choice(self.countries))
            
            passenger = self.generate_passenger_data(
                gender=gender,
                age=age,
                has_occupation=has_occupation,
                occupation_group=occupation_group,
                family_role=family_role,
                travel_year=travel_year,
                country_of_origin=country_of_origin
            )
            
            passengers.append(passenger)
        
        return passengers
    
    def print_passenger_summary(self, passenger_data):
        """Print a formatted summary of the passenger data"""
        print("\n" + "="*60)
        print("PASSENGER DATA SUMMARY")
        print("="*60)
        
        print(f"Gender: {passenger_data['gender']}")
        print(f"Age: {passenger_data['age']}")
        
        if passenger_data['has_occupation']:
            print(f"Occupation: {passenger_data['occupation_group']}")
        else:
            print(f"Family Role: {passenger_data['family_role']}")
        
        print(f"Year of Travel: {passenger_data['travel_year']}")
        print(f"Country of Origin: {passenger_data['country_of_origin']}")
        
        print("\n" + "-"*40)
        print("VOYAGE INFORMATION")
        print("-"*40)
        print(f"Ship Name: {passenger_data['ship_name']}")
        print(f"Itinerary: {passenger_data['itinerary']}")
        print(f"Arrival Port: {passenger_data['arrival_port']}")
        print(f"Passenger Count: {passenger_data['passenger_count']}")
        print(f"Voyage ID: {passenger_data['voyage_id']}")
        print("="*60)

def main():
    """Main function to demonstrate the passenger generator"""
    generator = PassengerGenerator()
    
    print("\nPassenger Data Generator for Tsar's Trans-Atlantic Voyagers")
    print("="*70)
    
    # Example 1: Generate a single passenger with specific criteria
    print("\nExample 1: Specific passenger criteria")
    passenger1 = generator.generate_passenger_data(
        gender='M',
        age=25,
        has_occupation=True,
        occupation_group='Manufacturing and mining',
        travel_year=1880,
        country_of_origin='Russia'
    )
    generator.print_passenger_summary(passenger1)
    
    # Example 2: Generate a family member
    print("\nExample 2: Family member")
    passenger2 = generator.generate_passenger_data(
        gender='F',
        age=8,
        has_occupation=False,
        family_role='Daughter',
        travel_year=1890,
        country_of_origin='Poland'
    )
    generator.print_passenger_summary(passenger2)
    
    # Example 3: Generate multiple random passengers
    print("\nExample 3: Multiple random passengers")
    random_passengers = generator.generate_multiple_passengers(3)
    
    for i, passenger in enumerate(random_passengers, 1):
        print(f"\n--- Passenger {i} ---")
        generator.print_passenger_summary(passenger)

if __name__ == "__main__":
    main()