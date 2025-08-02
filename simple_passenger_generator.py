#!/usr/bin/env python3
"""
Simple Passenger Data Generator
==============================

A simplified version that uses only standard Python libraries.
"""

import csv
import random
import sys
from collections import defaultdict

class SimplePassengerGenerator:
    def __init__(self):
        """Initialize the generator with data from CSV files"""
        print("Loading datasets...")
        
        # Load data from CSV files
        self.voyages = self._load_voyages()
        self.ships = self._load_ships()
        self.routes = self._load_routes()
        self.occupations = self._load_occupations()
        self.passengers = self._load_passengers()
        
        # Prepare merged data
        self._prepare_data()
        
        print("Data loaded successfully!")
    
    def _load_voyages(self):
        """Load voyages data"""
        voyages = []
        try:
            with open('dataverse_files/ttav_voyages.csv', 'r') as f:
                reader = csv.DictReader(f)
                # Print first row to debug
                first_row = next(reader)
                print(f"First voyage row: {first_row}")
                
                # Reset file pointer
                f.seek(0)
                next(reader)  # Skip header again
                
                for row in reader:
                    try:
                        voyages.append({
                            'MID': int(row['MID']),
                            'arv_yr': int(row['arv_yr']),
                            'routeID': int(row['routeID']),
                            'shipID': int(row['shipID']),
                            'q_psgrs': int(row['q_psgrs'])
                        })
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid row: {e}")
                        continue
        except FileNotFoundError:
            print("Warning: voyages file not found, using sample data")
            voyages = [
                {'MID': 1, 'arv_yr': 1880, 'routeID': 1, 'shipID': 1, 'q_psgrs': 200},
                {'MID': 2, 'arv_yr': 1890, 'routeID': 2, 'shipID': 2, 'q_psgrs': 150},
                {'MID': 3, 'arv_yr': 1885, 'routeID': 3, 'shipID': 3, 'q_psgrs': 300}
            ]
        return voyages
    
    def _load_ships(self):
        """Load ships data"""
        ships = {}
        try:
            with open('dataverse_files/ttav_ships.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ships[int(row['shipID'])] = row['ship']
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid ship row: {e}")
                        continue
        except FileNotFoundError:
            print("Warning: ships file not found, using sample data")
            ships = {1: 'VIRGINIA', 2: 'STEINHOEFT', 3: 'HERMANN'}
        return ships
    
    def _load_routes(self):
        """Load routes data"""
        routes = {}
        try:
            with open('dataverse_files/ttav_routes.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        routes[int(row['routeID'])] = {
                            'itinry': row['itinry'],
                            'port_arv': row['port_arv']
                        }
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid route row: {e}")
                        continue
        except FileNotFoundError:
            print("Warning: routes file not found, using sample data")
            routes = {
                1: {'itinry': 'Hamburg-New York', 'port_arv': 'New York'},
                2: {'itinry': 'Bremen-New York', 'port_arv': 'New York'},
                3: {'itinry': 'Havre-New York', 'port_arv': 'New York'}
            }
        return routes
    
    def _load_occupations(self):
        """Load occupations data"""
        occupation_groups = set()
        try:
            with open('dataverse_files/ttav_occupations.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if row['occ_grp'] and row['occ_grp'] != 'NA':
                            occupation_groups.add(row['occ_grp'])
                    except KeyError as e:
                        print(f"Warning: Skipping invalid occupation row: {e}")
                        continue
        except FileNotFoundError:
            print("Warning: occupations file not found, using sample data")
            occupation_groups = {
                'Agriculture', 'Manufacturing and mining', 'Trade and commerce',
                'Service and hospitality', 'Transportation and communication',
                'Construction', 'Production of food and drink', 'Leather, textiles, garments',
                'Printing and journalism', 'Education, sciences', 'Arts, entertainment, sports',
                'Government', 'Faith-related', 'Estate and household labor', 'No occupation'
            }
        return list(occupation_groups)
    
    def _load_passengers(self):
        """Load sample passenger data for family roles and countries"""
        family_roles = [
            'Head', 'Wife', 'Son', 'Daughter', 'Father', 'Mother', 'Brother', 'Sister',
            'Grandfather', 'Grandmother', 'Uncle', 'Aunt', 'Cousin', 'Nephew', 'Niece',
            'Son-in-law', 'Daughter-in-law', 'Father-in-law', 'Mother-in-law',
            'Stepfather', 'Stepmother', 'Stepson', 'Stepdaughter', 'Half-brother',
            'Half-sister', 'Servant', 'Boarder', 'Lodger', 'Friend', 'Partner',
            'Employee', 'Apprentice', 'Student', 'Child', 'Infant', 'Baby'
        ]
        
        countries = [
            'Russia', 'Poland', 'Ukraine', 'Belarus', 'Finland', 'Germany',
            'Austria', 'Hungary', 'Romania', 'Bulgaria', 'Serbia', 'Croatia',
            'Slovenia', 'Slovakia', 'Czech Republic', 'Lithuania', 'Latvia',
            'Estonia', 'Moldova', 'Georgia', 'Armenia', 'Azerbaijan'
        ]
        
        return {'family_roles': family_roles, 'countries': countries}
    
    def _prepare_data(self):
        """Prepare merged data"""
        # Create voyages with ship and route information
        self.voyages_full = []
        for voyage in self.voyages:
            ship_name = self.ships.get(voyage['shipID'], 'Unknown Ship')
            route_info = self.routes.get(voyage['routeID'], {'itinry': 'Unknown Route', 'port_arv': 'Unknown Port'})
            
            self.voyages_full.append({
                'MID': voyage['MID'],
                'arv_yr': voyage['arv_yr'],
                'ship': ship_name,
                'itinry': route_info['itinry'],
                'port_arv': route_info['port_arv'],
                'q_psgrs': voyage['q_psgrs']
            })
    
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
        return True
    
    def validate_age_for_family_role(self, age, family_role):
        """Validate if age is appropriate for the family role"""
        role_age_ranges = {
            'Head': (20, 80), 'Wife': (16, 70), 'Son': (0, 50), 'Daughter': (0, 50),
            'Father': (30, 90), 'Mother': (25, 85), 'Brother': (0, 70), 'Sister': (0, 70),
            'Grandfather': (50, 95), 'Grandmother': (45, 90), 'Uncle': (20, 85),
            'Aunt': (18, 85), 'Cousin': (0, 70), 'Nephew': (0, 60), 'Niece': (0, 60),
            'Son-in-law': (18, 70), 'Daughter-in-law': (16, 70), 'Father-in-law': (35, 90),
            'Mother-in-law': (30, 85), 'Stepfather': (25, 85), 'Stepmother': (20, 80),
            'Stepson': (0, 60), 'Stepdaughter': (0, 60), 'Half-brother': (0, 70),
            'Half-sister': (0, 70), 'Servant': (12, 70), 'Boarder': (0, 80),
            'Lodger': (0, 80), 'Friend': (0, 80), 'Partner': (18, 80), 'Employee': (14, 70),
            'Apprentice': (12, 25), 'Student': (5, 30), 'Child': (0, 18), 'Infant': (0, 3), 'Baby': (0, 2)
        }
        
        if family_role in role_age_ranges:
            min_age, max_age = role_age_ranges[family_role]
            return min_age <= age <= max_age
        return True
    
    def get_available_voyages(self, year):
        """Get available voyages for a specific year"""
        year_voyages = [v for v in self.voyages_full if v['arv_yr'] == year]
        if not year_voyages:
            # Find closest year
            available_years = sorted(set(v['arv_yr'] for v in self.voyages_full))
            closest_year = min(available_years, key=lambda x: abs(x - year))
            print(f"No voyages found for year {year}. Using closest available year: {closest_year}")
            year_voyages = [v for v in self.voyages_full if v['arv_yr'] == closest_year]
        
        return year_voyages
    
    def generate_passenger_data(self, gender, age, has_occupation, occupation_group=None,
                              family_role=None, travel_year=None, country_of_origin=None):
        """Generate passenger data based on input criteria"""
        
        # Validate inputs
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120")
        
        # Validate occupation/family role based on age
        if has_occupation:
            if occupation_group is None:
                occupation_group = random.choice(self.occupations)
            
            if not self.validate_age_for_occupation(age, occupation_group):
                print(f"Warning: Age {age} may not be appropriate for occupation group '{occupation_group}'")
        else:
            if family_role is None:
                family_role = random.choice(self.passengers['family_roles'])
            
            if not self.validate_age_for_family_role(age, family_role):
                print(f"Warning: Age {age} may not be appropriate for family role '{family_role}'")
        
        # Get available voyages for the travel year
        if travel_year is None:
            available_years = list(set(v['arv_yr'] for v in self.voyages_full))
            travel_year = random.choice(available_years)
        
        available_voyages = self.get_available_voyages(travel_year)
        
        if not available_voyages:
            raise ValueError(f"No voyages available for year {travel_year}")
        
        # Select a random voyage
        selected_voyage = random.choice(available_voyages)
        
        # Generate passenger data
        passenger_data = {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': occupation_group if has_occupation else None,
            'family_role': family_role if not has_occupation else None,
            'travel_year': selected_voyage['arv_yr'],
            'country_of_origin': country_of_origin or random.choice(self.passengers['countries']),
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'arrival_port': selected_voyage['port_arv'],
            'passenger_count': selected_voyage['q_psgrs'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data

def main():
    """Main function to demonstrate the generator"""
    generator = SimplePassengerGenerator()
    
    print("\nSimple Passenger Data Generator")
    print("="*50)
    
    # Example 1: Generate a single passenger with specific criteria
    print("\nExample 1: Specific passenger criteria")
    try:
        passenger1 = generator.generate_passenger_data(
            gender='M',
            age=25,
            has_occupation=True,
            occupation_group='Manufacturing and mining',
            travel_year=1880,
            country_of_origin='Russia'
        )
        
        print("\n" + "="*50)
        print("GENERATED PASSENGER DATA")
        print("="*50)
        print(f"Gender: {passenger1['gender']}")
        print(f"Age: {passenger1['age']}")
        print(f"Occupation: {passenger1['occupation_group']}")
        print(f"Year of Travel: {passenger1['travel_year']}")
        print(f"Country of Origin: {passenger1['country_of_origin']}")
        print(f"\nOutput:")
        print(f"1. Ship Name: {passenger1['ship_name']}")
        print(f"2. Itinerary: {passenger1['itinerary']}")
        print(f"3. Passenger Count: {passenger1['passenger_count']}")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Generate a family member
    print("\nExample 2: Family member")
    try:
        passenger2 = generator.generate_passenger_data(
            gender='F',
            age=8,
            has_occupation=False,
            family_role='Daughter',
            travel_year=1890,
            country_of_origin='Poland'
        )
        
        print("\n" + "="*50)
        print("GENERATED PASSENGER DATA")
        print("="*50)
        print(f"Gender: {passenger2['gender']}")
        print(f"Age: {passenger2['age']}")
        print(f"Family Role: {passenger2['family_role']}")
        print(f"Year of Travel: {passenger2['travel_year']}")
        print(f"Country of Origin: {passenger2['country_of_origin']}")
        print(f"\nOutput:")
        print(f"1. Ship Name: {passenger2['ship_name']}")
        print(f"2. Itinerary: {passenger2['itinerary']}")
        print(f"3. Passenger Count: {passenger2['passenger_count']}")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()