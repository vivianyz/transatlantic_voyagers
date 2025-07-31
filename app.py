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
            
            # Prepare features
            features = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
            X_input = input_df[features].copy()
            
            # Encode categorical variables
            categorical_cols = ['sex', 'age_range']
            for col in categorical_cols:
                if col in self.encoders:
                    encoded = self.encoders[col].transform(X_input[[col]])
                    encoded_df = pd.DataFrame(encoded, 
                                            columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                            index=X_input.index)
                    X_input = pd.concat([X_input.drop(col, axis=1), encoded_df], axis=1)
            
            # Scale numerical variables
            numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
            X_input[numerical_cols] = self.scaler.transform(X_input[numerical_cols])
            
            # Make predictions
            predictions = {}
            confidences = {}
            
            for target, model in self.prediction_models.items():
                try:
                    pred = model.predict(X_input)[0]
                    proba = model.predict_proba(X_input)
                    confidence = float(np.max(proba))
                    
                    predictions[target] = str(pred)
                    confidences[target] = confidence
                    
                except Exception as e:
                    predictions[target] = "Unknown"
                    confidences[target] = 0.0
            
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
            'age_ranges': [
                {'value': 'Child', 'label': 'Child (0-18)'},
                {'value': 'Young Adult', 'label': 'Young Adult (19-30)'},
                {'value': 'Adult', 'label': 'Adult (31-45)'},
                {'value': 'Middle Age', 'label': 'Middle Age (46-60)'},
                {'value': 'Senior', 'label': 'Senior (60+)'}
            ],
            'occupations': [
                {'value': int(occ_id), 'label': occ_name} 
                for occ_id, occ_name in list(self.occupation_lookup.items())[:20]
            ],
            'years': [
                {'value': year, 'label': f"Year {year}"} 
                for year in range(1834, 1898, 5)
            ],
            'residences': [
                {'value': int(res_id), 'label': res_name} 
                for res_id, res_name in list(self.residence_lookup.items())[:10]
            ],
            'group_sizes': [
                {'value': i, 'label': f"{i} passenger{'s' if i > 1 else ''}"} 
                for i in range(1, 11)
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
        required_fields = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        result = model.predict(data)
        if result is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        predictions, confidences = result
        
        # Format response
        response = {
            'input': {
                'gender': data['sex'],
                'age_range': data['age_range'],
                'occupation': model.occupation_lookup.get(data['occID'], 'Unknown'),
                'year': data['arv_yr'],
                'residence': model.residence_lookup.get(data['lkrID'], 'Unknown'),
                'group_size': data['travel_grp_size']
            },
            'predictions': {
                'literacy': {
                    'value': predictions.get('litr', 'Unknown'),
                    'confidence': confidences.get('litr', 0.0)
                },
                'family_role': {
                    'value': predictions.get('fam_role', 'Unknown'),
                    'confidence': confidences.get('fam_role', 0.0)
                },
                'passage_type': {
                    'value': predictions.get('pasg', 'Unknown'),
                    'confidence': confidences.get('pasg', 0.0)
                },
                'occupation_group': {
                    'value': predictions.get('occ_grp', 'Unknown'),
                    'confidence': confidences.get('occ_grp', 0.0)
                },
                'arrival_port': {
                    'value': predictions.get('port_arv', 'Unknown'),
                    'confidence': confidences.get('port_arv', 0.0)
                }
            }
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