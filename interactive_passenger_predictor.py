#!/usr/bin/env python3
"""
Interactive Trans-Atlantic Voyagers Passenger Predictor
=======================================================

Interactive interface for predicting passenger characteristics based on:
- Gender (sex)
- Age Range (age binned)
- Occupation (occID)
- Year of Departure (arv_yr)
- Original Residence (lkrID)
- Travel Group Size (travel_grp_size)

This script provides a user-friendly way to input passenger data and get predictions.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class InteractivePassengerPredictor:
    def __init__(self):
        self.data = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.prediction_models = {}
        self.options = {}
        self.occupation_lookup = {}
        self.residence_lookup = {}
        
    def load_model(self):
        """Load and prepare the prediction model"""
        print("🔄 Loading Trans-Atlantic Voyagers Prediction Model...")
        
        # Load data
        self.data = pd.read_csv('ttav_unified_dataset.csv', low_memory=False)
        
        # Create age ranges
        self.data['age_range'] = pd.cut(self.data['age'], 
                                       bins=[0, 18, 30, 45, 60, 100], 
                                       labels=['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior'])
        
        # Filter for complete cases
        required_cols = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        self.data = self.data.dropna(subset=required_cols)
        
        # Create lookup tables for user-friendly options
        self.create_lookup_tables()
        
        # Train the model
        self.train_model()
        
        print("✅ Model loaded successfully!")
        
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
        
        # Create user options
        self.options = {
            'sex': {
                'M': 'Male',
                'F': 'Female',
                'U': 'Unknown'
            },
            'age_range': {
                'Child': 'Child (0-18)',
                'Young Adult': 'Young Adult (19-30)',
                'Adult': 'Adult (31-45)',
                'Middle Age': 'Middle Age (46-60)',
                'Senior': 'Senior (60+)'
            },
            'occID': dict(list(self.occupation_lookup.items())[:20]),  # Top 20 occupations
            'arv_yr': {year: f"Year {year}" for year in range(1834, 1898, 5)},
            'lkrID': dict(list(self.residence_lookup.items())[:10]),  # Top 10 residences
            'travel_grp_size': {i: f"{i} passenger{'s' if i > 1 else ''}" for i in range(1, 11)}
        }
    
    def train_model(self):
        """Train the prediction models"""
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
    
    def predict_passenger(self, input_data):
        """Predict passenger characteristics"""
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
                confidence = np.max(proba)
                
                predictions[target] = pred
                confidences[target] = confidence
                
            except Exception as e:
                predictions[target] = "Unknown"
                confidences[target] = 0.0
        
        return predictions, confidences
    
    def display_options(self):
        """Display available input options"""
        print("\n" + "="*60)
        print("AVAILABLE INPUT OPTIONS")
        print("="*60)
        
        print(f"\n🚹🚺 Gender:")
        for key, value in self.options['sex'].items():
            print(f"   {key}: {value}")
        
        print(f"\n🎂 Age Range:")
        for key, value in self.options['age_range'].items():
            print(f"   {key}: {value}")
        
        print(f"\n💼 Occupation (sample):")
        for i, (key, value) in enumerate(list(self.options['occID'].items())[:5]):
            print(f"   {key}: {value}")
        print(f"   ... and {len(self.options['occID'])-5} more")
        
        print(f"\n📅 Year of Departure (sample):")
        years = list(self.options['arv_yr'].keys())
        print(f"   Available: {years[0]} to {years[-1]} (every 5 years)")
        
        print(f"\n🏠 Original Residence (sample):")
        for i, (key, value) in enumerate(list(self.options['lkrID'].items())[:3]):
            print(f"   {key}: {value}")
        print(f"   ... and {len(self.options['lkrID'])-3} more")
        
        print(f"\n👥 Travel Group Size:")
        for key, value in list(self.options['travel_grp_size'].items())[:5]:
            print(f"   {key}: {value}")
    
    def get_user_input(self):
        """Get user input for passenger characteristics"""
        print("\n" + "="*60)
        print("ENTER PASSENGER CHARACTERISTICS")
        print("="*60)
        
        input_data = {}
        
        # Gender
        print(f"\n🚹🚺 Select Gender:")
        for key, value in self.options['sex'].items():
            print(f"   {key}: {value}")
        while True:
            gender = input("Enter gender (M/F/U): ").strip().upper()
            if gender in self.options['sex']:
                input_data['sex'] = gender
                break
            print("❌ Invalid option. Please enter M, F, or U.")
        
        # Age Range
        print(f"\n🎂 Select Age Range:")
        age_options = list(self.options['age_range'].keys())
        for i, key in enumerate(age_options, 1):
            print(f"   {i}: {self.options['age_range'][key]}")
        while True:
            try:
                age_choice = int(input(f"Enter age range (1-{len(age_options)}): "))
                if 1 <= age_choice <= len(age_options):
                    input_data['age_range'] = age_options[age_choice - 1]
                    break
                print(f"❌ Please enter a number between 1 and {len(age_options)}.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Occupation
        print(f"\n💼 Select Occupation:")
        occ_options = list(self.options['occID'].items())[:10]  # Show top 10
        for i, (occ_id, occ_name) in enumerate(occ_options, 1):
            print(f"   {i}: {occ_name}")
        while True:
            try:
                occ_choice = int(input(f"Enter occupation (1-{len(occ_options)}): "))
                if 1 <= occ_choice <= len(occ_options):
                    input_data['occID'] = occ_options[occ_choice - 1][0]
                    break
                print(f"❌ Please enter a number between 1 and {len(occ_options)}.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Year
        print(f"\n📅 Enter Year of Departure:")
        while True:
            try:
                year = int(input("Enter year (1834-1897): "))
                if 1834 <= year <= 1897:
                    input_data['arv_yr'] = year
                    break
                print("❌ Please enter a year between 1834 and 1897.")
            except ValueError:
                print("❌ Please enter a valid year.")
        
        # Residence
        print(f"\n🏠 Select Original Residence:")
        res_options = list(self.options['lkrID'].items())[:5]  # Show top 5
        for i, (res_id, res_name) in enumerate(res_options, 1):
            print(f"   {i}: {res_name}")
        while True:
            try:
                res_choice = int(input(f"Enter residence (1-{len(res_options)}): "))
                if 1 <= res_choice <= len(res_options):
                    input_data['lkrID'] = res_options[res_choice - 1][0]
                    break
                print(f"❌ Please enter a number between 1 and {len(res_options)}.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Travel Group Size
        print(f"\n👥 Enter Travel Group Size:")
        while True:
            try:
                group_size = int(input("Enter group size (1-10): "))
                if 1 <= group_size <= 10:
                    input_data['travel_grp_size'] = group_size
                    break
                print("❌ Please enter a number between 1 and 10.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        return input_data
    
    def display_predictions(self, predictions, confidences, input_data):
        """Display prediction results"""
        print("\n" + "="*60)
        print("PREDICTION RESULTS")
        print("="*60)
        
        print(f"\n📝 Input Summary:")
        print(f"   Gender: {self.options['sex'][input_data['sex']]}")
        print(f"   Age Range: {self.options['age_range'][input_data['age_range']]}")
        print(f"   Occupation: {self.occupation_lookup.get(input_data['occID'], 'Unknown')}")
        print(f"   Year: {input_data['arv_yr']}")
        print(f"   Residence: {self.residence_lookup.get(input_data['lkrID'], 'Unknown')}")
        print(f"   Group Size: {input_data['travel_grp_size']}")
        
        print(f"\n🔮 Predicted Characteristics:")
        
        prediction_labels = {
            'litr': '📚 Literacy',
            'fam_role': '👨‍👩‍👧‍👦 Family Role',
            'pasg': '🚢 Passage Type',
            'occ_grp': '💼 Occupation Group',
            'port_arv': '🏙️ Arrival Port'
        }
        
        for target, pred in predictions.items():
            if target in prediction_labels:
                confidence = confidences.get(target, 0.0)
                confidence_bar = "█" * int(confidence * 10) + "░" * (10 - int(confidence * 10))
                print(f"   {prediction_labels[target]}: {pred}")
                print(f"      Confidence: {confidence:.1%} {confidence_bar}")
    
    def run_interactive_session(self):
        """Run interactive prediction session"""
        print("="*60)
        print("🚢 TRANS-ATLANTIC VOYAGERS PASSENGER PREDICTOR")
        print("="*60)
        print("Predict passenger characteristics based on historical data")
        print("from Russian Empire migration to the USA (1834-1897)")
        
        while True:
            print("\n" + "="*60)
            print("MAIN MENU")
            print("="*60)
            print("1. View available options")
            print("2. Make a prediction")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.display_options()
                
            elif choice == '2':
                try:
                    input_data = self.get_user_input()
                    predictions, confidences = self.predict_passenger(input_data)
                    self.display_predictions(predictions, confidences, input_data)
                    
                    # Ask if user wants to continue
                    continue_choice = input("\nMake another prediction? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        break
                        
                except KeyboardInterrupt:
                    print("\n\nOperation cancelled.")
                    break
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    
            elif choice == '3':
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        print("\n👋 Thank you for using the Trans-Atlantic Voyagers Predictor!")

def main():
    """Main function"""
    predictor = InteractivePassengerPredictor()
    predictor.load_model()
    predictor.run_interactive_session()

if __name__ == "__main__":
    main()