#!/usr/bin/env python3
"""
Trans-Atlantic Voyagers Simple Passenger Predictor
==================================================

This model uses user-specified input features to predict passenger characteristics:
- Gender (sex)
- Age Range (age binned)  
- Occupation (occID)
- Year of Departure (arv_yr)
- Original Residence (lkrID)
- Travel Group Size (travel_grp_size)

Uses hierarchical clustering on a sample and prediction models for efficiency.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class SimplePassengerPredictor:
    def __init__(self):
        self.data = None
        self.sample_data = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.prediction_models = {}
        self.clusters = None
        
    def load_and_prepare_data(self, sample_size=5000):
        """Load and prepare data for modeling"""
        print("="*60)
        print("SIMPLE PASSENGER PREDICTION MODEL")
        print("="*60)
        
        # Load data
        print(f"\n📊 Loading unified dataset...")
        self.data = pd.read_csv('ttav_unified_dataset.csv', low_memory=False)
        print(f"✓ Loaded {len(self.data):,} passenger records")
        
        # Create age ranges
        self.data['age_range'] = pd.cut(self.data['age'], 
                                       bins=[0, 18, 30, 45, 60, 100], 
                                       labels=['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior'])
        
        # Filter for complete cases
        required_cols = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        self.data = self.data.dropna(subset=required_cols)
        print(f"✓ Filtered to {len(self.data):,} complete records")
        
        # Create sample for clustering
        self.sample_data = self.data.sample(n=min(sample_size, len(self.data)), random_state=42)
        print(f"✓ Created sample of {len(self.sample_data):,} records for clustering")
        
        return self.data
    
    def perform_clustering(self):
        """Perform hierarchical clustering on sample"""
        print(f"\n🌳 Performing Hierarchical Clustering...")
        
        # Prepare features for clustering
        features = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        X = self.sample_data[features].copy()
        
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
        
        # Perform clustering
        clusterer = AgglomerativeClustering(n_clusters=6, linkage='ward')
        self.clusters = clusterer.fit_predict(X)
        self.sample_data['cluster'] = self.clusters
        
        print(f"✅ Created {len(np.unique(self.clusters))} clusters")
        
        # Analyze clusters
        self.analyze_clusters()
        
        return self.clusters
    
    def analyze_clusters(self):
        """Analyze cluster characteristics"""
        print(f"\n📊 Cluster Analysis:")
        
        for cluster_id in sorted(np.unique(self.clusters)):
            cluster_data = self.sample_data[self.sample_data['cluster'] == cluster_id]
            size = len(cluster_data)
            
            print(f"\n🔸 Cluster {cluster_id} ({size} passengers, {size/len(self.sample_data)*100:.1f}%):")
            print(f"   Average Age: {cluster_data['age'].mean():.1f}")
            print(f"   Most Common Gender: {cluster_data['sex'].mode().iloc[0]}")
            print(f"   Most Common Occupation: {cluster_data['occ_nm'].mode().iloc[0] if 'occ_nm' in cluster_data.columns else 'N/A'}")
            print(f"   Average Year: {cluster_data['arv_yr'].mean():.0f}")
            print(f"   Average Group Size: {cluster_data['travel_grp_size'].mean():.1f}")
    
    def build_prediction_models(self):
        """Build prediction models for passenger characteristics"""
        print(f"\n🤖 Building Prediction Models...")
        
        # Use full dataset for training
        features = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        targets = ['litr', 'fam_role', 'pasg', 'occ_grp', 'port_arv']
        
        # Prepare feature matrix
        X = self.data[features].copy()
        
        # Encode categorical variables
        categorical_cols = ['sex', 'age_range']
        for col in categorical_cols:
            if col in self.encoders:
                encoded = self.encoders[col].transform(X[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                        index=X.index)
                X = pd.concat([X.drop(col, axis=1), encoded_df], axis=1)
        
        # Scale numerical variables
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        X[numerical_cols] = self.scaler.transform(X[numerical_cols])
        
        # Train models for each target
        for target in targets:
            if target not in self.data.columns:
                continue
                
            print(f"   Training model for {target}...")
            
            # Get non-null target data
            target_mask = self.data[target].notna()
            X_target = X[target_mask]
            y_target = self.data[target][target_mask]
            
            if len(y_target) < 100:  # Skip if too few samples
                continue
            
            # Choose model type
            if y_target.dtype == 'object' or len(y_target.unique()) < 50:
                model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=8)
                model_type = 'classification'
            else:
                model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=8)
                model_type = 'regression'
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_target, y_target, test_size=0.2, random_state=42
            )
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            if model_type == 'classification':
                score = accuracy_score(y_test, y_pred)
                print(f"     ✅ Accuracy: {score:.3f}")
            else:
                score = mean_squared_error(y_test, y_pred)
                print(f"     ✅ MSE: {score:.3f}")
            
            # Store model
            self.prediction_models[target] = {
                'model': model,
                'type': model_type,
                'score': score
            }
        
        print(f"✅ Built {len(self.prediction_models)} prediction models")
        return self.prediction_models
    
    def predict_passenger(self, input_data):
        """Predict passenger characteristics from input features"""
        print(f"\n🔮 Making Predictions...")
        
        # Convert to DataFrame
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data.copy()
        
        print(f"   Input: {input_df.iloc[0].to_dict()}")
        
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
        for target, model_info in self.prediction_models.items():
            try:
                pred = model_info['model'].predict(X_input)
                predictions[target] = pred[0]
                
                # Get confidence for classification
                if model_info['type'] == 'classification' and hasattr(model_info['model'], 'predict_proba'):
                    proba = model_info['model'].predict_proba(X_input)
                    confidence = np.max(proba)
                    print(f"   ✅ {target}: {pred[0]} (confidence: {confidence:.2f})")
                else:
                    print(f"   ✅ {target}: {pred[0]}")
                    
            except Exception as e:
                print(f"   ❌ Error predicting {target}: {e}")
                predictions[target] = None
        
        return predictions
    
    def create_user_interface(self):
        """Create user interface with examples"""
        print(f"\n🖥️  User Interface Examples:")
        
        # Get available options
        options = {
            'sex': list(self.data['sex'].unique()),
            'age_range': ['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior'],
            'occID': sorted(self.data['occID'].unique())[:10],
            'arv_yr': list(range(1834, 1898, 10)),
            'lkrID': sorted(self.data['lkrID'].unique())[:5],
            'travel_grp_size': [1, 2, 3, 4, 5]
        }
        
        print(f"\n📋 Available Options:")
        for field, values in options.items():
            print(f"   {field}: {values}")
        
        # Example predictions
        examples = [
            {
                'sex': 'M',
                'age_range': 'Young Adult',
                'occID': 210,
                'arv_yr': 1890,
                'lkrID': 2,
                'travel_grp_size': 1
            },
            {
                'sex': 'F',
                'age_range': 'Adult',
                'occID': 681,
                'arv_yr': 1885,
                'lkrID': 1,
                'travel_grp_size': 3
            }
        ]
        
        print(f"\n🔮 Example Predictions:")
        for i, example in enumerate(examples, 1):
            print(f"\n--- Example {i} ---")
            predictions = self.predict_passenger(example)
            
        return options

def main():
    """Main execution function"""
    # Initialize predictor
    predictor = SimplePassengerPredictor()
    
    # Load and prepare data
    data = predictor.load_and_prepare_data()
    
    # Perform clustering
    clusters = predictor.perform_clustering()
    
    # Build prediction models
    models = predictor.build_prediction_models()
    
    # Create user interface
    options = predictor.create_user_interface()
    
    print(f"\n" + "="*60)
    print("PASSENGER PREDICTION MODEL COMPLETE! 🎉")
    print("="*60)
    
    print(f"\n📊 Summary:")
    print(f"   • Dataset: {len(data):,} passengers")
    print(f"   • Clusters: {len(np.unique(clusters))} groups")
    print(f"   • Models: {len(models)} prediction targets")
    
    print(f"\n🎯 Prediction Targets:")
    for target, model_info in models.items():
        print(f"   • {target}: {model_info['type']} (score: {model_info['score']:.3f})")
    
    print(f"\n🔧 How to use:")
    print(f"   predictor.predict_passenger({{'sex': 'M', 'age_range': 'Young Adult', 'occID': 210, 'arv_yr': 1890, 'lkrID': 2, 'travel_grp_size': 1}})")
    
    return predictor

if __name__ == "__main__":
    predictor = main()