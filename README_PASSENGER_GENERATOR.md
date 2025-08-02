# Passenger Data Generator

This tool generates passenger data based on the Tsar's Trans-Atlantic Voyagers dataset, allowing you to create realistic passenger records with specific criteria.

## Files Included

1. **`passenger_generator_final.py`** - The main interactive generator (recommended)
2. **`working_passenger_generator.py`** - Working version with sample data
3. **`simple_passenger_generator.py`** - Simplified version (uses CSV files)
4. **`passenger_generator.py`** - Full version with pandas (requires dependencies)

## How to Use

### Quick Start
```bash
python3 passenger_generator_final.py
```

### Input Criteria

The generator asks for the following information:

1. **Gender** (M/F) - Male or Female
2. **Age** (0-120) - Age of the passenger
3. **Occupation Status** (y/n) - Whether the character works
   - If **yes**: Select an occupation group from the list
   - If **no**: Select a family role from the list
4. **Year of Travel** (1849-1892) - Year the passenger traveled
5. **Country of Origin** - Select from available countries

### Output

The generator provides:

1. **Ship Name** - The name of the ship the passenger traveled on
2. **Itinerary** - The route taken (e.g., "Hamburg-New York")
3. **Passenger Count** - Number of passengers on that voyage

## Example Usage

```
============================================================
PASSENGER DATA GENERATOR
============================================================
1. Gender (M/F): M
2. Age: 25
3. Does this character work? (y/n): y

Available occupation groups:
 1. Agriculture
 2. Manufacturing and mining
 3. Trade and commerce
 4. Service and hospitality
 5. Transportation and communication
 6. Construction
 7. Production of food and drink
 8. Leather, textiles, garments
 9. Printing and journalism
10. Education, sciences
11. Arts, entertainment, sports
12. Government
13. Faith-related
14. Estate and household labor
15. No occupation

Select occupation group (enter number): 2

4. Year of travel (1849-1892): 1880

Available countries of origin:
 1. Russia
 2. Poland
 3. Ukraine
 4. Belarus
 5. Finland
 6. Germany
 7. Austria
 8. Hungary
 9. Romania
10. Bulgaria
11. Serbia
12. Croatia
13. Slovenia
14. Slovakia
15. Czech Republic
16. Lithuania
17. Latvia
18. Estonia
19. Moldova
20. Georgia
21. Armenia
22. Azerbaijan

Select country of origin (enter number): 1

============================================================
GENERATED PASSENGER DATA
============================================================

Input Criteria:
Gender: M
Age: 25
Occupation Group: Manufacturing and mining
Year of Travel: 1880
Country of Origin: Russia

Output:
1. Ship Name: HERMANN
2. Itinerary: Hamburg-New York
3. Passenger Count: 24
============================================================
```

## Features

- **Age Validation**: Ensures age is appropriate for occupation or family role
- **Historical Accuracy**: Uses real ship names and routes from the 19th century
- **Flexible Input**: Can handle various passenger types (workers, family members)
- **Interactive Interface**: Easy-to-use command-line interface
- **Multiple Voyages**: Randomly selects from available voyages for the specified year

## Data Sources

The generator uses sample data from the Tsar's Trans-Atlantic Voyagers dataset, including:
- Real ship names (HERMANN, VIRGINIA, STEINHOEFT, etc.)
- Historical routes (Hamburg-New York, Bremen-New York, Havre-New York)
- Actual passenger counts from voyages
- Realistic occupation groups and family roles

## Requirements

- Python 3.x
- No external dependencies required (uses only standard library)

## Troubleshooting

If you encounter issues:
1. Make sure you're using Python 3
2. Check that all input values are within the specified ranges
3. The generator will automatically find the closest available year if your specified year doesn't have voyages

## Files Description

- **`passenger_generator_final.py`**: Complete interactive version with all features
- **`working_passenger_generator.py`**: Demonstrates the functionality with sample data
- **`simple_passenger_generator.py`**: Attempts to read from CSV files (may have issues)
- **`passenger_generator.py`**: Full version requiring pandas (not recommended for basic use)