#!/usr/bin/env python3
"""
Passenger Data Generator - Final Version
=======================================

This script generates passenger data based on the exact input/output format requested:

Input:
1. Gender
2. Age  
3. Ask if this character works (have occupation)
   If yes, pick an occupation category (occ_grp)
   If not, pick a family relation. Make sure the age is in line with age.
4. Year of travel: arv_yr
5. Country of origin

Output:
1. Ship name
2. Itinerary  
3. Passenger count (q_psgrs)
"""

import random

class PassengerGenerator:
    def __init__(self):
        """Initialize with sample data"""
        print("Loading passenger data...")
        
        # Sample voyages data
        self.voyages = [
            {'arv_yr': 1849, 'ship': 'ADAM CARR', 'itinry': 'Bremen-New York', 'q_psgrs': 2},
            {'arv_yr': 1849, 'ship': 'PATRICK HENRY', 'itinry': 'Havre-New York', 'q_psgrs': 5},
            {'arv_yr': 1850, 'ship': 'NORD AMERICA', 'itinry': 'Hamburg-New York', 'q_psgrs': 1},
            {'arv_yr': 1850, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 9},
            {'arv_yr': 1852, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 1},
            {'arv_yr': 1852, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 4},
            {'arv_yr': 1855, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'q_psgrs': 1},
            {'arv_yr': 1856, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'q_psgrs': 1},
            {'arv_yr': 1857, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1858, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1865, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1866, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 4},
            {'arv_yr': 1873, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'q_psgrs': 1},
            {'arv_yr': 1874, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1874, 'ship': 'HERMANN', 'itinry': 'Havre-New York', 'q_psgrs': 1},
            {'arv_yr': 1875, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 16},
            {'arv_yr': 1876, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 59},
            {'arv_yr': 1877, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 24},
            {'arv_yr': 1880, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 4},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 1},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 36},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 3},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 5},
            {'arv_yr': 1881, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 1},
            {'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 3},
            {'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 46},
            {'arv_yr': 1882, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 3},
            {'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 1},
            {'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1883, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 7},
            {'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1884, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 20},
            {'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 2},
            {'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 52},
            {'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 18},
            {'arv_yr': 1885, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 48},
            {'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 5},
            {'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 28},
            {'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 2},
            {'arv_yr': 1886, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 20},
            {'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 110},
            {'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 31},
            {'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 99},
            {'arv_yr': 1887, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 91},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 71},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 13},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 39},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 73},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 44},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 62},
            {'arv_yr': 1888, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 39},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 76},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 112},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 97},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 76},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 89},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 39},
            {'arv_yr': 1889, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 23},
            {'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 25},
            {'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 42},
            {'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 53},
            {'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 169},
            {'arv_yr': 1890, 'ship': 'HERMANN', 'itinry': 'Bremen-New York', 'q_psgrs': 15},
            {'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 59},
            {'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 96},
            {'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 221},
            {'arv_yr': 1891, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 234},
            {'arv_yr': 1891, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'q_psgrs': 208},
            {'arv_yr': 1891, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'q_psgrs': 356},
            {'arv_yr': 1892, 'ship': 'VIRGINIA', 'itinry': 'Hamburg-New York', 'q_psgrs': 113},
            {'arv_yr': 1892, 'ship': 'STEINHOEFT', 'itinry': 'Hamburg-New York', 'q_psgrs': 119},
            {'arv_yr': 1892, 'ship': 'HERMANN', 'itinry': 'Hamburg-New York', 'q_psgrs': 61}
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
    
    def get_user_input(self):
        """Get input from user following the exact format requested"""
        print("\n" + "="*60)
        print("PASSENGER DATA GENERATOR")
        print("="*60)
        
        # 1. Gender
        while True:
            gender = input("1. Gender (M/F): ").strip().upper()
            if gender in ['M', 'F']:
                break
            print("Please enter 'M' for Male or 'F' for Female")
        
        # 2. Age
        while True:
            try:
                age = int(input("2. Age: "))
                if 0 <= age <= 120:
                    break
                print("Please enter an age between 0 and 120")
            except ValueError:
                print("Please enter a valid number for age")
        
        # 3. Occupation status
        while True:
            occupation_choice = input("3. Does this character work? (y/n): ").strip().lower()
            if occupation_choice in ['y', 'yes']:
                has_occupation = True
                break
            elif occupation_choice in ['n', 'no']:
                has_occupation = False
                break
            print("Please enter 'y' for yes or 'n' for no")
        
        # 4. Occupation group or family role
        if has_occupation:
            print("\nAvailable occupation groups:")
            for i, group in enumerate(self.occupation_groups, 1):
                print(f"{i:2d}. {group}")
            
            while True:
                try:
                    choice = int(input("\nSelect occupation group (enter number): "))
                    if 1 <= choice <= len(self.occupation_groups):
                        occupation_group = self.occupation_groups[choice - 1]
                        family_role = None
                        break
                    print(f"Please enter a number between 1 and {len(self.occupation_groups)}")
                except ValueError:
                    print("Please enter a valid number")
        else:
            print("\nAvailable family roles:")
            for i, role in enumerate(self.family_roles, 1):
                print(f"{i:2d}. {role}")
            
            while True:
                try:
                    choice = int(input("\nSelect family role (enter number): "))
                    if 1 <= choice <= len(self.family_roles):
                        family_role = self.family_roles[choice - 1]
                        occupation_group = None
                        break
                    print(f"Please enter a number between 1 and {len(self.family_roles)}")
                except ValueError:
                    print("Please enter a valid number")
        
        # 5. Year of travel
        while True:
            try:
                travel_year = int(input("\n4. Year of travel (1849-1892): "))
                if 1849 <= travel_year <= 1892:
                    break
                print("Please enter a year between 1849 and 1892")
            except ValueError:
                print("Please enter a valid year")
        
        # 6. Country of origin
        print("\nAvailable countries of origin:")
        for i, country in enumerate(self.countries, 1):
            print(f"{i:2d}. {country}")
        
        while True:
            try:
                choice = int(input("\nSelect country of origin (enter number): "))
                if 1 <= choice <= len(self.countries):
                    country_of_origin = self.countries[choice - 1]
                    break
                print(f"Please enter a number between 1 and {len(self.countries)}")
            except ValueError:
                print("Please enter a valid number")
        
        return {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'occupation_group': occupation_group,
            'family_role': family_role,
            'travel_year': travel_year,
            'country_of_origin': country_of_origin
        }
    
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
    
    def generate_passenger_data(self, **kwargs):
        """Generate passenger data based on input criteria"""
        
        # Get available voyages for the travel year
        available_voyages = self.get_available_voyages(kwargs['travel_year'])
        
        if not available_voyages:
            raise ValueError(f"No voyages available for year {kwargs['travel_year']}")
        
        # Select a random voyage
        selected_voyage = random.choice(available_voyages)
        
        # Generate passenger data
        passenger_data = {
            'gender': kwargs['gender'],
            'age': kwargs['age'],
            'has_occupation': kwargs['has_occupation'],
            'occupation_group': kwargs.get('occupation_group'),
            'family_role': kwargs.get('family_role'),
            'travel_year': selected_voyage['arv_yr'],
            'country_of_origin': kwargs['country_of_origin'],
            'ship_name': selected_voyage['ship'],
            'itinerary': selected_voyage['itinry'],
            'passenger_count': selected_voyage['q_psgrs']
        }
        
        return passenger_data
    
    def display_output(self, passenger_data):
        """Display output in the exact format requested"""
        print("\n" + "="*60)
        print("GENERATED PASSENGER DATA")
        print("="*60)
        
        print(f"\nInput Criteria:")
        print(f"Gender: {passenger_data['gender']}")
        print(f"Age: {passenger_data['age']}")
        if passenger_data['has_occupation']:
            print(f"Occupation Group: {passenger_data['occupation_group']}")
        else:
            print(f"Family Role: {passenger_data['family_role']}")
        print(f"Year of Travel: {passenger_data['travel_year']}")
        print(f"Country of Origin: {passenger_data['country_of_origin']}")
        
        print(f"\nOutput:")
        print(f"1. Ship Name: {passenger_data['ship_name']}")
        print(f"2. Itinerary: {passenger_data['itinerary']}")
        print(f"3. Passenger Count: {passenger_data['passenger_count']}")
        print("="*60)

def main():
    """Main function"""
    generator = PassengerGenerator()
    
    try:
        # Get user input
        criteria = generator.get_user_input()
        
        # Generate passenger data
        passenger_data = generator.generate_passenger_data(**criteria)
        
        # Display results
        generator.display_output(passenger_data)
        
        # Ask if user wants to generate another passenger
        while True:
            another = input("\nGenerate another passenger? (y/n): ").strip().lower()
            if another in ['y', 'yes']:
                main()  # Recursive call
                return
            elif another in ['n', 'no']:
                print("\nThank you for using the Passenger Data Generator!")
                return
            else:
                print("Please enter 'y' for yes or 'n' for no")
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please try again.")

if __name__ == "__main__":
    main()