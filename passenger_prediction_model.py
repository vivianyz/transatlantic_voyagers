#!/usr/bin/env python3
"""
Trans-Atlantic Voyagers Passenger Prediction Model
==================================================

This model uses hierarchical clustering to predict passenger characteristics based on:
- Gender (sex)
- Age Range (age binned)
- Occupation (occID -> occupation categories)
- Year of Departure (arv_yr)
- Original Residence (lkrID -> residence info)
- Travel Group Size (travel_grp_size)

The model clusters similar passengers and predicts missing fields for new inputs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class PassengerPredictor:
    def __init__(self):
        self.data = None
        self.processed_data = None
        self.clusters = None
        self.cluster_model = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.prediction_models = {}
        self.feature_columns = []
        self.target_columns = []
        
    def load_and_prepare_data(self):
        """Load the unified dataset and prepare features"""
        print("="*60)
        print("PASSENGER PREDICTION MODEL - DATA PREPARATION")
        print("="*60)
        
        # Load unified dataset
        print("\n📊 Loading unified dataset...")
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
        
        print(f"\n🎯 Input Features Specified:")
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
        
        return self.data
    
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
            'port_arv'  # Arrival port
        ]
        
        print(f"   Input features: {len(self.feature_columns)} columns")
        print(f"   Target variables: {len(self.target_columns)} columns")
        
        # Create feature matrix
        X = self.data[self.feature_columns].copy()
        
        # Encode categorical variables
        print(f"\n🏷️  Encoding categorical variables...")
        
        categorical_cols = ['sex', 'age_range']
        numerical_cols = ['occID', 'arv_yr', 'lkrID', 'travel_grp_size']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in X.columns:
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                encoded = encoder.fit_transform(X[[col]])
                encoded_df = pd.DataFrame(encoded, 
                                        columns=[f"{col}_{cat}" for cat in encoder.categories_[0]],
                                        index=X.index)
                X = pd.concat([X.drop(col, axis=1), encoded_df], axis=1)
                self.encoders[col] = encoder
        
        # Scale numerical variables
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        
        self.processed_data = X
        print(f"   Final feature matrix: {X.shape[0]:,} rows × {X.shape[1]} columns")
        
        return X
    
    def perform_hierarchical_clustering(self, n_clusters=8):
        """Perform hierarchical clustering on passenger data"""
        print(f"\n🌳 Performing Hierarchical Clustering...")
        
        X = self.processed_data
        
        # Try different numbers of clusters and evaluate
        print(f"   Evaluating optimal number of clusters...")
        silhouette_scores = []
        cluster_range = range(3, 15)
        
        for n in cluster_range:
            clusterer = AgglomerativeClustering(n_clusters=n, linkage='ward')
            cluster_labels = clusterer.fit_predict(X)
            silhouette_avg = silhouette_score(X, cluster_labels)
            silhouette_scores.append(silhouette_avg)
            print(f"     {n} clusters: Silhouette Score = {silhouette_avg:.3f}")
        
        # Choose optimal number of clusters
        optimal_clusters = cluster_range[np.argmax(silhouette_scores)]
        print(f"   🎯 Optimal number of clusters: {optimal_clusters}")
        
        # Perform final clustering
        self.cluster_model = AgglomerativeClustering(n_clusters=optimal_clusters, linkage='ward')
        self.clusters = self.cluster_model.fit_predict(X)
        
        # Add cluster labels to original data
        self.data['cluster'] = self.clusters
        
        print(f"   ✅ Clustering complete!")
        print(f"   Final silhouette score: {max(silhouette_scores):.3f}")
        
        # Analyze clusters
        self.analyze_clusters()
        
        return self.clusters
    
    def analyze_clusters(self):
        """Analyze the characteristics of each cluster"""
        print(f"\n📊 Analyzing Cluster Characteristics...")
        
        cluster_summary = []
        
        for cluster_id in sorted(self.data['cluster'].unique()):
            cluster_data = self.data[self.data['cluster'] == cluster_id]
            size = len(cluster_data)
            
            summary = {
                'Cluster': cluster_id,
                'Size': size,
                'Percentage': f"{size/len(self.data)*100:.1f}%",
                'Avg_Age': f"{cluster_data['age'].mean():.1f}",
                'Most_Common_Gender': cluster_data['sex'].mode().iloc[0] if not cluster_data['sex'].mode().empty else 'N/A',
                'Most_Common_Occupation': cluster_data['occ_nm'].mode().iloc[0] if not cluster_data['occ_nm'].mode().empty else 'N/A',
                'Avg_Year': f"{cluster_data['arv_yr'].mean():.0f}",
                'Most_Common_Port': cluster_data['port_arv'].mode().iloc[0] if not cluster_data['port_arv'].mode().empty else 'N/A'
            }
            cluster_summary.append(summary)
        
        cluster_df = pd.DataFrame(cluster_summary)
        print("\n" + "="*100)
        print("CLUSTER CHARACTERISTICS SUMMARY")
        print("="*100)
        print(cluster_df.to_string(index=False))
        
        return cluster_df
    
    def build_prediction_models(self):
        """Build prediction models for each target variable"""
        print(f"\n🤖 Building Prediction Models...")
        
        X = self.processed_data
        
        for target in self.target_columns:
            if target not in self.data.columns:
                print(f"   ⚠️  Skipping {target} - column not found")
                continue
                
            print(f"\n   Training model for: {target}")
            
            # Get target variable (remove rows with missing targets)
            target_data = self.data[target].dropna()
            X_target = X.loc[target_data.index]
            y_target = target_data
            
            if len(y_target) == 0:
                print(f"     ❌ No data available for {target}")
                continue
            
            # Determine if classification or regression
            if y_target.dtype == 'object' or len(y_target.unique()) < 20:
                # Classification
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model_type = 'classification'
            else:
                # Regression
                model = RandomForestRegressor(n_estimators=100, random_state=42)
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
                accuracy = accuracy_score(y_test, y_pred)
                print(f"     ✅ Accuracy: {accuracy:.3f}")
                metric = accuracy
            else:
                mse = mean_squared_error(y_test, y_pred)
                print(f"     ✅ MSE: {mse:.3f}")
                metric = mse
            
            # Store model
            self.prediction_models[target] = {
                'model': model,
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
        
        print(f"   Input data shape: {input_df.shape}")
        
        # Prepare input features (same preprocessing as training data)
        X_input = input_df[self.feature_columns].copy()
        
        # Apply same encoding and scaling
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
        
        # Make predictions
        predictions = {}
        
        for target, model_info in self.prediction_models.items():
            try:
                pred = model_info['model'].predict(X_input)
                predictions[target] = pred[0] if len(pred) == 1 else pred
                print(f"   ✅ {target}: {predictions[target]}")
            except Exception as e:
                print(f"   ❌ Error predicting {target}: {e}")
                predictions[target] = None
        
        return predictions
    
    def create_user_interface(self):
        """Create an interactive interface for user input"""
        print(f"\n🖥️  Creating User Interface...")
        
        # Get unique values for categorical inputs
        unique_values = {
            'sex': sorted(self.data['sex'].unique()),
            'age_range': ['Child (0-18)', 'Young Adult (19-30)', 'Adult (31-45)', 'Middle Age (46-60)', 'Senior (60+)'],
            'occID': sorted(self.data['occID'].unique()),
            'arv_yr': sorted(self.data['arv_yr'].unique()),
            'lkrID': sorted(self.data['lkrID'].unique()),
            'travel_grp_size': sorted(self.data['travel_grp_size'].unique())
        }
        
        print(f"   Available options for each field:")
        for field, values in unique_values.items():
            print(f"     {field}: {len(values)} unique values (range: {min(values)} to {max(values)})")
        
        return unique_values
    
    def visualize_clusters(self):
        """Visualize the clustering results"""
        print(f"\n📈 Creating Cluster Visualizations...")
        
        # PCA for dimensionality reduction
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.processed_data)
        
        # Create visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. PCA scatter plot colored by clusters
        scatter = ax1.scatter(X_pca[:, 0], X_pca[:, 1], c=self.clusters, cmap='tab10', alpha=0.6)
        ax1.set_title('Hierarchical Clusters (PCA Visualization)')
        ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        plt.colorbar(scatter, ax=ax1)
        
        # 2. Cluster size distribution
        cluster_counts = pd.Series(self.clusters).value_counts().sort_index()
        ax2.bar(cluster_counts.index, cluster_counts.values)
        ax2.set_title('Cluster Size Distribution')
        ax2.set_xlabel('Cluster ID')
        ax2.set_ylabel('Number of Passengers')
        
        # 3. Average age by cluster
        age_by_cluster = self.data.groupby('cluster')['age'].mean()
        ax3.bar(age_by_cluster.index, age_by_cluster.values)
        ax3.set_title('Average Age by Cluster')
        ax3.set_xlabel('Cluster ID')
        ax3.set_ylabel('Average Age')
        
        # 4. Gender distribution by cluster
        gender_dist = self.data.groupby(['cluster', 'sex']).size().unstack(fill_value=0)
        gender_dist.plot(kind='bar', stacked=True, ax=ax4)
        ax4.set_title('Gender Distribution by Cluster')
        ax4.set_xlabel('Cluster ID')
        ax4.set_ylabel('Number of Passengers')
        ax4.legend(title='Gender')
        ax4.tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        plt.savefig('passenger_clustering_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"   ✅ Visualization saved as 'passenger_clustering_analysis.png'")

def main():
    """Main execution function"""
    print("="*60)
    print("TRANS-ATLANTIC VOYAGERS PASSENGER PREDICTION MODEL")
    print("="*60)
    
    # Initialize predictor
    predictor = PassengerPredictor()
    
    # Load and prepare data
    data = predictor.load_and_prepare_data()
    
    # Prepare features
    X = predictor.prepare_features_and_targets()
    
    # Perform clustering
    clusters = predictor.perform_hierarchical_clustering()
    
    # Build prediction models
    models = predictor.build_prediction_models()
    
    # Create visualizations
    predictor.visualize_clusters()
    
    # Create user interface options
    ui_options = predictor.create_user_interface()
    
    print(f"\n" + "="*60)
    print("MODEL TRAINING COMPLETE! 🎉")
    print("="*60)
    
    print(f"\n📊 Model Summary:")
    print(f"   • Training data: {len(data):,} passengers")
    print(f"   • Features: {len(predictor.feature_columns)} input variables")
    print(f"   • Clusters: {len(np.unique(clusters))} passenger groups")
    print(f"   • Prediction models: {len(models)} target variables")
    
    print(f"\n🎯 Available Predictions:")
    for target, model_info in models.items():
        print(f"   • {target}: {model_info['type']} (accuracy/MSE: {model_info['metric']:.3f})")
    
    # Example prediction
    print(f"\n🔮 Example Prediction:")
    example_input = {
        'sex': 'M',
        'age_range': 'Young Adult (19-30)',
        'occID': 210,  # Common occupation ID
        'arv_yr': 1890,
        'lkrID': 2,  # Common residence ID
        'travel_grp_size': 1
    }
    
    print(f"   Input: {example_input}")
    try:
        predictions = predictor.predict_passenger_characteristics(example_input)
        print(f"   Predictions: {predictions}")
    except Exception as e:
        print(f"   ❌ Example prediction failed: {e}")
    
    return predictor

if __name__ == "__main__":
    predictor = main()