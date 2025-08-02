#!/usr/bin/env python3
"""
Demonstration Script for Passenger Data Generator
================================================

This script demonstrates various ways to use the passenger generator system.
"""

from passenger_generator import PassengerGenerator
import json

def demo_basic_usage():
    """Demonstrate basic usage of the passenger generator"""
    print("="*60)
    print("DEMONSTRATION: Basic Usage")
    print("="*60)
    
    # Initialize the generator
    generator = PassengerGenerator()
    
    # Example 1: Generate a working adult male
    print("\n1. Working Adult Male (Age 30, Has Occupation)")
    passenger1 = generator.generate_passenger_data(
        gender='M',
        age=30,
        has_occupation=True,
        arv_yr=1890,
        country_of_origin='POLAND'
    )
    generator.print_passenger_summary(passenger1)
    
    # Example 2: Generate a child (no occupation)
    print("\n2. Child (Age 8, No Occupation)")
    passenger2 = generator.generate_passenger_data(
        gender='F',
        age=8,
        has_occupation=False,
        arv_yr=1885,
        country_of_origin='POLAND'
    )
    generator.print_passenger_summary(passenger2)
    
    # Example 3: Generate an elderly person
    print("\n3. Elderly Person (Age 70, Has Occupation)")
    passenger3 = generator.generate_passenger_data(
        gender='M',
        age=70,
        has_occupation=True,
        arv_yr=1880,
        country_of_origin='POLAND'
    )
    generator.print_passenger_summary(passenger3)

def demo_age_appropriate_logic():
    """Demonstrate age-appropriate occupation and family role logic"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Age-Appropriate Logic")
    print("="*60)
    
    generator = PassengerGenerator()
    
    # Test different ages to show age-appropriate selections
    test_cases = [
        (5, 'M', True, 1890, 'POLAND'),   # Child with occupation (should default to No occupation)
        (15, 'F', True, 1890, 'POLAND'),  # Teen with occupation
        (22, 'M', False, 1890, 'POLAND'), # Young adult without occupation
        (35, 'F', True, 1890, 'POLAND'),  # Adult with occupation
        (75, 'M', False, 1890, 'POLAND'), # Elderly without occupation
    ]
    
    for i, (age, gender, has_occupation, year, country) in enumerate(test_cases, 1):
        print(f"\n{i}. Age {age}, Gender {gender}, Has Occupation: {has_occupation}")
        try:
            passenger = generator.generate_passenger_data(
                gender=gender,
                age=age,
                has_occupation=has_occupation,
                arv_yr=year,
                country_of_origin=country
            )
            
            if has_occupation:
                print(f"   Occupation Group: {passenger['occupation_group']}")
            else:
                print(f"   Family Role: {passenger['family_role']}")
            print(f"   Ship: {passenger['ship_name']}")
            print(f"   Itinerary: {passenger['itinerary']}")
            print(f"   Passengers: {passenger['q_psgrs']}")
            
        except Exception as e:
            print(f"   Error: {e}")

def demo_json_output():
    """Demonstrate JSON output format"""
    print("\n" + "="*60)
    print("DEMONSTRATION: JSON Output Format")
    print("="*60)
    
    generator = PassengerGenerator()
    
    # Generate passenger data
    passenger = generator.generate_passenger_data(
        gender='M',
        age=25,
        has_occupation=True,
        arv_yr=1890,
        country_of_origin='POLAND'
    )
    
    # Convert to JSON-serializable format
    json_data = {}
    for key, value in passenger.items():
        if hasattr(value, 'item'):  # numpy type
            json_data[key] = value.item()
        else:
            json_data[key] = value
    
    print("JSON Output:")
    print(json.dumps(json_data, indent=2))

def demo_available_data():
    """Show available data options"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Available Data")
    print("="*60)
    
    generator = PassengerGenerator()
    
    # Show available years
    years = generator.get_available_years()
    print(f"Available Years: {len(years)} years")
    print(f"Range: {min(years)} - {max(years)}")
    print(f"Sample years: {years[:10]}")
    
    # Show available countries (first 20)
    countries = generator.get_available_countries()
    print(f"\nAvailable Countries: {len(countries)} countries")
    print("Sample countries:")
    for country in countries[:20]:
        print(f"  - {country}")
    
    # Show occupation groups
    print(f"\nOccupation Groups: {len(generator.occupation_groups)} categories")
    print("All groups:")
    for group in generator.occupation_groups:
        print(f"  - {group}")

def demo_error_handling():
    """Demonstrate error handling"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Error Handling")
    print("="*60)
    
    generator = PassengerGenerator()
    
    # Test invalid inputs
    test_cases = [
        ("Invalid gender", {'gender': 'X', 'age': 25, 'has_occupation': True, 'arv_yr': 1890, 'country_of_origin': 'POLAND'}),
        ("Invalid age", {'gender': 'M', 'age': 150, 'has_occupation': True, 'arv_yr': 1890, 'country_of_origin': 'POLAND'}),
        ("Invalid year", {'gender': 'M', 'age': 25, 'has_occupation': True, 'arv_yr': 2000, 'country_of_origin': 'POLAND'}),
        ("Invalid country", {'gender': 'M', 'age': 25, 'has_occupation': True, 'arv_yr': 1890, 'country_of_origin': 'INVALID_COUNTRY'}),
    ]
    
    for description, params in test_cases:
        print(f"\n{description}:")
        try:
            passenger = generator.generate_passenger_data(**params)
            print("  SUCCESS (unexpected)")
        except Exception as e:
            print(f"  ERROR: {e}")

def main():
    """Run all demonstrations"""
    print("Passenger Data Generator - Demonstration Script")
    print("="*60)
    
    # Run demonstrations
    demo_basic_usage()
    demo_age_appropriate_logic()
    demo_json_output()
    demo_available_data()
    demo_error_handling()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nTo use the system:")
    print("1. Interactive mode: python3 interactive_passenger_generator.py")
    print("2. Command line: python3 cli_passenger_generator.py --help")
    print("3. Programmatic: from passenger_generator import PassengerGenerator")

if __name__ == "__main__":
    main()