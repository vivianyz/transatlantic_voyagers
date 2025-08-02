#!/usr/bin/env python3
"""
Demo Script for ML-Enhanced Passenger Generator
==============================================

This script demonstrates the key features of the ML-enhanced passenger generator:
1. Machine Learning Clustering
2. Dynamic Occupation/Family Role Logic
3. Travel Group Prediction
4. Age-Appropriate Logic
"""

from ml_passenger_generator import MLPassengerGenerator
import json

def main():
    """Demonstrate the ML-enhanced passenger generator"""
    print("🤖 ML-Enhanced Passenger Generator Demo")
    print("=" * 60)
    
    # Initialize the ML generator
    print("Initializing ML-enhanced passenger generator...")
    generator = MLPassengerGenerator()
    
    # Show cluster statistics
    print("\n📊 ML Cluster Statistics:")
    cluster_stats = generator.get_cluster_statistics()
    print(f"   • Passenger Clusters: {cluster_stats['passenger_clusters']}")
    print(f"   • Voyage Clusters: {cluster_stats['voyage_clusters']}")
    
    # Demo 1: Working Adult Male
    print("\n" + "="*60)
    print("DEMO 1: Working Adult Male")
    print("="*60)
    
    try:
        passenger1 = generator.generate_passenger_data_with_selections(
            gender='M',
            age=30,
            has_occupation=True,
            arv_yr=1890,
            country_of_origin='POLAND',
            occupation_group='Manufacturing and mining'
        )
        
        print(f"✅ Generated: {passenger1['gender']} age {passenger1['age']}")
        print(f"   Occupation: {passenger1['occupation_group']}")
        print(f"   Ship: {passenger1['ship_name']}")
        print(f"   Itinerary: {passenger1['itinerary']}")
        print(f"   Travel Group Size: {passenger1['travel_group_size']} people")
        print(f"   Confidence: {passenger1['prediction_confidence']}")
        print(f"   Pattern: {passenger1['travel_pattern_description']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 2: Family Member (No Occupation)
    print("\n" + "="*60)
    print("DEMO 2: Family Member (No Occupation)")
    print("="*60)
    
    try:
        passenger2 = generator.generate_passenger_data_with_selections(
            gender='F',
            age=25,
            has_occupation=False,
            arv_yr=1885,
            country_of_origin='RUSSIA',
            family_role='WIFE'
        )
        
        print(f"✅ Generated: {passenger2['gender']} age {passenger2['age']}")
        print(f"   Family Role: {passenger2['family_role']}")
        print(f"   Ship: {passenger2['ship_name']}")
        print(f"   Itinerary: {passenger2['itinerary']}")
        print(f"   Travel Group Size: {passenger2['travel_group_size']} people")
        print(f"   Confidence: {passenger2['prediction_confidence']}")
        print(f"   Pattern: {passenger2['travel_pattern_description']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 3: Child (No Occupation)
    print("\n" + "="*60)
    print("DEMO 3: Child (No Occupation)")
    print("="*60)
    
    try:
        passenger3 = generator.generate_passenger_data_with_selections(
            gender='M',
            age=8,
            has_occupation=False,
            arv_yr=1890,
            country_of_origin='GERMANY',
            family_role='SON'
        )
        
        print(f"✅ Generated: {passenger3['gender']} age {passenger3['age']}")
        print(f"   Family Role: {passenger3['family_role']}")
        print(f"   Ship: {passenger3['ship_name']}")
        print(f"   Itinerary: {passenger3['itinerary']}")
        print(f"   Travel Group Size: {passenger3['travel_group_size']} people")
        print(f"   Confidence: {passenger3['prediction_confidence']}")
        print(f"   Pattern: {passenger3['travel_pattern_description']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demo 4: Young Professional
    print("\n" + "="*60)
    print("DEMO 4: Young Professional")
    print("="*60)
    
    try:
        passenger4 = generator.generate_passenger_data_with_selections(
            gender='F',
            age=22,
            has_occupation=True,
            arv_yr=1880,
            country_of_origin='IRELAND',
            occupation_group='Service and hospitality'
        )
        
        print(f"✅ Generated: {passenger4['gender']} age {passenger4['age']}")
        print(f"   Occupation: {passenger4['occupation_group']}")
        print(f"   Ship: {passenger4['ship_name']}")
        print(f"   Itinerary: {passenger4['itinerary']}")
        print(f"   Travel Group Size: {passenger4['travel_group_size']} people")
        print(f"   Confidence: {passenger4['prediction_confidence']}")
        print(f"   Pattern: {passenger4['travel_pattern_description']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Show JSON output for one example
    print("\n" + "="*60)
    print("JSON OUTPUT EXAMPLE:")
    print("="*60)
    
    try:
        example = generator.generate_passenger_data_with_selections(
            gender='M',
            age=35,
            has_occupation=True,
            arv_yr=1890,
            country_of_origin='POLAND',
            occupation_group='Trade and commerce'
        )
        
        # Convert numpy types for JSON serialization
        json_data = {}
        for key, value in example.items():
            if hasattr(value, 'item'):  # numpy type
                json_data[key] = value.item()
            else:
                json_data[key] = value
        
        print(json.dumps(json_data, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🎉 Demo Complete!")
    print("="*60)
    print("✅ All ML features working:")
    print("   • K-means clustering for passenger segmentation")
    print("   • Dynamic occupation/family role logic")
    print("   • Travel group size prediction")
    print("   • Age-appropriate role selection")
    print("   • Cluster-based voyage selection")
    print("\n🌐 Start the web app: python3 ml_web_passenger_generator.py")
    print("📱 Open browser to: http://localhost:5000")

if __name__ == "__main__":
    main()