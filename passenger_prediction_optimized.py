#!/usr/bin/env python3
"""
Trans-Atlantic Voyagers Passenger Prediction Model (Optimized)
==============================================================

This model uses hierarchical clustering on a sample to predict passenger characteristics based on:
- Gender (sex)
- Age Range (age binned)
- Occupation (occID -> occupation categories)
- Year of Departure (arv_yr)
- Original Residence (lkrID -> residence info)
- Travel Group Size (travel_grp_size)

Uses sampling for efficient hierarchical clustering, then applies to full dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class OptimizedPassengerPredictor:
    def __init__(self, sample_size=10000):
        self.sample_size = sample_size
        self.data = None
        self.sample_data = None
        self.processed_data = None
        self.clusters = None
        self.cluster_model = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.prediction_models = {}
        self.feature_columns = []
        self.target_columns = []
        self.cluster_centers = None
        
    def load_and_prepare_data(self):
        """Load the unified dataset and prepare features"""
        print("="*60)
        print("OPTIMIZED PASSENGER PREDICTION MODEL")
        print("="*60)
        
        # Load unified dataset
        print(f"\n📊 Loading unified dataset...")
        self.data = pd.read_csv('ttav_unified_dataset.csv', low_memory=False)
        print(f"✓ Loaded {len(self.data):,} passenger records")
        
        # Define input features (from user specification)
        input_features = {
            'Gender': 'sex',
            'Age': 'age', 
            'Occupation': 'occID',
            'Year_of_Departure': 'arv_yr',
            'Original_Residence': 'lkrID',
            'Travel_Group_Size': 'travel_grp_size'
        }
        
        print(f"\n🎯 User-Specified Input Features:")
        for label, column in input_features.items():
            if column in self.data.columns:
                non_null = self.data[column].count()
                total = len(self.data)
                print(f"   {label}: {column} ({non_null:,}/{total:,} non-null, {non_null/total*100:.1f}%)")
            else:
                print(f"   ❌ {label}: {column} (NOT FOUND)")
        
        # Create age bins
        print(f"\n🔢 Creating age ranges...")
        self.data['age_range'] = pd.cut(self.data['age'], 
                                       bins=[0, 18, 30, 45, 60, 100], 
                                       labels=['Child (0-18)', 'Young Adult (19-30)', 
                                              'Adult (31-45)', 'Middle Age (46-60)', 'Senior (60+)'])
        
        # Filter for complete cases in input features
        required_cols = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        print(f"\n🧹 Filtering for complete input feature cases...")
        
        before_filter = len(self.data)
        self.data = self.data.dropna(subset=required_cols)
        after_filter = len(self.data)
        
        print(f"   Before filtering: {before_filter:,} records")
        print(f"   After filtering: {after_filter:,} records")
        print(f"   Removed: {before_filter - after_filter:,} records ({(before_filter - after_filter)/before_filter*100:.1f}%)")
        
        # Create stratified sample for clustering
        print(f"\n🎲 Creating stratified sample for clustering...")
        sample_size = min(self.sample_size, len(self.data))
        
        # Stratify by key categorical variables
        stratify_cols = ['sex', 'age_range']
        stratify_key = self.data[stratify_cols].apply(lambda x: '_'.join(x.astype(str)), axis=1)
        
        sampled_groups = self.data.groupby(stratify_key, group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(1, int(sample_size * len(x) / len(self.data)))))
        )
        
        # If we have more samples than requested, downsample
        if len(sampled_groups) > sample_size:
            self.sample_data = sampled_groups.sample(n=sample_size, random_state=42).reset_index(drop=True)
        else:
            self.sample_data = sampled_groups.reset_index(drop=True)
        
        print(f"   Sample size: {len(self.sample_data):,} records")
        print(f"   Sample ratio: {len(self.sample_data)/len(self.data)*100:.1f}%")
        
        return self.data, self.sample_data
    
    def prepare_features_and_targets(self):
        """Prepare feature matrix and target variables"""
        print(f"\n🔧 Preparing features and targets...")
        
        # Input features for clustering and prediction
        self.feature_columns = ['sex', 'age_range', 'occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        
        # Target columns to predict (interesting passenger characteristics)
        self.target_columns = [
            'litr',  # Literacy
            'fam_role',  # Family role
            'pasg',  # Passage type (steerage/cabin)
            'occ_grp',  # Occupation group
            'tsar_trty',  # Whether from tsarist territory
            'port_arv',  # Arrival port
            'occ_nm',  # Specific occupation name
            'resdn'  # Residence name
        ]
        
        print(f"   Input features: {len(self.feature_columns)} columns")
        print(f"   Target variables: {len(self.target_columns)} columns")
        
        # Create feature matrix for sample data
        X_sample = self.sample_data[self.feature_columns].copy()
        
        # Encode categorical variables
        print(f"\n🏷️  Encoding categorical variables...")
        
        categorical_cols = ['sex', 'age_range']
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in X_sample.columns:
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                encoded = encoder.fit_transform(X_sample[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in encoder.categories_[0]],
                                        index=X_sample.index)
                X_sample = pd.concat([X_sample.drop(col, axis=1), encoded_df], axis=1)
                self.encoders[col] = encoder
        
        # Scale numerical variables
        X_sample[numerical_cols] = self.scaler.fit_transform(X_sample[numerical_cols])
        
        self.processed_data = X_sample
        print(f"   Final feature matrix (sample): {X_sample.shape[0]:,} rows × {X_sample.shape[1]} columns")
        
        return X_sample
    
    def perform_hierarchical_clustering(self, n_clusters=8):
        """Perform hierarchical clustering on sample data"""
        print(f"\n🌳 Performing Hierarchical Clustering on Sample...")
        
        X = self.processed_data
        
        # Try different numbers of clusters and evaluate
        print(f"   Evaluating optimal number of clusters...")
        silhouette_scores = []
        cluster_range = range(3, min(12, len(X)//100))  # Reasonable range
        
        best_score = -1
        best_n_clusters = 8
        
        for n in cluster_range:
            try:
                clusterer = AgglomerativeClustering(n_clusters=n, linkage='ward')
                cluster_labels = clusterer.fit_predict(X)
                silhouette_avg = silhouette_score(X, cluster_labels)
                silhouette_scores.append(silhouette_avg)
                print(f"     {n} clusters: Silhouette Score = {silhouette_avg:.3f}")
                
                if silhouette_avg > best_score:
                    best_score = silhouette_avg
                    best_n_clusters = n
                    
            except Exception as e:
                print(f"     {n} clusters: Error - {e}")
                silhouette_scores.append(0)
        
        print(f"   🎯 Optimal number of clusters: {best_n_clusters}")
        
        # Perform final clustering
        self.cluster_model = AgglomerativeClustering(n_clusters=best_n_clusters, linkage='ward')
        self.clusters = self.cluster_model.fit_predict(X)
        
        # Add cluster labels to sample data
        self.sample_data['cluster'] = self.clusters
        
        print(f"   ✅ Clustering complete!")
        print(f"   Final silhouette score: {best_score:.3f}")
        
        # Analyze clusters
        self.analyze_clusters()
        
        return self.clusters
    
    def analyze_clusters(self):
        """Analyze the characteristics of each cluster"""
        print(f"\n📊 Analyzing Cluster Characteristics...")
        
        cluster_summary = []
        
        for cluster_id in sorted(self.sample_data['cluster'].unique()):
            cluster_data = self.sample_data[self.sample_data['cluster'] == cluster_id]
            size = len(cluster_data)
            
            summary = {
                'Cluster': cluster_id,
                'Size': size,
                'Percentage': f"{size/len(self.sample_data)*100:.1f}%",
                'Avg_Age': f"{cluster_data['age'].mean():.1f}",
                'Most_Common_Gender': cluster_data['sex'].mode().iloc[0] if not cluster_data['sex'].mode().empty else 'N/A',
                'Most_Common_Occupation': cluster_data['occ_nm'].mode().iloc[0] if 'occ_nm' in cluster_data.columns and not cluster_data['occ_nm'].mode().empty else 'N/A',
                'Avg_Year': f"{cluster_data['arv_yr'].mean():.0f}",
                'Most_Common_Port': cluster_data['port_arv'].mode().iloc[0] if 'port_arv' in cluster_data.columns and not cluster_data['port_arv'].mode().empty else 'N/A'
            }
            cluster_summary.append(summary)
        
        cluster_df = pd.DataFrame(cluster_summary)
        print("\n" + "="*100)
        print("CLUSTER CHARACTERISTICS SUMMARY")
        print("="*100)
        print(cluster_df.to_string(index=False))
        
        return cluster_df
    
    def assign_clusters_to_full_data(self):
        """Assign cluster labels to full dataset using trained model"""
        print(f"\n🔄 Assigning clusters to full dataset...")
        
        # Prepare full dataset features
        X_full = self.data[self.feature_columns].copy()
        
        # Apply same encoding and scaling
        categorical_cols = ['sex', 'age_range']
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in X_full.columns and col in self.encoders:
                encoded = self.encoders[col].transform(X_full[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                        index=X_full.index)
                X_full = pd.concat([X_full.drop(col, axis=1), encoded_df], axis=1)
        
        # Scale numerical variables
        X_full[numerical_cols] = self.scaler.transform(X_full[numerical_cols])
        
        # Use KMeans to assign clusters (more scalable than hierarchical clustering)
        print(f"   Using KMeans to assign clusters to full dataset...")
        
        # Calculate cluster centers from sample
        sample_cluster_centers = []
        for cluster_id in np.unique(self.clusters):
            cluster_mask = self.clusters == cluster_id
            cluster_center = self.processed_data[cluster_mask].mean()
            sample_cluster_centers.append(cluster_center.values)
        
        cluster_centers = np.array(sample_cluster_centers)
        
        # Assign each point to nearest cluster center
        full_clusters = []
        for i, row in X_full.iterrows():
            distances = [np.linalg.norm(row.values - center) for center in cluster_centers]
            closest_cluster = np.argmin(distances)
            full_clusters.append(closest_cluster)
        
        full_clusters = np.array(full_clusters)
        self.data['cluster'] = full_clusters
        
        print(f"   ✅ Assigned clusters to {len(self.data):,} passengers")
        
        return full_clusters
    
    def build_prediction_models(self):
        """Build prediction models for each target variable"""
        print(f"\n🤖 Building Prediction Models...")
        
        # Use full dataset for training prediction models
        X_full = self.data[self.feature_columns + ['cluster']].copy()
        
        # Encode features for full dataset
        categorical_cols = ['sex', 'age_range']
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size', 'cluster']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in X_full.columns and col in self.encoders:
                encoded = self.encoders[col].transform(X_full[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                        index=X_full.index)
                X_full = pd.concat([X_full.drop(col, axis=1), encoded_df], axis=1)
        
        # Scale numerical variables (except cluster)
        scale_cols = [col for col in numerical_cols if col != 'cluster']
        scaler_full = StandardScaler()
        X_full[scale_cols] = scaler_full.fit_transform(X_full[scale_cols])
        
        for target in self.target_columns:
            if target not in self.data.columns:
                print(f"   ⚠️  Skipping {target} - column not found")
                continue
                
            print(f"\n   Training model for: {target}")
            
            # Get target variable (remove rows with missing targets)
            target_data = self.data[target].dropna()
            if len(target_data) == 0:
                print(f"     ❌ No data available for {target}")
                continue
                
            X_target = X_full.loc[target_data.index]
            y_target = target_data
            
            # Determine if classification or regression
            if y_target.dtype == 'object' or len(y_target.unique()) < 50:
                # Classification
                model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
                model_type = 'classification'
            else:
                # Regression
                model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
                model_type = 'regression'
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_target, y_target, test_size=0.2, random_state=42, stratify=y_target if model_type == 'classification' else None
            )
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            
            if model_type == 'classification':
                accuracy = accuracy_score(y_test, y_pred)
                print(f"     ✅ Accuracy: {accuracy:.3f}")
                print(f"     📊 Unique classes: {len(y_target.unique())}")
                metric = accuracy
            else:
                mse = mean_squared_error(y_test, y_pred)
                print(f"     ✅ MSE: {mse:.3f}")
                metric = mse
            
            # Store model
            self.prediction_models[target] = {
                'model': model,
                'scaler': scaler_full,
                'type': model_type,
                'metric': metric,
                'feature_importance': dict(zip(X_target.columns, model.feature_importances_))
            }
        
        print(f"\n✅ Built {len(self.prediction_models)} prediction models")
        return self.prediction_models
    
    def predict_passenger_characteristics(self, input_data):
        """Predict passenger characteristics based on input features"""
        print(f"\n🔮 Predicting Passenger Characteristics...")
        
        # Convert input to DataFrame if needed
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data.copy()
        
        print(f"   Input: {input_df.iloc[0].to_dict()}")
        
        # First, predict cluster membership
        X_input = input_df[self.feature_columns].copy()
        
        # Apply same encoding and scaling as training
        categorical_cols = ['sex', 'age_range']
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in X_input.columns and col in self.encoders:
                encoded = self.encoders[col].transform(X_input[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                        index=X_input.index)
                X_input = pd.concat([X_input.drop(col, axis=1), encoded_df], axis=1)
        
        # Scale numerical variables
        X_input[numerical_cols] = self.scaler.transform(X_input[numerical_cols])
        
        # Predict cluster (using nearest cluster center)
        cluster_distances = []
        for cluster_id in np.unique(self.clusters):
            cluster_mask = self.clusters == cluster_id
            cluster_center = self.processed_data[cluster_mask].mean()
            # Calculate distance to cluster center
            distance = np.linalg.norm(X_input.iloc[0].values - cluster_center.values)
            cluster_distances.append((cluster_id, distance))
        
        predicted_cluster = min(cluster_distances, key=lambda x: x[1])[0]
        print(f"   Predicted cluster: {predicted_cluster}")
        
        # Add cluster to input features
        input_df['cluster'] = predicted_cluster
        X_input_with_cluster = input_df[self.feature_columns + ['cluster']].copy()
        
        # Apply encoding for prediction
        for col in categorical_cols:
            if col in X_input_with_cluster.columns and col in self.encoders:
                encoded = self.encoders[col].transform(X_input_with_cluster[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                                        index=X_input_with_cluster.index)
                X_input_with_cluster = pd.concat([X_input_with_cluster.drop(col, axis=1), encoded_df], axis=1)
        
        # Make predictions
        predictions = {}
        
        for target, model_info in self.prediction_models.items():
            try:
                # Scale features
                X_scaled = X_input_with_cluster.copy()
                scale_cols = [col for col in numerical_cols if col != 'cluster']
                if 'cluster' in X_scaled.columns:
                    scale_cols_available = [col for col in scale_cols if col in X_scaled.columns]
                    X_scaled[scale_cols_available] = model_info['scaler'].transform(X_scaled[scale_cols_available])
                
                pred = model_info['model'].predict(X_scaled)
                predictions[target] = pred[0] if len(pred) == 1 else pred
                
                # Get prediction probability for classification
                if model_info['type'] == 'classification' and hasattr(model_info['model'], 'predict_proba'):
                    proba = model_info['model'].predict_proba(X_scaled)
                    max_proba = np.max(proba)
                    print(f"   ✅ {target}: {predictions[target]} (confidence: {max_proba:.2f})")
                else:
                    print(f"   ✅ {target}: {predictions[target]}")
                    
            except Exception as e:
                print(f"   ❌ Error predicting {target}: {e}")
                predictions[target] = None
        
        return predictions, predicted_cluster
    
    def create_interactive_example(self):
        """Create an interactive example for user input"""
        print(f"\n🖥️  Creating Interactive Example...")
        
        # Get sample values for each input field
        example_options = {
            'sex': list(self.data['sex'].unique()),
            'age_range': ['Child (0-18)', 'Young Adult (19-30)', 'Adult (31-45)', 'Middle Age (46-60)', 'Senior (60+)'],
            'occID': sorted(self.data['occID'].unique())[:20],  # Top 20 occupation IDs
            'arv_yr': sorted(self.data['arv_yr'].unique())[::5],  # Every 5th year
            'lkrID': sorted(self.data['lkrID'].unique())[:10],  # Top 10 residence IDs
            'travel_grp_size': sorted(self.data['travel_grp_size'].unique())[:10]  # Top 10 group sizes
        }
        
        print(f"\n📋 Available Input Options:")
        for field, values in example_options.items():
            print(f"   {field}: {values}")
        
        # Create several example predictions
        examples = [
            {
                'sex': 'M',
                'age_range': 'Young Adult (19-30)',
                'occID': 210,
                'arv_yr': 1890,
                'lkrID': 2,
                'travel_grp_size': 1
            },
            {
                'sex': 'F',
                'age_range': 'Adult (31-45)',
                'occID': 681,
                'arv_yr': 1885,
                'lkrID': 1,
                'travel_grp_size': 4
            },
            {
                'sex': 'M',
                'age_range': 'Middle Age (46-60)',
                'occID': 342,
                'arv_yr': 1875,
                'lkrID': 244,
                'travel_grp_size': 2
            }
        ]
        
        print(f"\n🔮 Example Predictions:")
        for i, example in enumerate(examples, 1):
            print(f"\n--- Example {i} ---")
            try:
                predictions, cluster = self.predict_passenger_characteristics(example)
                print(f"   Cluster: {cluster}")
                print(f"   Key Predictions:")
                for target, pred in predictions.items():
                    if pred is not None:
                        print(f"     • {target}: {pred}")
            except Exception as e:
                print(f"   ❌ Prediction failed: {e}")
        
        return example_options

def main():
    """Main execution function"""
    print("="*60)
    print("OPTIMIZED TRANS-ATLANTIC VOYAGERS PREDICTION MODEL")
    print("="*60)
    
    # Initialize predictor
    predictor = OptimizedPassengerPredictor(sample_size=10000)
    
    # Load and prepare data
    data, sample_data = predictor.load_and_prepare_data()
    
    # Prepare features
    X = predictor.prepare_features_and_targets()
    
    # Perform clustering on sample
    clusters = predictor.perform_hierarchical_clustering()
    
    # Assign clusters to full dataset
    full_clusters = predictor.assign_clusters_to_full_data()
    
    # Build prediction models
    models = predictor.build_prediction_models()
    
    # Create interactive examples
    options = predictor.create_interactive_example()
    
    print(f"\n" + "="*60)
    print("MODEL TRAINING COMPLETE! 🎉")
    print("="*60)
    
    print(f"\n📊 Model Summary:")
    print(f"   • Total passengers: {len(data):,}")
    print(f"   • Sample for clustering: {len(sample_data):,}")
    print(f"   • Features: {len(predictor.feature_columns)} input variables")
    print(f"   • Clusters: {len(np.unique(clusters))} passenger groups")
    print(f"   • Prediction models: {len(models)} target variables")
    
    print(f"\n🎯 Available Predictions:")
    for target, model_info in models.items():
        print(f"   • {target}: {model_info['type']} (score: {model_info['metric']:.3f})")
    
    return predictor

if __name__ == "__main__":
    predictor = main()