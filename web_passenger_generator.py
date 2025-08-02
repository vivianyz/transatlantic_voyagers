#!/usr/bin/env python3
"""
Flask Web Application for Passenger Data Generator
================================================

This Flask app provides a web interface for the passenger generator system.
"""

from flask import Flask, render_template, request, jsonify
from passenger_generator import PassengerGenerator
import json

app = Flask(__name__)

# Initialize the passenger generator
generator = None

def initialize_generator():
    """Initialize the passenger generator"""
    global generator
    try:
        generator = PassengerGenerator()
        return True
    except Exception as e:
        print(f"Error initializing generator: {e}")
        return False

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('passenger_generator.html')

@app.route('/api/generate', methods=['POST'])
def generate_passenger():
    """API endpoint to generate passenger data"""
    try:
        data = request.get_json()
        
        if not generator:
            return jsonify({'error': 'Generator not initialized'}), 500
        
        # Extract form data
        gender = data.get('gender')
        age = data.get('age')
        has_occupation = data.get('hasOccupation')
        arv_yr = data.get('year')
        country_of_origin = data.get('country')
        
        # Validate required fields
        if not all([gender, age is not None, has_occupation is not None, arv_yr, country_of_origin]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Generate passenger data
        passenger_data = generator.generate_passenger_data(
            gender=gender,
            age=age,
            has_occupation=has_occupation,
            arv_yr=arv_yr,
            country_of_origin=country_of_origin
        )
        
        # Convert numpy types to native Python types for JSON serialization
        json_data = {}
        for key, value in passenger_data.items():
            if hasattr(value, 'item'):  # numpy type
                json_data[key] = value.item()
            else:
                json_data[key] = value
        
        return jsonify(json_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/random', methods=['POST'])
def generate_random_passenger():
    """API endpoint to generate random passenger data"""
    try:
        if not generator:
            return jsonify({'error': 'Generator not initialized'}), 500
        
        # Generate random passenger
        passengers = generator.generate_multiple_passengers(1)
        if passengers:
            passenger_data = passengers[0]
            
            # Convert numpy types to native Python types for JSON serialization
            json_data = {}
            for key, value in passenger_data.items():
                if hasattr(value, 'item'):  # numpy type
                    json_data[key] = value.item()
                else:
                    json_data[key] = value
            
            return jsonify(json_data)
        else:
            return jsonify({'error': 'Failed to generate random passenger'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/options', methods=['GET'])
def get_available_options():
    """API endpoint to get available options"""
    try:
        if not generator:
            return jsonify({'error': 'Generator not initialized'}), 500
        
        # Convert numpy types to native Python types for JSON serialization
        years = [int(year) for year in generator.get_available_years()]
        countries = generator.get_available_countries()[:50]  # Limit to first 50
        occupation_groups = generator.occupation_groups
        
        return jsonify({
            'years': years,
            'countries': countries,
            'occupationGroups': occupation_groups
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def validate_input():
    """API endpoint to validate input data"""
    try:
        data = request.get_json()
        
        if not generator:
            return jsonify({'error': 'Generator not initialized'}), 500
        
        # Extract form data
        gender = data.get('gender')
        age = data.get('age')
        has_occupation = data.get('hasOccupation')
        arv_yr = data.get('year')
        country_of_origin = data.get('country')
        
        errors = []
        
        # Validate gender
        if not gender or gender not in ['M', 'F']:
            errors.append('Gender must be M or F')
        
        # Validate age
        if age is None or age < 0 or age > 100:
            errors.append('Age must be between 0 and 100')
        
        # Validate year
        available_years = generator.get_available_years()
        if arv_yr not in available_years:
            errors.append(f'Year must be between {min(available_years)} and {max(available_years)}')
        
        # Validate country
        available_countries = generator.get_available_countries()
        if country_of_origin not in available_countries:
            errors.append(f'Country "{country_of_origin}" not found in dataset')
        
        # Validate occupation status
        if has_occupation is None:
            errors.append('Occupation status is required')
        
        return jsonify({
            'valid': len(errors) == 0,
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Initializing Passenger Generator...")
    if initialize_generator():
        print("✅ Generator initialized successfully")
        print("🌐 Starting Flask web server...")
        print("📱 Open your browser to: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize generator")
        exit(1)