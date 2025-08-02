# Passenger Data Generator for Trans-Atlantic Voyagers

This system generates realistic passenger data based on the Trans-Atlantic Voyagers dataset (1834-1897). It takes input criteria and generates appropriate ship names, itineraries, and passenger counts.

## Features

### Input Criteria
1. **Gender** (M/F)
2. **Age** (0-100)
3. **Occupation Status** 
   - If yes: Selects appropriate occupation category (`occ_grp`)
   - If no: Selects appropriate family relation
4. **Year of Travel** (`arv_yr`)
5. **Country of Origin**

### Output Data
1. **Ship Name** - Real ship from the dataset
2. **Itinerary** - Actual route taken
3. **Number of Passengers** (`q_psgrs`) - Actual passenger count for that voyage

## Age-Appropriate Logic

The system ensures age-appropriate selections:

### Occupation Categories by Age
- **Children (0-12)**: No occupation only
- **Teens (13-17)**: No occupation, Manufacturing, Service
- **Young Adults (18-25)**: No occupation, Manufacturing, Service, Trade, Agriculture
- **Adults (26-65)**: All categories available
- **Elderly (66+)**: Limited categories

### Family Roles by Age
- **Children (0-12)**: Child, Son, Daughter, Infant
- **Teens (13-17)**: Child, Son, Daughter, Student
- **Young Adults (18-25)**: Head, Son, Daughter, Student, Servant
- **Adults (26-65)**: Head, Wife, Husband, Son, Daughter, Servant, Relative
- **Elderly (66+)**: Head, Wife, Husband, Relative

## Usage

### 1. Interactive Mode
```bash
python interactive_passenger_generator.py
```
This provides a step-by-step interface for entering criteria.

### 2. Command Line Interface
```bash
# Generate a specific passenger
python cli_passenger_generator.py --gender M --age 25 --has-occupation --year 1890 --country "Russia"

# Generate a family member (no occupation)
python cli_passenger_generator.py --gender F --age 8 --no-occupation --year 1885 --country "Poland"

# Generate multiple random passengers
python cli_passenger_generator.py --random 5

# Show available options
python cli_passenger_generator.py --show-options

# Output in JSON format
python cli_passenger_generator.py --gender M --age 30 --has-occupation --year 1880 --country "Germany" --json
```

### 3. Programmatic Use
```python
from passenger_generator import PassengerGenerator

# Initialize generator
generator = PassengerGenerator()

# Generate passenger data
passenger_data = generator.generate_passenger_data(
    gender='M',
    age=25,
    has_occupation=True,
    arv_yr=1890,
    country_of_origin='Russia'
)

# Access the data
print(f"Ship: {passenger_data['ship_name']}")
print(f"Itinerary: {passenger_data['itinerary']}")
print(f"Passengers: {passenger_data['q_psgrs']}")
```

## Available Data

### Years
- **Range**: 1849-1897
- **Total**: 49 years of data

### Countries
- **Total**: 100+ countries of origin
- Includes: Russia, Poland, Germany, Austria, Hungary, etc.

### Occupation Groups
- **Total**: 15+ categories
- Includes: Manufacturing and mining, Trade and commerce, Agriculture, Government, Education, Arts, etc.

### Ships
- **Total**: 783 unique ships
- Examples: VIRGINIA, STEINHOEFT, HERMANN, WISCONSIN, etc.

### Itineraries
- **Total**: 152 unique routes
- Examples: Hamburg-New York, Bremen-New York, Glasgow-New York, etc.

## Example Output

```
============================================================
GENERATED PASSENGER DATA
============================================================
Gender: M
Age: 25
Has Occupation: True
Occupation Group: Manufacturing and mining
Year of Travel: 1890
Country of Origin: Russia

----------------------------------------
VOYAGE DETAILS
----------------------------------------
Ship Name: VIRGINIA
Itinerary: Hamburg-New York
Number of Passengers: 356
Port of Arrival: New York
Voyage ID: 42057
============================================================
```

## Data Validation

The system includes comprehensive validation:

- **Age**: Must be 0-100
- **Gender**: Must be M or F
- **Year**: Must exist in dataset (1849-1897)
- **Country**: Must exist in dataset
- **Occupation**: Age-appropriate categories only
- **Family Role**: Age-appropriate roles only

## Error Handling

The system provides clear error messages for:
- Invalid input values
- Missing required parameters
- Data not found in dataset
- Age-inappropriate selections

## Dependencies

- pandas
- numpy
- random (built-in)
- datetime (built-in)

## Data Sources

All data is sourced from the Trans-Atlantic Voyagers dataset:
- `ttav_passengers.csv` - Main passenger records
- `ttav_occupations.csv` - Occupation categories
- `ttav_voyages.csv` - Voyage information
- `ttav_ships.csv` - Ship details
- `ttav_routes.csv` - Route information

## Files

- `passenger_generator.py` - Core generator class
- `interactive_passenger_generator.py` - Interactive interface
- `cli_passenger_generator.py` - Command-line interface
- `README_PASSENGER_GENERATOR.md` - This documentation