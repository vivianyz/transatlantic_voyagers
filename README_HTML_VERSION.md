# Trans-Atlantic Voyagers Passenger Generator - HTML Web Application

## Overview

This is a complete HTML web application for the Trans-Atlantic Voyagers Passenger Data Generator. It provides a modern, user-friendly interface for generating realistic passenger data based on the historical dataset (1834-1897).

## Features

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient backgrounds and smooth animations
- **Real-time Validation**: Instant feedback on form inputs
- **Loading States**: Visual feedback during data generation

### 📊 Live Statistics
- **Dataset Statistics**: Shows total passengers, ships, years, and countries
- **Real-time Updates**: Statistics load automatically from the backend

### 🚀 Multiple Generation Options
- **Specific Passenger**: Generate based on exact criteria
- **Random Passenger**: Generate completely random passenger data
- **Form Auto-fill**: Random generation fills the form with the generated data

### ✅ Comprehensive Validation
- **Client-side Validation**: Immediate feedback on form errors
- **Server-side Validation**: Backend validation for data integrity
- **Age-appropriate Logic**: Ensures realistic occupation and family role selections

## Files

### Core Application Files
- **`web_passenger_generator.py`** - Flask web server with API endpoints
- **`templates/passenger_generator.html`** - Main HTML interface
- **`passenger_generator.html`** - Standalone HTML version (client-side only)

### Backend Integration
- **`passenger_generator.py`** - Core generator class
- **`dataverse_files/`** - Dataset files (CSV format)

## Usage

### 1. Web Application (Recommended)

Start the Flask web server:
```bash
python3 web_passenger_generator.py
```

Then open your browser to: **http://localhost:5000**

### 2. Standalone HTML Version

Open `passenger_generator.html` directly in your browser for a client-side only version.

## API Endpoints

The web application provides several REST API endpoints:

### GET `/api/options`
Returns available data options:
```json
{
  "years": [1834, 1835, ..., 1897],
  "countries": ["POLAND", "RUSSIA", ...],
  "occupationGroups": ["Manufacturing and mining", ...]
}
```

### POST `/api/generate`
Generate passenger data based on criteria:
```json
{
  "gender": "M",
  "age": 25,
  "hasOccupation": true,
  "year": 1890,
  "country": "POLAND"
}
```

Response:
```json
{
  "gender": "M",
  "age": 25,
  "has_occupation": true,
  "occupation_group": "Trade and commerce",
  "family_role": null,
  "arv_yr": 1890,
  "country_of_origin": "POLAND",
  "ship_name": "ANCHORIA",
  "itinerary": "Glasgow & Moville-New York",
  "q_psgrs": 50,
  "port_arrival": "New York",
  "voyage_id": 81674
}
```

### POST `/api/random`
Generate a completely random passenger:
```json
{
  "gender": "F",
  "age": 32,
  "has_occupation": false,
  "family_role": "Wife",
  "arv_yr": 1885,
  "country_of_origin": "RUSSIA",
  "ship_name": "WISCONSIN",
  "itinerary": "Hamburg-New York",
  "q_psgrs": 356,
  "port_arrival": "New York",
  "voyage_id": 42057
}
```

## User Interface Features

### 📝 Form Inputs
- **Gender**: Dropdown selection (M/F)
- **Age**: Number input with validation (0-100)
- **Year of Travel**: Number input with validation (1834-1897)
- **Country of Origin**: Text input with validation
- **Occupation Status**: Radio buttons for occupation vs. family role

### 🎯 Action Buttons
- **Generate Passenger Data**: Creates passenger based on form inputs
- **Generate Random Passenger**: Creates random passenger and fills form
- **Clear Form**: Resets all form fields

### 📊 Results Display
- **Success Status**: Visual confirmation of successful generation
- **Passenger Details**: All input and generated data
- **Voyage Information**: Ship name, itinerary, passenger count, etc.
- **Error Handling**: Clear error messages for validation failures

## Technical Features

### Frontend (HTML/CSS/JavaScript)
- **Responsive CSS Grid**: Adapts to different screen sizes
- **Modern CSS**: Gradients, shadows, animations
- **Vanilla JavaScript**: No external dependencies
- **Async/Await**: Modern JavaScript for API calls
- **Error Handling**: Comprehensive client-side error management

### Backend (Flask/Python)
- **RESTful API**: Clean API design
- **JSON Serialization**: Proper handling of numpy types
- **Error Handling**: Comprehensive server-side validation
- **CORS Support**: Ready for cross-origin requests

### Data Integration
- **Real Dataset**: Uses actual Trans-Atlantic Voyagers data
- **Age-appropriate Logic**: Ensures realistic data generation
- **Validation**: Both client and server-side validation

## Installation & Setup

### Prerequisites
```bash
sudo apt install python3-flask python3-pandas python3-numpy
```

### Data Files
Ensure the following files are present in `dataverse_files/`:
- `ttav_passengers.csv`
- `ttav_occupations.csv`
- `ttav_voyages.csv`
- `ttav_ships.csv`
- `ttav_routes.csv`

### Running the Application
```bash
# Start the web server
python3 web_passenger_generator.py

# Open browser to
# http://localhost:5000
```

## Example Usage

### 1. Generate Specific Passenger
1. Fill in the form with desired criteria
2. Click "Generate Passenger Data"
3. View the generated passenger information

### 2. Generate Random Passenger
1. Click "Generate Random Passenger"
2. Form will be auto-filled with random data
3. View the generated passenger information

### 3. API Usage
```bash
# Get available options
curl http://localhost:5000/api/options

# Generate specific passenger
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"gender":"M","age":25,"hasOccupation":true,"year":1890,"country":"POLAND"}'

# Generate random passenger
curl -X POST http://localhost:5000/api/random
```

## Browser Compatibility

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## Performance

- **Fast Loading**: Optimized CSS and JavaScript
- **Efficient API**: Minimal server response times
- **Responsive**: Works smoothly on all devices
- **Scalable**: Can handle multiple concurrent users

## Security Features

- **Input Validation**: Both client and server-side validation
- **Error Handling**: Graceful error management
- **Data Sanitization**: Proper handling of user inputs

## Future Enhancements

- **Export Options**: Download results as CSV/JSON
- **Batch Generation**: Generate multiple passengers at once
- **Advanced Filters**: Filter by ship, year range, etc.
- **Data Visualization**: Charts and graphs of generated data
- **User Accounts**: Save favorite configurations

## Troubleshooting

### Common Issues

1. **Server won't start**: Check if port 5000 is available
2. **Data not loading**: Ensure CSV files are in `dataverse_files/`
3. **API errors**: Check browser console for detailed error messages
4. **Validation errors**: Review form inputs and try again

### Debug Mode
The Flask app runs in debug mode by default, providing detailed error messages.

## Conclusion

The HTML web application provides a complete, user-friendly interface for the Trans-Atlantic Voyagers Passenger Generator. It combines the power of the Python backend with the accessibility of a modern web interface, making it easy for users to generate realistic historical passenger data.