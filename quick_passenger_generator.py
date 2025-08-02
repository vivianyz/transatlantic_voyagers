#!/usr/bin/env python3
"""
Quick Passenger Data Generator
=============================

A simple command-line tool for quickly generating passenger data.
Usage: python quick_passenger_generator.py [gender] [age] [has_occupation] [travel_year] [country]
"""

from passenger_generator import PassengerGenerator
import sys
import random

def quick_generate(gender=None, age=None, has_occupation=None, travel_year=None, country=None):
    """Quickly generate passenger data with minimal input"""
    generator = PassengerGenerator()
    
    # Set defaults for missing parameters
    if gender is None:
        gender = random.choice(['M', 'F'])
    if age is None:
        age = random.randint(1, 80)
    if has_occupation is None:
        has_occupation = random.choice([True, False])
    if travel_year is None:
        travel_year = random.choice(generator.voyages_full['arv_yr'].unique())
    if country is None:
        country = random.choice(generator.countries)
    
    # Generate passenger data
    passenger_data = generator.generate_passenger_data(
        gender=gender,
        age=age,
        has_occupation=has_occupation,
        travel_year=travel_year,
        country_of_origin=country
    )
    
    return passenger_data

def main():
    """Main function for command-line usage"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("""
Quick Passenger Data Generator
============================

Usage: python quick_passenger_generator.py [gender] [age] [has_occupation] [travel_year] [country]

Parameters:
  gender         M or F (optional)
  age           Age in years (optional)
  has_occupation y or n (optional)
  travel_year   Year between 1834-1897 (optional)
  country       Country of origin (optional)

Examples:
  python quick_passenger_generator.py
  python quick_passenger_generator.py M 25 y 1880 Russia
  python quick_passenger_generator.py F 8 n 1890 Poland
        """)
        return
    
    # Parse command line arguments
    gender = None
    age = None
    has_occupation = None
    travel_year = None
    country = None
    
    if len(sys.argv) > 1:
        gender = sys.argv[1].upper()
    if len(sys.argv) > 2:
        try:
            age = int(sys.argv[2])
        except ValueError:
            print("Error: Age must be a number")
            return
    if len(sys.argv) > 3:
        has_occupation = sys.argv[3].lower() in ['y', 'yes', 'true']
    if len(sys.argv) > 4:
        try:
            travel_year = int(sys.argv[4])
        except ValueError:
            print("Error: Travel year must be a number")
            return
    if len(sys.argv) > 5:
        country = sys.argv[5]
    
    try:
        # Generate passenger data
        passenger_data = quick_generate(gender, age, has_occupation, travel_year, country)
        
        # Display results
        print("\n" + "="*50)
        print("GENERATED PASSENGER DATA")
        print("="*50)
        
        print(f"Gender: {passenger_data['gender']}")
        print(f"Age: {passenger_data['age']}")
        
        if passenger_data['has_occupation']:
            print(f"Occupation: {passenger_data['occupation_group']}")
        else:
            print(f"Family Role: {passenger_data['family_role']}")
        
        print(f"Year of Travel: {passenger_data['travel_year']}")
        print(f"Country of Origin: {passenger_data['country_of_origin']}")
        
        print(f"\nOutput:")
        print(f"1. Ship Name: {passenger_data['ship_name']}")
        print(f"2. Itinerary: {passenger_data['itinerary']}")
        print(f"3. Passenger Count: {passenger_data['passenger_count']}")
        
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Try running with --help for usage information")

if __name__ == "__main__":
    main()