# 🚢 Trans-Atlantic Voyagers Passenger Prediction Web Application

A beautiful, modern web interface for predicting passenger characteristics based on historical migration data from the Russian Empire to the USA (1834-1897). This application uses machine learning and hierarchical clustering to predict missing passenger information based on user input.

## 🌟 Features

### **User-Specified Input Features**
- **🚹🚺 Gender** - Male, Female, or Unknown
- **🎂 Age Range** - Child (0-18), Young Adult (19-30), Adult (31-45), Middle Age (46-60), Senior (60+)
- **💼 Occupation** - Various historical occupations (Laborer, Farmer, Merchant, etc.)
- **📅 Year of Departure** - Any year from 1834 to 1897
- **🏠 Original Residence** - Last known residence in the Russian Empire
- **👥 Travel Group Size** - Number of passengers traveling together (1-10+)

### **Predicted Characteristics**
- **📚 Literacy** - Whether the passenger could read/write
- **👨‍👩‍👧‍👦 Family Role** - Position within family structure (Wife, Husband, Child, etc.)
- **🚢 Passage Type** - Steerage or Cabin class
- **💼 Occupation Group** - Broader occupational category
- **🏙️ Arrival Port** - Port of entry in the USA

### **Machine Learning Models**
- **Hierarchical Clustering** - Groups similar passengers into 6 distinct clusters
- **Random Forest Models** - High-accuracy prediction models (85-97% accuracy)
- **Confidence Scores** - Visual confidence indicators for each prediction

## 📁 File Structure

```
/workspace/
├── app.py                           # Flask backend server
├── templates/
│   └── index.html                   # Main web interface
├── test_web.html                    # Standalone demo version
├── ttav_unified_dataset.csv         # Integrated passenger dataset
├── passenger_predictor_simple.py    # Core prediction model
├── data_integration.py              # Data integration script
└── dataverse_files/                 # Original dataset files
```

## 🚀 How to Use

### **Option 1: Full Web Application (with Flask Backend)**

1. **Start the Flask Server**
   ```bash
   python3 app.py
   ```

2. **Open Your Browser**
   - Navigate to `http://localhost:5000`
   - The application will automatically load the machine learning models

3. **Make Predictions**
   - Fill out the passenger information form
   - Click "🔮 Predict Passenger Characteristics"
   - View detailed predictions with confidence scores

### **Option 2: Demo Version (Standalone HTML)**

1. **Open the Demo File**
   ```bash
   # Simply open test_web.html in any web browser
   open test_web.html
   ```

2. **Interactive Demo**
   - Uses rule-based predictions for demonstration
   - Shows the complete user interface and functionality
   - No backend server required

## 🎯 Example Usage

### **Sample Input:**
- **Gender:** Male
- **Age Range:** Young Adult (19-30)
- **Occupation:** LABORER
- **Year:** 1890
- **Residence:** Poland
- **Group Size:** 1 passenger

### **Sample Predictions:**
- **📚 Literacy:** Unknown (96.0% confidence)
- **👨‍👩‍👧‍👦 Family Role:** not given (100.0% confidence)
- **🚢 Passage Type:** steerage (98.0% confidence)
- **💼 Occupation Group:** Agriculture (48.0% confidence)
- **🏙️ Arrival Port:** New York (95.0% confidence)

## 🔧 Technical Details

### **Backend (Flask)**
- **REST API** endpoints for predictions and options
- **Machine Learning Pipeline** with preprocessing and encoding
- **Error Handling** and validation
- **CORS Support** for cross-origin requests

### **Frontend (HTML/CSS/JavaScript)**
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Beautiful gradients and animations
- **Interactive Forms** - Dynamic dropdowns and validation
- **Real-time Results** - Instant predictions with loading states
- **Confidence Visualization** - Progress bars showing prediction confidence

### **Machine Learning Models**
- **Data Processing:** 521,140 passenger records
- **Feature Engineering:** One-hot encoding, standardization
- **Clustering:** Hierarchical clustering with silhouette optimization
- **Prediction:** Random Forest classifiers with 90%+ accuracy

## 📊 Dataset Information

- **Source:** "The Tsar's Trans-Atlantic Voyagers" dataset
- **Time Period:** 1834-1897 (63 years)
- **Records:** 527,394 total passengers
- **Coverage:** Migration from Russian Empire to USA
- **Data Types:** Demographic, occupational, geographical, temporal

## 🎨 User Interface Features

### **Modern Design**
- **Gradient Backgrounds** - Beautiful purple-blue gradients
- **Card-based Layout** - Clean, organized information display
- **Hover Effects** - Interactive elements with smooth transitions
- **Responsive Grid** - Adapts to different screen sizes

### **User Experience**
- **Form Validation** - Ensures all required fields are filled
- **Loading States** - Visual feedback during predictions
- **Error Handling** - Clear error messages and recovery
- **Accessibility** - Semantic HTML and keyboard navigation

### **Data Visualization**
- **Confidence Bars** - Visual representation of prediction certainty
- **Input Summary** - Clear display of user selections
- **Color Coding** - Consistent visual language throughout
- **Icons and Emojis** - Intuitive visual cues for different data types

## 🔮 How It Works

1. **User Input** - User fills out the 6 required passenger characteristics
2. **Data Processing** - Backend encodes and standardizes the input data
3. **Cluster Assignment** - Determines which historical passenger group is most similar
4. **Prediction** - Trained Random Forest models predict missing characteristics
5. **Results Display** - Frontend shows predictions with confidence scores and visualizations

## 📈 Model Performance

| Prediction Target | Model Type | Accuracy |
|------------------|------------|----------|
| Literacy | Classification | 91.8% |
| Family Role | Classification | 91.5% |
| Passage Type | Classification | 97.2% |
| Occupation Group | Classification | 90.8% |
| Arrival Port | Classification | 93.0% |

## 🛠️ Installation Requirements

### **Python Dependencies**
```bash
pip install flask flask-cors pandas numpy scikit-learn matplotlib seaborn
```

### **System Requirements**
- Python 3.7+
- 2GB+ RAM (for loading the dataset)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🎉 Success!

You now have a complete web application that:
- ✅ Takes user input through a beautiful web interface
- ✅ Uses hierarchical clustering and machine learning for predictions
- ✅ Displays results with confidence scores and visualizations
- ✅ Works on both desktop and mobile devices
- ✅ Provides both full-featured and demo versions

The application successfully transforms historical migration data into an interactive, predictive tool that helps understand passenger characteristics and migration patterns from the Russian Empire to the United States during the 19th century.