#!/usr/bin/env python3
"""
Command-Line Passenger Data Generator
====================================

A command-line interface for the passenger generator that accepts arguments
for automated use and batch processing.
"""

from passenger_generator import PassengerGenerator
import argparse
import json
import sys

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Generate passenger data for Trans-Atlantic Voyagers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a specific passenger
  python cli_passenger_generator.py --gender M --age 25 --has-occupation --year 1890 --country "Russia"
  
  # Generate a family member (no occupation)
  python cli_passenger_generator.py --gender F --age 8 --no-occupation --year 1885 --country "Poland"
  
  # Generate multiple random passengers
  python cli_passenger_generator.py --random 5
  
  # Show available options
  python cli_passenger_generator.py --show-options
        """
    )
    
    # Input parameters
    parser.add_argument('--gender', choices=['M', 'F'], help='Gender (M/F)')
    parser.add_argument('--age', type=int, help='Age (0-100)')
    parser.add_argument('--has-occupation', action='store_true', help='Person has an occupation')
    parser.add_argument('--no-occupation', action='store_true', help='Person has no occupation (family member)')
    parser.add_argument('--year', type=int, help='Year of travel')
    parser.add_argument('--country', help='Country of origin')
    
    # Output options
    parser.add_argument('--random', type=int, help='Generate N random passengers')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--show-options', action='store_true', help='Show available options')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PassengerGenerator()
    
    # Show available options
    if args.show_options:
        print("Available Options:")
        print("="*50)
        
        available_years = generator.get_available_years()
        print(f"Years: {min(available_years)} - {max(available_years)}")
        print(f"Total years: {len(available_years)}")
        
        available_countries = generator.get_available_countries()
        print(f"\nCountries: {len(available_countries)} available")
        print("Sample countries:")
        for country in available_countries[:20]:
            print(f"  - {country}")
        if len(available_countries) > 20:
            print(f"  ... and {len(available_countries) - 20} more")
        
        print(f"\nOccupation Groups: {len(generator.occupation_groups)} categories")
        print("Sample groups:")
        for group in generator.occupation_groups[:10]:
            print(f"  - {group}")
        if len(generator.occupation_groups) > 10:
            print(f"  ... and {len(generator.occupation_groups) - 10} more")
        
        return
    
    # Generate random passengers
    if args.random:
        if args.random < 1:
            print("Error: Number of random passengers must be at least 1")
            sys.exit(1)
        
        passengers = generator.generate_multiple_passengers(args.random)
        
        if args.json:
            print(json.dumps(passengers, indent=2))
        else:
            for i, passenger in enumerate(passengers, 1):
                print(f"\nPassenger {i}:")
                generator.print_passenger_summary(passenger)
        
        return
    
    # Validate required arguments for specific passenger generation
    if not all([args.gender, args.age is not None, args.year, args.country]):
        print("Error: For specific passenger generation, all arguments are required:")
        print("  --gender, --age, --year, --country")
        print("  --has-occupation OR --no-occupation")
        print("\nUse --help for more information or --show-options to see available values.")
        sys.exit(1)
    
    # Validate occupation argument
    if args.has_occupation and args.no_occupation:
        print("Error: Cannot specify both --has-occupation and --no-occupation")
        sys.exit(1)
    
    if not args.has_occupation and not args.no_occupation:
        print("Error: Must specify either --has-occupation or --no-occupation")
        sys.exit(1)
    
    has_occupation = args.has_occupation
    
    # Validate age
    if args.age < 0 or args.age > 100:
        print("Error: Age must be between 0 and 100")
        sys.exit(1)
    
    # Validate year
    available_years = generator.get_available_years()
    if args.year not in available_years:
        print(f"Error: Year {args.year} not available in dataset")
        print(f"Available years: {min(available_years)} - {max(available_years)}")
        sys.exit(1)
    
    # Validate country
    available_countries = generator.get_available_countries()
    if args.country not in available_countries:
        print(f"Error: Country '{args.country}' not found in dataset")
        print("Available countries:")
        for country in available_countries[:20]:
            print(f"  - {country}")
        if len(available_countries) > 20:
            print(f"  ... and {len(available_countries) - 20} more")
        sys.exit(1)
    
    # Generate passenger data
    try:
        passenger_data = generator.generate_passenger_data(
            gender=args.gender,
            age=args.age,
            has_occupation=has_occupation,
            arv_yr=args.year,
            country_of_origin=args.country
        )
        
        if args.json:
            # Convert numpy types to native Python types for JSON serialization
            json_data = {}
            for key, value in passenger_data.items():
                if hasattr(value, 'item'):  # numpy type
                    json_data[key] = value.item()
                else:
                    json_data[key] = value
            print(json.dumps(json_data, indent=2))
        else:
            generator.print_passenger_summary(passenger_data)
            
    except Exception as e:
        print(f"Error generating passenger data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()