# 🤖 ML-Enhanced Passenger Data Generator

A machine learning-powered system for generating realistic passenger data from the Trans-Atlantic Voyagers dataset (1834-1897) using clustering algorithms and historical patterns.

## 🚀 Features

### **Machine Learning Clustering**
- **K-means clustering** for passenger segmentation (6 clusters)
- **PCA dimensionality reduction** for optimal performance
- **Cluster-based voyage selection** using demographic patterns
- **Travel group size prediction** based on historical patterns

### **Smart Logic**
- **Age-appropriate occupation/family role selection**
- **Gender-aware family role assignment**
- **Dynamic form behavior** (occupation vs family role dropdowns)
- **Real-time validation** and error handling

### **Web Interface**
- **Modern, responsive UI** with ML statistics
- **Dynamic dropdowns** based on user selection
- **Real-time travel group prediction**
- **Cluster visualization** and statistics

## 📊 System Statistics

- **527,394** passenger records processed
- **681** occupation categories available
- **10,761** voyage records analyzed
- **781** ship records included
- **6** passenger clusters created
- **150** voyage clusters generated

## 🛠️ Installation

### **Prerequisites**
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-pandas python3-numpy python3-sklearn python3-matplotlib python3-seaborn python3-flask python3-venv
```

### **Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/ml-passenger-generator.git
cd ml-passenger-generator
```

### **Run the Application**
```bash
# Start the ML-enhanced web application
python3 ml_web_passenger_generator.py
```

### **Access the Web Interface**
Open your browser to: `http://localhost:5000`

## 🎯 Usage

### **Web Interface**
1. **Enter passenger criteria**: Gender, Age, Year, Country
2. **Select occupation status**: Has occupation (Yes/No)
3. **Choose specific role**:
   - If "Has occupation" → Select from occupation groups
   - If "No occupation" → Select from family roles
4. **Generate passenger data** with ML clustering
5. **View travel group prediction** and statistics

### **API Usage**
```bash
# Generate passenger with occupation
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "M",
    "age": 30,
    "hasOccupation": true,
    "occupationGroup": "Manufacturing and mining",
    "year": 1890,
    "country": "POLAND"
  }'

# Generate passenger with family role
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "F",
    "age": 25,
    "hasOccupation": false,
    "familyRole": "Wife",
    "year": 1885,
    "country": "RUSSIA"
  }'
```

## 📁 Project Structure

```
ml-passenger-generator/
├── ml_passenger_generator.py          # Core ML system
├── ml_web_passenger_generator.py      # Flask web application
├── templates/
│   └── ml_passenger_generator.html    # Web interface
├── dataverse_files/                   # Historical data
│   ├── ttav_passengers.csv
│   ├── ttav_occupations.csv
│   ├── ttav_voyages.csv
│   ├── ttav_ships.csv
│   └── ttav_routes.csv
├── README.md                          # This file
└── ML_UPDATE_SUMMARY.md              # Detailed update summary
```

## 🧠 Machine Learning Features

### **Clustering Algorithms**
```python
# Passenger Clustering
- Features: age, gender, year, occupation status
- Algorithm: K-means with PCA (6 clusters)
- Purpose: Find similar demographic patterns

# Voyage Clustering  
- Features: passenger count, voyage frequency, ship diversity
- Algorithm: K-means (4 clusters)
- Purpose: Group similar voyage characteristics
```

### **Travel Group Prediction**
- **Family patterns**: Analyze travel groups by family role
- **Occupation patterns**: Analyze travel groups by occupation
- **Age/gender patterns**: Consider demographic factors
- **Confidence levels**: High, medium, low, very_low

### **Age-Appropriate Logic**
```python
# Occupation Mapping
child (0-12): ['No occupation']
teen (13-17): ['No occupation', 'Manufacturing and mining', 'Service and hospitality']
young_adult (18-25): ['No occupation', 'Manufacturing and mining', 'Service and hospitality', 'Trade and commerce', 'Agriculture']
adult (26-65): [All occupation groups]
elderly (66-100): [Limited occupation groups]

# Family Role Mapping
child: ['Child', 'Son', 'Daughter', 'Infant']
teen: ['Child', 'Son', 'Daughter', 'Student']
young_adult: ['Head', 'Son', 'Daughter', 'Student', 'Servant']
adult: ['Head', 'Wife', 'Husband', 'Son', 'Daughter', 'Servant', 'Relative']
elderly: ['Head', 'Wife', 'Husband', 'Relative']
```

## 🌐 API Endpoints

### **Generate Passenger Data**
```http
POST /api/generate
Content-Type: application/json

{
  "gender": "M",
  "age": 30,
  "hasOccupation": true,
  "occupationGroup": "Manufacturing and mining",
  "year": 1890,
  "country": "POLAND"
}
```

### **Get Available Options**
```http
GET /api/options
```

### **Get Cluster Statistics**
```http
GET /api/clusters
```

### **Validate Input Data**
```http
POST /api/validate
Content-Type: application/json

{
  "gender": "M",
  "age": 30,
  "hasOccupation": true,
  "year": 1890,
  "country": "POLAND"
}
```

## 📊 Example Output

```json
{
  "gender": "M",
  "age": 30,
  "has_occupation": true,
  "occupation_group": "Manufacturing and mining",
  "family_role": null,
  "arv_yr": 1890,
  "country_of_origin": "POLAND",
  "ship_name": "WIELAND",
  "itinerary": "Hamburg-New York",
  "q_psgrs": 212,
  "port_arrival": "New York",
  "voyage_id": 81572,
  "travel_group_size": 2,
  "travel_group_stats": {
    "avg_group_size": 2.3,
    "median_group_size": 2.0,
    "max_group_size": 8,
    "min_group_size": 1
  },
  "prediction_confidence": "medium",
  "travel_pattern_description": "Adult working male in manufacturing and mining - may travel alone or with family"
}
```

## 🔧 Technical Details

### **Dependencies**
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms (K-means, PCA)
- **matplotlib/seaborn**: Data visualization
- **flask**: Web application framework

### **Performance**
- **Fast clustering**: PCA dimensionality reduction
- **Efficient memory usage**: Optimized data processing
- **Real-time predictions**: Cached cluster analysis
- **Robust error handling**: Fallback mechanisms

### **Data Sources**
- **Trans-Atlantic Voyagers Database**: Historical passenger records
- **Time period**: 1834-1897
- **Geographic scope**: Trans-Atlantic migration routes
- **Data quality**: Cleaned and validated historical records

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Trans-Atlantic Voyagers Database**: Historical passenger data
- **scikit-learn**: Machine learning algorithms
- **Flask**: Web framework
- **Historical migration research**: Academic sources

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Check the documentation in `ML_UPDATE_SUMMARY.md`
- Review the API examples above

---

**Built with ❤️ using Machine Learning and Historical Data**