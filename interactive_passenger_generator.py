#!/usr/bin/env python3
"""
Interactive Passenger Data Generator
==================================

An interactive version of the passenger generator that allows users to input
their criteria and get immediate results.
"""

from passenger_generator import PassengerGenerator
import sys

def get_user_input():
    """Get user input for passenger generation"""
    print("\n" + "="*60)
    print("PASSENGER DATA GENERATOR")
    print("="*60)
    
    # Initialize generator
    generator = PassengerGenerator()
    
    # Show available options
    print("\nAvailable Options:")
    print(f"Years: {min(generator.get_available_years())} - {max(generator.get_available_years())}")
    print(f"Countries: {len(generator.get_available_countries())} available")
    print(f"Occupation Groups: {len(generator.occupation_groups)} categories")
    
    try:
        # Get gender
        while True:
            gender = input("\nEnter gender (M/F): ").strip().upper()
            if gender in ['M', 'F']:
                break
            print("Please enter 'M' for male or 'F' for female.")
        
        # Get age
        while True:
            try:
                age = int(input("Enter age (0-100): "))
                if 0 <= age <= 100:
                    break
                print("Age must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get occupation status
        while True:
            has_occupation = input("Does this person have an occupation? (y/n): ").strip().lower()
            if has_occupation in ['y', 'yes']:
                has_occupation = True
                break
            elif has_occupation in ['n', 'no']:
                has_occupation = False
                break
            print("Please enter 'y' for yes or 'n' for no.")
        
        # Get year of travel
        available_years = generator.get_available_years()
        print(f"\nAvailable years: {min(available_years)} - {max(available_years)}")
        while True:
            try:
                arv_yr = int(input("Enter year of travel: "))
                if arv_yr in available_years:
                    break
                print(f"Year must be between {min(available_years)} and {max(available_years)}.")
            except ValueError:
                print("Please enter a valid year.")
        
        # Get country of origin
        available_countries = generator.get_available_countries()
        print(f"\nAvailable countries (showing first 20):")
        for i, country in enumerate(available_countries[:20], 1):
            print(f"{i:2d}. {country}")
        if len(available_countries) > 20:
            print(f"... and {len(available_countries) - 20} more")
        
        while True:
            country_of_origin = input("Enter country of origin: ").strip()
            if country_of_origin in available_countries:
                break
            print(f"Country '{country_of_origin}' not found. Please enter a valid country from the list.")
        
        return {
            'gender': gender,
            'age': age,
            'has_occupation': has_occupation,
            'arv_yr': arv_yr,
            'country_of_origin': country_of_origin
        }
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

def main():
    """Main interactive function"""
    print("Interactive Trans-Atlantic Voyagers Passenger Data Generator")
    print("="*70)
    
    while True:
        try:
            # Get user input
            user_input = get_user_input()
            
            # Generate passenger data
            generator = PassengerGenerator()
            passenger_data = generator.generate_passenger_data(**user_input)
            
            # Display results
            generator.print_passenger_summary(passenger_data)
            
            # Ask if user wants to generate another passenger
            while True:
                another = input("\nGenerate another passenger? (y/n): ").strip().lower()
                if another in ['y', 'yes']:
                    break
                elif another in ['n', 'no']:
                    print("\nThank you for using the Passenger Data Generator!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                    
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()