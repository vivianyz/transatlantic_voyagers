#!/usr/bin/env python3
"""
Working Passenger Data Generator
===============================

A working version that demonstrates passenger data generation
using sample data from the Tsar's Trans-Atlantic Voyagers dataset.
"""

import random

class WorkingPassengerGenerator:
    def __init__(self):
        """Initialize with sample data"""
        print("Loading sample datasets...")
        
        # Sample voyages data (MID, arv_yr, ship, itinerary, port_arv, q_psgrs)
        self.voyages = [
            {'MID': 731, 'arv_yr': 1891, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 208},
            {'MID': 42057, 'arv_yr': 1891, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 356},
            {'MID': 653, 'arv_yr': 1892, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 113},
            {'MID': 961, 'arv_yr': 1892, 'ship': 'STEINHOEFT', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 119},
            {'MID': 3376, 'arv_yr': 1849, 'ship': 'ADAM CARR', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 3388, 'arv_yr': 1849, 'ship': 'PATRICK HENRY', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 5},
            {'MID': 36535, 'arv_yr': 1882, 'ship': 'SPEED', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 27},
            {'MID': 36637, 'arv_yr': 1882, 'ship': 'SPEED', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 11},
            {'MID': 36722, 'arv_yr': 1882, 'ship': 'SPEED', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 19},
            {'MID': 766, 'arv_yr': 1892, 'ship': 'SPEED', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 61},
            {'MID': 3447, 'arv_yr': 1849, 'ship': 'DEVONSHIRE', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 7481, 'arv_yr': 1853, 'ship': 'DEVONSHIRE', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 8721, 'arv_yr': 1856, 'ship': 'DEVONSHIRE', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 8967, 'arv_yr': 1857, 'ship': 'DEVONSHIRE', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 3},
            {'MID': 9702, 'arv_yr': 1860, 'ship': 'DEVONSHIRE', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 3456, 'arv_yr': 1849, 'ship': 'PATRICK HENRY', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 7214, 'arv_yr': 1852, 'ship': 'PATRICK HENRY', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 6431, 'arv_yr': 1850, 'ship': 'NORD AMERICA', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 6445, 'arv_yr': 1850, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 9},
            {'MID': 7306, 'arv_yr': 1852, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 8018, 'arv_yr': 1852, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 4},
            {'MID': 8415, 'arv_yr': 1855, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 8711, 'arv_yr': 1856, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 18424, 'arv_yr': 1857, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 18472, 'arv_yr': 1858, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 10402, 'arv_yr': 1865, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 30262, 'arv_yr': 1866, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 4},
            {'MID': 33091, 'arv_yr': 1873, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 33532, 'arv_yr': 1874, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 33679, 'arv_yr': 1874, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 33971, 'arv_yr': 1875, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 16},
            {'MID': 34248, 'arv_yr': 1876, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 59},
            {'MID': 34284, 'arv_yr': 1877, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 34554, 'arv_yr': 1877, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 15815, 'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 15818, 'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 24},
            {'MID': 15822, 'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 4},
            {'MID': 15835, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 15843, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 15853, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 36},
            {'MID': 15877, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 3},
            {'MID': 15887, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 15898, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 5},
            {'MID': 36152, 'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 15910, 'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 3},
            {'MID': 15923, 'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 46},
            {'MID': 15950, 'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 3},
            {'MID': 15978, 'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 16015, 'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 1},
            {'MID': 16026, 'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 37309, 'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 7},
            {'MID': 16034, 'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 16040, 'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 16046, 'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 20},
            {'MID': 16050, 'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 16053, 'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 52},
            {'MID': 16064, 'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 18},
            {'MID': 38168, 'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 48},
            {'MID': 38542, 'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 5},
            {'MID': 38677, 'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 28},
            {'MID': 38737, 'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 2},
            {'MID': 38873, 'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 20},
            {'MID': 16116, 'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 110},
            {'MID': 16123, 'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 31},
            {'MID': 16131, 'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 99},
            {'MID': 16159, 'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 91},
            {'MID': 16166, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 71},
            {'MID': 16173, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 13},
            {'MID': 16179, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 39},
            {'MID': 16202, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 73},
            {'MID': 16208, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 44},
            {'MID': 16215, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 62},
            {'MID': 16221, 'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 39},
            {'MID': 16232, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 76},
            {'MID': 16239, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 112},
            {'MID': 16250, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 97},
            {'MID': 16256, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 76},
            {'MID': 16263, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 89},
            {'MID': 16270, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 39},
            {'MID': 41205, 'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 23},
            {'MID': 16278, 'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 25},
            {'MID': 16282, 'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 42},
            {'MID': 16327, 'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 53},
            {'MID': 41416, 'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 169},
            {'MID': 41498, 'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'port_arv': 'New York', 'q_psgrs': 15},
            {'MID': 16332, 'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 59},
            {'MID': 16339, 'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 96},
            {'MID': 16349, 'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 221},
            {'MID': 16369, 'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'port_arv': 'New York', 'q_psgrs': 234}
        ]
        
        # Occupation groups
        self.occupation_groups = [
            'Agriculture', 'Manufacturing and mining', 'Trade and commerce',
            'Service and hospitality', 'Transportation and communication',
            'Construction', 'Production of food and drink', 'Leather, textiles, garments',
            'Printing and journalism', 'Education, sciences', 'Arts, entertainment, sports',
            'Government', 'Faith-related', 'Estate and household labor', 'No occupation'
        ]
        
        # Family roles
        self.family_roles = [
            'Head', 'Wife', 'Son', 'Daughter', 'Father', 'Mother', 'Brother', 'Sister',
            'Grandfather', 'Grandmother', 'Uncle', 'Aunt', 'Cousin', 'Nephew', 'Niece',
            'Son-in-law', 'Daughter-in-law', 'Father-in-law', 'Mother-in-law',
            'Stepfather', 'Stepmother', 'Stepson', 'Stepdaughter', 'Half-brother',
            'Half-sister', 'Servant', 'Boarder', 'Lodger', 'Friend', 'Partner',
            'Employee', 'Apprentice', 'Student', 'Child', 'Infant', 'Baby'
        ]
        
        # Countries of origin
        self.countries = [
            'Russia', 'Poland', 'Ukraine', 'Belarus', 'Finland', 'Germany',
            'Austria', 'Hungary', 'Romania', 'Bulgaria', 'Serbia', 'Croatia',
            'Slovenia', 'Slovakia', 'Czech Republic', 'Lithuania', 'Latvia',
            'Estonia', 'Moldova', 'Georgia', 'Armenia', 'Azerbaijan'
        ]
        
        print("Data loaded successfully!")
    
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
        year_voyages = [v for v in self.voyages if v['arv_yr'] == year]
        if not year_voyages:
            # Find closest year
            available_years = sorted(set(v['arv_yr'] for v in self.voyages))
            closest_year = min(available_years, key=lambda x: abs(x - year))
            print(f"No voyages found for year {year}. Using closest available year: {closest_year}")
            year_voyages = [v for v in self.voyages if v['arv_yr'] == closest_year]
        
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
            available_years = list(set(v['arv_yr'] for v in self.voyages))
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
            'country_of_origin': country_of_origin or random.choice(self.countries),
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'arrival_port': selected_voyage['port_arv'],
            'passenger_count': selected_voyage['q_psgrs'],
            'voyage_id': selected_voyage['MID']
        }
        
        return passenger_data

def main():
    """Main function to demonstrate the generator"""
    generator = WorkingPassengerGenerator()
    
    print("\nWorking Passenger Data Generator")
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
    
    # Example 3: Generate a random passenger
    print("\nExample 3: Random passenger")
    try:
        passenger3 = generator.generate_passenger_data(
            gender=random.choice(['M', 'F']),
            age=random.randint(1, 80),
            has_occupation=random.choice([True, False])
        )
        
        print("\n" + "="*50)
        print("GENERATED PASSENGER DATA")
        print("="*50)
        print(f"Gender: {passenger3['gender']}")
        print(f"Age: {passenger3['age']}")
        if passenger3['has_occupation']:
            print(f"Occupation: {passenger3['occupation_group']}")
        else:
            print(f"Family Role: {passenger3['family_role']}")
        print(f"Year of Travel: {passenger3['travel_year']}")
        print(f"Country of Origin: {passenger3['country_of_origin']}")
        print(f"\nOutput:")
        print(f"1. Ship Name: {passenger3['ship_name']}")
        print(f"2. Itinerary: {passenger3['itinerary']}")
        print(f"3. Passenger Count: {passenger3['passenger_count']}")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()