#!/usr/bin/env python3
"""
Trans-Atlantic Voyagers Web Application Backend
==============================================

Flask web server that provides a REST API for passenger predictions.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

class PassengerPredictionModel:
    def __init__(self):
        self.data = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.prediction_models = {}
        self.occupation_lookup = {}
        self.residence_lookup = {}
        self.is_loaded = False
        
    def load_model(self):
        """Load and prepare the prediction model"""
        if self.is_loaded:
            return True
            
        try:
            print("🔄 Loading prediction model...")
            
            # Load data
            self.data = pd.read_csv('ttav_unified_dataset.csv', low_memory=False)
            
            # Create age ranges
            self.data['age_range'] = pd.cut(self.data['age'], 
                                           bins=[0, 18, 30, 45, 60, 100], 
                                           labels=['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior'])
            
            # Filter for complete cases
            required_cols = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
            self.data = self.data.dropna(subset=required_cols)
            
            # Create lookup tables
            self.create_lookup_tables()
            
            # Train models
            self.train_models()
            
            self.is_loaded = True
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def create_lookup_tables(self):
        """Create lookup tables for occupations and residences"""
        # Occupation lookup
        if 'occ_nm' in self.data.columns:
            occ_data = self.data[['occID', 'occ_nm']].drop_duplicates()
            self.occupation_lookup = dict(zip(occ_data['occID'], occ_data['occ_nm']))
        
        # Residence lookup
        if 'resdn' in self.data.columns:
            res_data = self.data[['lkrID', 'resdn']].drop_duplicates()
            self.residence_lookup = dict(zip(res_data['lkrID'], res_data['resdn']))
    
    def train_models(self):
        """Train prediction models"""
        # Prepare features
        features = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        X = self.data[features].copy()
        
        # Encode categorical variables
        categorical_cols = ['sex', 'age_range']
        for col in categorical_cols:
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoded = encoder.fit_transform(X[[col]])
            encoded_df = pd.DataFrame(encoded, 
                                    columns=[f"{col}_{cat}" for cat in encoder.categories_[0]],
                                    index=X.index)
            X = pd.concat([X.drop(col, axis=1), encoded_df], axis=1)
            self.encoders[col] = encoder
        
        # Scale numerical variables
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        
        # Train models for each target
        targets = ['litr', 'fam_role', 'pasg', 'occ_grp', 'port_arv']
        
        for target in targets:
            if target not in self.data.columns:
                continue
                
            # Get non-null target data
            target_mask = self.data[target].notna()
            X_target = X[target_mask]
            y_target = self.data[target][target_mask]
            
            if len(y_target) < 100:
                continue
            
            # Train model
            model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=8)
            X_train, X_test, y_train, y_test = train_test_split(
                X_target, y_target, test_size=0.2, random_state=42
            )
            model.fit(X_train, y_train)
            
            # Store model
            self.prediction_models[target] = model
    
    def predict(self, input_data):
        """Make predictions for given input"""
        if not self.is_loaded:
            return None
            
        try:
            # Convert to DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Prepare features based on new input structure
            features = ['sex', 'age', 'has_occupation', 'arv_yr', 'country_origin']
            if input_data.get('has_occupation') == 'yes':
                features.append('occ_grp')
            else:
                features.append('fam_role')
            
            X_input = input_df[features].copy()
            
            # Encode categorical variables
            categorical_cols = ['sex', 'has_occupation']
            if 'occ_grp' in X_input.columns:
                categorical_cols.append('occ_grp')
            if 'fam_role' in X_input.columns:
                categorical_cols.append('fam_role')
                
            for col in categorical_cols:
                if col in self.encoders:
                    encoded = self.encoders[col].transform(X_input[[col]])
                    encoded_df = pd.DataFrame(encoded, 
                                            columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                            index=X_input.index)
                    X_input = pd.concat([X_input.drop(col, axis=1), encoded_df], axis=1)
            
            # Scale numerical variables
            numerical_cols = ['age', 'arv_yr']
            X_input[numerical_cols] = self.scaler.transform(X_input[numerical_cols])
            
            # Make predictions for new targets
            predictions = {}
            confidences = {}
            
            # For now, return mock data since we need to train on ship/itinerary/passenger data
            predictions['ship_name'] = 'SS Bremen'
            predictions['itinerary'] = 'Bremen-New York'
            predictions['q_psgrs'] = '150'
            
            confidences['ship_name'] = 0.85
            confidences['itinerary'] = 0.90
            confidences['q_psgrs'] = 0.75
            
            return predictions, confidences
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def get_options(self):
        """Get available input options"""
        if not self.is_loaded:
            return {}
            
        return {
            'genders': [
                {'value': 'M', 'label': 'Male'},
                {'value': 'F', 'label': 'Female'},
                {'value': 'U', 'label': 'Unknown'}
            ],
            'occupation_groups': [
                {'value': 'Professional', 'label': 'Professional'},
                {'value': 'Skilled', 'label': 'Skilled Worker'},
                {'value': 'Unskilled', 'label': 'Unskilled Worker'},
                {'value': 'Agricultural', 'label': 'Agricultural Worker'},
                {'value': 'Service', 'label': 'Service Worker'},
                {'value': 'Merchant', 'label': 'Merchant/Trader'},
                {'value': 'Student', 'label': 'Student'},
                {'value': 'Unknown', 'label': 'Unknown'}
            ],
            'family_roles': [
                {'value': 'Head', 'label': 'Family Head'},
                {'value': 'Spouse', 'label': 'Spouse'},
                {'value': 'Child', 'label': 'Child'},
                {'value': 'Parent', 'label': 'Parent'},
                {'value': 'Sibling', 'label': 'Sibling'},
                {'value': 'Other', 'label': 'Other Family Member'}
            ],
            'countries': [
                {'value': 'Russia', 'label': 'Russia'},
                {'value': 'Germany', 'label': 'Germany'},
                {'value': 'Poland', 'label': 'Poland'},
                {'value': 'Austria', 'label': 'Austria'},
                {'value': 'Hungary', 'label': 'Hungary'},
                {'value': 'Romania', 'label': 'Romania'},
                {'value': 'Ukraine', 'label': 'Ukraine'},
                {'value': 'Belarus', 'label': 'Belarus'},
                {'value': 'Lithuania', 'label': 'Lithuania'},
                {'value': 'Latvia', 'label': 'Latvia'},
                {'value': 'Estonia', 'label': 'Estonia'},
                {'value': 'Finland', 'label': 'Finland'},
                {'value': 'Other', 'label': 'Other'}
            ]
        }

# Initialize model
model = PassengerPredictionModel()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/options')
def get_options():
    """Get available input options"""
    if not model.is_loaded:
        model.load_model()
    
    options = model.get_options()
    return jsonify(options)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make prediction based on input data"""
    try:
        if not model.is_loaded:
            model.load_model()
        
        data = request.json
        
        # Validate required fields
        required_fields = ['sex', 'age', 'has_occupation', 'arv_yr', 'country_origin']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate conditional fields
        if data['has_occupation'] == 'yes' and 'occ_grp' not in data:
            return jsonify({'error': 'Occupation category required when has_occupation is yes'}), 400
        if data['has_occupation'] == 'no' and 'fam_role' not in data:
            return jsonify({'error': 'Family role required when has_occupation is no'}), 400
        
        # Make prediction
        result = model.predict(data)
        if result is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        predictions, confidences = result
        
        # --- Migration Route Logic ---
        # Load routes and ports data
        import csv
        routes = []
        with open('dataverse_files/ttav_routes.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                routes.append(row)
        ports = {}
        with open('dataverse_files/ttav_ports.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ports[row['port']] = {
                    'name': row['port'],
                    'lat': float(row['geonm_lat']),
                    'lon': float(row['geonm_long'])
                }
        # Find the route for the predicted itinerary
        predicted_itinerary = predictions.get('itinerary', 'Unknown')
        route_row = None
        for r in routes:
            if r['itinry'] == predicted_itinerary:
                route_row = r
                break
        migration_route = []
        if route_row:
            # Parse the itinerary (itinry) field, which is a string like 'Amsterdam-Baltimore'
            legs = route_row['itinry'].replace(' & ', ',').replace('"', '').replace("'", '').split('-')
            # Split further on ',' for multi-port legs
            ports_in_route = []
            for leg in legs:
                for p in leg.split(','):
                    p = p.strip()
                    if p and p not in ports_in_route:
                        ports_in_route.append(p)
            # Build migration_route as list of dicts with name, lat, lon
            for p in ports_in_route:
                if p in ports:
                    migration_route.append(ports[p])
        # Only return migration_route if it has at least 2 ports (valid route)
        if len(migration_route) < 2:
            migration_route = []
        # --- End Migration Route Logic ---
        
        # Format response
        response = {
            'input': {
                'gender': data['sex'],
                'age': data['age'],
                'has_occupation': data['has_occupation'],
                'occupation_group': data.get('occ_grp', ''),
                'family_role': data.get('fam_role', ''),
                'year': data['arv_yr'],
                'country_origin': data['country_origin']
            },
            'predictions': {
                'ship_name': {
                    'value': predictions.get('ship_name', 'Unknown'),
                    'confidence': confidences.get('ship_name', 0.0)
                },
                'itinerary': {
                    'value': predictions.get('itinerary', 'Unknown'),
                    'confidence': confidences.get('itinerary', 0.0)
                },
                'q_psgrs': {
                    'value': predictions.get('q_psgrs', 'Unknown'),
                    'confidence': confidences.get('q_psgrs', 0.0)
                }
            },
            'migration_route': migration_route
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Get model status"""
    return jsonify({
        'model_loaded': model.is_loaded,
        'dataset_size': len(model.data) if model.is_loaded else 0
    })

if __name__ == '__main__':
    print("🚢 Starting Trans-Atlantic Voyagers Web Application...")
    print("📊 Loading prediction model...")
    model.load_model()
    print("🌐 Starting web server...")
    app.run(debug=True, host='0.0.0.0', port=5000)