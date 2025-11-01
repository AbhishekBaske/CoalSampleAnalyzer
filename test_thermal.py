"""
Coal Thermal Analysis Test Script

This script demonstrates the thermal simulation capabilities
by processing a sample of bituminous coal images from the dataset.
"""

import os
import sys
import random
from datetime import datetime

# Add the parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from thermal_simulator import ThermalSimulator
    from app import CoalSpontaneousAnalyzer
    
    print("🔥 Coal Thermal Analysis Test Script")
    print("=" * 50)
    
    # Initialize components
    thermal_sim = ThermalSimulator()
    coal_analyzer = CoalSpontaneousAnalyzer()
    
    # Dataset path
    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'Bituminous')
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at: {dataset_path}")
        print("Please ensure the dataset/Bituminous folder contains coal images.")
        sys.exit(1)
    
    # Get available images
    image_files = [f for f in os.listdir(dataset_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ No coal images found in dataset folder")
        sys.exit(1)
    
    print(f"📁 Found {len(image_files)} coal sample images")
    
    # Test with a few random samples
    test_samples = random.sample(image_files, min(5, len(image_files)))
    
    print(f"🧪 Testing thermal analysis on {len(test_samples)} samples...")
    print()
    
    results = []
    
    for i, image_name in enumerate(test_samples, 1):
        print(f"[{i}/{len(test_samples)}] Processing {image_name}...")
        
        try:
            image_path = os.path.join(dataset_path, image_name)
            
            # Analyze image features
            print("  📊 Analyzing image features...")
            features = thermal_sim.analyze_image_features(image_path)
            
            if not features:
                print("  ❌ Failed to analyze image features")
                continue
            
            # Generate environmental parameters
            scenario = random.choice(['normal', 'hot_day', 'humid', 'poor_ventilation'])
            print(f"  🌡️  Generating environmental conditions ({scenario})...")
            env_params = thermal_sim.generate_environmental_parameters(features, scenario)
            
            # Generate coal properties
            print("  ⚗️  Generating coal properties...")
            coal_props = thermal_sim.generate_coal_properties_from_image(features, env_params)
            
            # Simulate thermal distribution
            print("  🔥 Simulating thermal distribution...")
            thermal_map, temp_map = thermal_sim.simulate_thermal_distribution(image_path, env_params)
            
            if thermal_map is None:
                print("  ❌ Failed to simulate thermal distribution")
                continue
            
            # Calculate temperature statistics
            temp_stats = {
                'min_temp': float(temp_map.min()),
                'max_temp': float(temp_map.max()),
                'avg_temp': float(temp_map.mean()),
                'hot_spot_count': int((temp_map > (temp_map.mean() + 2 * temp_map.std())).sum()),
                'critical_area_percentage': float((temp_map > 80).sum() / temp_map.size * 100)
            }
            
            # Perform coal analysis
            print("  📈 Performing coal analysis...")
            cpt = coal_analyzer.crossing_point_temperature(
                coal_props['moisture'], coal_props['volatile_matter'],
                coal_props['ash'], coal_props['fixed_carbon']
            )
            
            li = coal_analyzer.liability_index(
                coal_props['moisture'], coal_props['volatile_matter'], coal_props['ash']
            )
            
            wits = coal_analyzer.wits_index(
                coal_props['moisture'], coal_props['volatile_matter'],
                coal_props['ash'], env_params['oxygen_content']
            )
            
            # Risk assessment
            thermal_risk = thermal_sim.assess_thermal_risk(temp_map, temp_stats)
            standard_risk = coal_analyzer.risk_assessment(
                cpt, li, wits, None, env_params['ambient_temperature'], env_params['wind_speed']
            )
            
            combined_risk_score = (standard_risk['risk_score'] + thermal_risk['thermal_risk_score']) / 2
            
            # Store results
            result = {
                'image': image_name,
                'scenario': scenario,
                'features': features,
                'env_params': env_params,
                'coal_properties': coal_props,
                'temp_stats': temp_stats,
                'indices': {'cpt': cpt, 'li': li, 'wits': wits},
                'thermal_risk_score': thermal_risk['thermal_risk_score'],
                'standard_risk_score': standard_risk['risk_score'],
                'combined_risk_score': combined_risk_score
            }
            
            results.append(result)
            
            # Print summary
            print(f"  ✅ Analysis complete!")
            print(f"     Max Temperature: {temp_stats['max_temp']:.1f}°C")
            print(f"     CPT: {cpt:.1f}°C" if cpt else "     CPT: N/A")
            print(f"     Combined Risk Score: {combined_risk_score:.1f}/100")
            print(f"     Risk Level: {'CRITICAL' if combined_risk_score >= 80 else 'HIGH' if combined_risk_score >= 60 else 'MODERATE' if combined_risk_score >= 40 else 'LOW'}")
            print()
            
        except Exception as e:
            print(f"  ❌ Error processing {image_name}: {e}")
            continue
    
    # Summary report
    print("=" * 50)
    print("📋 THERMAL ANALYSIS SUMMARY REPORT")
    print("=" * 50)
    
    if results:
        print(f"Total samples analyzed: {len(results)}")
        print(f"Average max temperature: {sum(r['temp_stats']['max_temp'] for r in results) / len(results):.1f}°C")
        print(f"Average combined risk score: {sum(r['combined_risk_score'] for r in results) / len(results):.1f}/100")
        
        # Risk distribution
        critical = sum(1 for r in results if r['combined_risk_score'] >= 80)
        high = sum(1 for r in results if 60 <= r['combined_risk_score'] < 80)
        moderate = sum(1 for r in results if 40 <= r['combined_risk_score'] < 60)
        low = sum(1 for r in results if r['combined_risk_score'] < 40)
        
        print(f"\nRisk Level Distribution:")
        print(f"  Critical Risk: {critical} samples")
        print(f"  High Risk: {high} samples")
        print(f"  Moderate Risk: {moderate} samples")
        print(f"  Low Risk: {low} samples")
        
        # Highest risk sample
        highest_risk = max(results, key=lambda x: x['combined_risk_score'])
        print(f"\nHighest Risk Sample:")
        print(f"  Image: {highest_risk['image']}")
        print(f"  Scenario: {highest_risk['scenario']}")
        print(f"  Max Temperature: {highest_risk['temp_stats']['max_temp']:.1f}°C")
        print(f"  Risk Score: {highest_risk['combined_risk_score']:.1f}/100")
        
        # Environmental factors
        scenarios = {}
        for result in results:
            scenario = result['scenario']
            scenarios[scenario] = scenarios.get(scenario, 0) + 1
        
        print(f"\nEnvironmental Scenarios:")
        for scenario, count in scenarios.items():
            print(f"  {scenario.replace('_', ' ').title()}: {count} samples")
        
        print(f"\n🎉 Thermal analysis test completed successfully!")
        print(f"⏰ Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    else:
        print("❌ No samples were successfully analyzed")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)