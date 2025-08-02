#!/usr/bin/env python3
"""
Interactive Passenger Data Generator
==================================

This script provides an interactive interface for generating passenger data
based on user input criteria.
"""

from passenger_generator import PassengerGenerator
import sys

def get_user_input():
    """Get input criteria from the user"""
    print("\n" + "="*60)
    print("PASSENGER DATA GENERATOR")
    print("="*60)
    print("Please provide the following information:")
    
    # 1. Gender
    while True:
        gender = input("\n1. Gender (M/F): ").strip().upper()
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
        generator = PassengerGenerator()
        for i, group in enumerate(generator.occupation_groups, 1):
            print(f"{i:2d}. {group}")
        
        while True:
            try:
                choice = int(input("\nSelect occupation group (enter number): "))
                if 1 <= choice <= len(generator.occupation_groups):
                    occupation_group = generator.occupation_groups[choice - 1]
                    family_role = None
                    break
                print(f"Please enter a number between 1 and {len(generator.occupation_groups)}")
            except ValueError:
                print("Please enter a valid number")
    else:
        print("\nAvailable family roles:")
        generator = PassengerGenerator()
        for i, role in enumerate(generator.family_roles, 1):
            print(f"{i:2d}. {role}")
        
        while True:
            try:
                choice = int(input("\nSelect family role (enter number): "))
                if 1 <= choice <= len(generator.family_roles):
                    family_role = generator.family_roles[choice - 1]
                    occupation_group = None
                    break
                print(f"Please enter a number between 1 and {len(generator.family_roles)}")
            except ValueError:
                print("Please enter a valid number")
    
    # 5. Year of travel
    while True:
        try:
            travel_year = int(input("\n4. Year of travel (1834-1897): "))
            if 1834 <= travel_year <= 1897:
                break
            print("Please enter a year between 1834 and 1897")
        except ValueError:
            print("Please enter a valid year")
    
    # 6. Country of origin
    print("\nAvailable countries of origin:")
    generator = PassengerGenerator()
    for i, country in enumerate(generator.countries, 1):
        print(f"{i:2d}. {country}")
    
    while True:
        try:
            choice = int(input("\nSelect country of origin (enter number): "))
            if 1 <= choice <= len(generator.countries):
                country_of_origin = generator.countries[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(generator.countries)}")
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

def main():
    """Main interactive function"""
    try:
        # Get user input
        criteria = get_user_input()
        
        # Generate passenger data
        generator = PassengerGenerator()
        passenger_data = generator.generate_passenger_data(**criteria)
        
        # Display results
        print("\n" + "="*60)
        print("GENERATED PASSENGER DATA")
        print("="*60)
        
        print(f"\nInput Criteria:")
        print(f"Gender: {criteria['gender']}")
        print(f"Age: {criteria['age']}")
        if criteria['has_occupation']:
            print(f"Occupation Group: {criteria['occupation_group']}")
        else:
            print(f"Family Role: {criteria['family_role']}")
        print(f"Year of Travel: {criteria['travel_year']}")
        print(f"Country of Origin: {criteria['country_of_origin']}")
        
        print(f"\nOutput Data:")
        print(f"1. Ship Name: {passenger_data['ship_name']}")
        print(f"2. Itinerary: {passenger_data['itinerary']}")
        print(f"3. Passenger Count (q_psgrs): {passenger_data['passenger_count']}")
        
        print(f"\nAdditional Information:")
        print(f"Arrival Port: {passenger_data['arrival_port']}")
        print(f"Voyage ID: {passenger_data['voyage_id']}")
        
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
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("Please try again.")

if __name__ == "__main__":
    main()