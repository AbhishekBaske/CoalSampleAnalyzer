from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import math
import logging
import os
import random
import numpy as np
from datetime import datetime
from thermal_simulator import ThermalSimulator

def convert_numpy_types(obj):
    """Convert NumPy types to Python native types for JSON serialization"""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

app = Flask(__name__)
app.secret_key = 'coal_spontaneous_analyzer_2025'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize thermal simulator
thermal_simulator = ThermalSimulator()

# Dataset path
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset', 'Bituminous')

class CoalSpontaneousAnalyzer:
    """
    Coal Spontaneous Combustion Analyzer
    
    This class implements various methods to assess the risk of spontaneous combustion
    in coal based on different properties and environmental conditions.
    """
    
    def __init__(self):
        self.analysis_results = {}
    
    def crossing_point_temperature(self, moisture, volatile_matter, ash, fixed_carbon):
        """
        Calculate Crossing Point Temperature (CPT) - a key indicator of spontaneous combustion
        
        CPT is the temperature at which the rate of heat generation exceeds heat dissipation
        Lower CPT indicates higher risk of spontaneous combustion
        
        Formula based on Sharma et al. (2020) research
        """
        try:
            # Normalize values to percentages if needed
            total = moisture + volatile_matter + ash + fixed_carbon
            if total > 100:
                moisture = (moisture / total) * 100
                volatile_matter = (volatile_matter / total) * 100
                ash = (ash / total) * 100
                fixed_carbon = (fixed_carbon / total) * 100
            
            # CPT calculation (empirical formula)
            cpt = 150 + (0.3 * ash) - (0.5 * volatile_matter) + (0.2 * moisture) + (0.1 * fixed_carbon)
            
            return max(120, min(200, cpt))  # Reasonable bounds for CPT
        except Exception as e:
            logger.error(f"Error calculating CPT: {e}")
            return None
    
    def liability_index(self, moisture, volatile_matter, ash):
        """
        Calculate Liability Index for spontaneous combustion
        
        Higher values indicate greater liability to spontaneous combustion
        Based on Banerjee (2000) methodology
        """
        try:
            if ash == 0:
                return None
            
            li = (moisture * volatile_matter) / ash
            return round(li, 2)
        except Exception as e:
            logger.error(f"Error calculating Liability Index: {e}")
            return None
    
    def wits_index(self, moisture, volatile_matter, ash, oxygen):
        """
        Calculate WITS Index (Wits-Ehac Index)
        
        Developed at University of Witwatersrand for predicting spontaneous combustion
        """
        try:
            # WITS index calculation
            wits = (moisture + volatile_matter) * oxygen / (ash + 1)
            return round(wits, 2)
        except Exception as e:
            logger.error(f"Error calculating WITS Index: {e}")
            return None
    
    def olpinski_index(self, moisture, volatile_matter, ash):
        """
        Calculate Olpinski Index for spontaneous combustion liability
        """
        try:
            if (ash + volatile_matter) == 0:
                return None
            
            oi = moisture / (ash + volatile_matter)
            return round(oi, 3)
        except Exception as e:
            logger.error(f"Error calculating Olpinski Index: {e}")
            return None
    
    def risk_assessment(self, cpt, li, wits, oi, ambient_temp, ventilation_rate):
        """
        Comprehensive risk assessment based on all calculated indices
        """
        risk_factors = []
        risk_score = 0
        
        # CPT Risk Assessment
        if cpt:
            if cpt < 140:
                risk_factors.append("Very High CPT Risk (CPT < 140°C)")
                risk_score += 40
            elif cpt < 150:
                risk_factors.append("High CPT Risk (CPT 140-150°C)")
                risk_score += 30
            elif cpt < 160:
                risk_factors.append("Moderate CPT Risk (CPT 150-160°C)")
                risk_score += 20
            else:
                risk_factors.append("Low CPT Risk (CPT > 160°C)")
                risk_score += 10
        
        # Liability Index Risk Assessment
        if li:
            if li > 2.0:
                risk_factors.append("High Liability Index Risk (LI > 2.0)")
                risk_score += 25
            elif li > 1.0:
                risk_factors.append("Moderate Liability Index Risk (LI 1.0-2.0)")
                risk_score += 15
            else:
                risk_factors.append("Low Liability Index Risk (LI < 1.0)")
                risk_score += 5
        
        # WITS Index Risk Assessment
        if wits:
            if wits > 5.0:
                risk_factors.append("High WITS Index Risk (WITS > 5.0)")
                risk_score += 20
            elif wits > 2.0:
                risk_factors.append("Moderate WITS Index Risk (WITS 2.0-5.0)")
                risk_score += 10
            else:
                risk_factors.append("Low WITS Index Risk (WITS < 2.0)")
                risk_score += 5
        
        # Environmental factors
        if ambient_temp > 30:
            risk_factors.append("High Ambient Temperature Risk (> 30°C)")
            risk_score += 15
        
        if ventilation_rate < 0.5:
            risk_factors.append("Poor Ventilation Risk (< 0.5 m/s)")
            risk_score += 15
        
        # Overall risk classification
        if risk_score >= 80:
            overall_risk = "CRITICAL"
            color = "danger"
        elif risk_score >= 60:
            overall_risk = "HIGH"
            color = "warning"
        elif risk_score >= 40:
            overall_risk = "MODERATE"
            color = "info"
        else:
            overall_risk = "LOW"
            color = "success"
        
        return {
            'overall_risk': overall_risk,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'color': color
        }
    
    def generate_recommendations(self, risk_level, risk_factors, cpt):
        """
        Generate specific recommendations based on risk assessment
        """
        recommendations = []
        
        if risk_level in ["CRITICAL", "HIGH"]:
            recommendations.extend([
                "Implement immediate monitoring systems for temperature and gas emissions",
                "Increase ventilation rates to minimum 1.0 m/s",
                "Consider water spraying or foam injection for temperature control",
                "Establish regular thermal imaging surveys",
                "Implement CO monitoring systems"
            ])
        
        if risk_level in ["CRITICAL", "HIGH", "MODERATE"]:
            recommendations.extend([
                "Regular inspection of coal stockpiles every 2-4 hours",
                "Maintain maximum pile height of 3-4 meters",
                "Ensure proper drainage to prevent moisture accumulation",
                "Consider coal blending to reduce volatile matter content"
            ])
        
        if "Poor Ventilation" in str(risk_factors):
            recommendations.append("Install or upgrade ventilation systems immediately")
        
        if "High Ambient Temperature" in str(risk_factors):
            recommendations.append("Implement cooling measures during hot weather")
        
        if cpt and cpt < 145:
            recommendations.append("Consider relocating coal to cooler storage areas")
        
        if not recommendations:
            recommendations = [
                "Continue regular monitoring procedures",
                "Maintain current storage practices",
                "Review conditions monthly"
            ]
        
        return recommendations

# Initialize analyzer
analyzer = CoalSpontaneousAnalyzer()

@app.route('/')
def index():
    """Home page with coal analysis form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process coal analysis request"""
    try:
        # Get form data
        data = request.get_json() if request.is_json else request.form
        
        # Extract coal properties
        moisture = float(data.get('moisture', 0))
        volatile_matter = float(data.get('volatile_matter', 0))
        ash = float(data.get('ash', 0))
        fixed_carbon = float(data.get('fixed_carbon', 0))
        oxygen = float(data.get('oxygen', 20.9))  # Default atmospheric oxygen
        
        # Environmental conditions
        ambient_temp = float(data.get('ambient_temp', 25))
        ventilation_rate = float(data.get('ventilation_rate', 1.0))
        
        # Coal identification
        coal_type = data.get('coal_type', 'Unknown')
        location = data.get('location', 'Not specified')
        
        # Perform calculations
        cpt = analyzer.crossing_point_temperature(moisture, volatile_matter, ash, fixed_carbon)
        li = analyzer.liability_index(moisture, volatile_matter, ash)
        wits = analyzer.wits_index(moisture, volatile_matter, ash, oxygen)
        oi = analyzer.olpinski_index(moisture, volatile_matter, ash)
        
        # Risk assessment
        risk_assessment = analyzer.risk_assessment(
            cpt, li, wits, oi, ambient_temp, ventilation_rate
        )
        
        # Generate recommendations
        recommendations = analyzer.generate_recommendations(
            risk_assessment['overall_risk'], 
            risk_assessment['risk_factors'],
            cpt
        )
        
        # Prepare results
        results = {
            'coal_info': {
                'type': coal_type,
                'location': location,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'input_data': {
                'moisture': moisture,
                'volatile_matter': volatile_matter,
                'ash': ash,
                'fixed_carbon': fixed_carbon,
                'oxygen': oxygen,
                'ambient_temp': ambient_temp,
                'ventilation_rate': ventilation_rate
            },
            'calculated_indices': {
                'cpt': cpt,
                'liability_index': li,
                'wits_index': wits,
                'olpinski_index': oi
            },
            'risk_assessment': risk_assessment,
            'recommendations': recommendations
        }
        
        return render_template('results.html', results=results)
        
    except ValueError as e:
        logger.error(f"Invalid input data: {e}")
        return render_template('index.html', error="Please enter valid numeric values for all fields.")
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return render_template('index.html', error="An error occurred during analysis. Please try again.")

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for coal analysis"""
    try:
        data = request.get_json()
        
        # Perform the same analysis as the web interface
        moisture = float(data.get('moisture', 0))
        volatile_matter = float(data.get('volatile_matter', 0))
        ash = float(data.get('ash', 0))
        fixed_carbon = float(data.get('fixed_carbon', 0))
        oxygen = float(data.get('oxygen', 20.9))
        ambient_temp = float(data.get('ambient_temp', 25))
        ventilation_rate = float(data.get('ventilation_rate', 1.0))
        
        cpt = analyzer.crossing_point_temperature(moisture, volatile_matter, ash, fixed_carbon)
        li = analyzer.liability_index(moisture, volatile_matter, ash)
        wits = analyzer.wits_index(moisture, volatile_matter, ash, oxygen)
        oi = analyzer.olpinski_index(moisture, volatile_matter, ash)
        
        risk_assessment = analyzer.risk_assessment(
            cpt, li, wits, oi, ambient_temp, ventilation_rate
        )
        
        recommendations = analyzer.generate_recommendations(
            risk_assessment['overall_risk'], 
            risk_assessment['risk_factors'],
            cpt
        )
        
        return jsonify({
            'success': True,
            'calculated_indices': {
                'cpt': cpt,
                'liability_index': li,
                'wits_index': wits,
                'olpinski_index': oi
            },
            'risk_assessment': risk_assessment,
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"API analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/thermal')
def thermal_analysis():
    """Thermal analysis page with dataset images"""
    try:
        # Get list of available coal images
        if os.path.exists(DATASET_PATH):
            image_files = [f for f in os.listdir(DATASET_PATH) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            image_files.sort()
        else:
            image_files = []
        
        return render_template('thermal.html', images=image_files)
    except Exception as e:
        logger.error(f"Error loading thermal analysis page: {e}")
        return render_template('thermal.html', images=[], error="Could not load coal images")

@app.route('/thermal_analyze/<image_name>')
def analyze_thermal_image(image_name):
    """Analyze specific coal image with thermal simulation"""
    try:
        image_path = os.path.join(DATASET_PATH, image_name)
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        
        # Analyze image features
        image_features = thermal_simulator.analyze_image_features(image_path)
        if not image_features:
            return jsonify({'error': 'Could not analyze image'}), 500
        
        # Generate environmental parameters (random scenario)
        scenarios = ['normal', 'hot_day', 'humid', 'poor_ventilation']
        scenario = random.choice(scenarios)
        env_params = thermal_simulator.generate_environmental_parameters(image_features, scenario)
        
        # Generate coal properties from image
        coal_properties = thermal_simulator.generate_coal_properties_from_image(image_features, env_params)
        
        # Simulate thermal distribution
        thermal_map, temperature_map = thermal_simulator.simulate_thermal_distribution(image_path, env_params)
        if thermal_map is None:
            return jsonify({'error': 'Could not simulate thermal distribution'}), 500
        
        # Create thermal visualization
        try:
            thermal_image_b64, temp_stats = thermal_simulator.create_thermal_visualization(
                thermal_map, temperature_map, image_path
            )
            if not thermal_image_b64:
                # Fallback: calculate basic temp stats without visualization
                temp_stats = {
                    'min_temp': float(temperature_map.min()),
                    'max_temp': float(temperature_map.max()),
                    'avg_temp': float(temperature_map.mean()),
                    'hot_spot_count': int((temperature_map > (temperature_map.mean() + 2 * temperature_map.std())).sum()),
                    'critical_area_percentage': float((temperature_map > 80).sum() / temperature_map.size * 100)
                }
                thermal_image_b64 = None
        except Exception as viz_error:
            logger.error(f"Visualization error: {viz_error}")
            # Fallback: calculate basic temp stats without visualization
            temp_stats = {
                'min_temp': float(temperature_map.min()),
                'max_temp': float(temperature_map.max()),
                'avg_temp': float(temperature_map.mean()),
                'hot_spot_count': int((temperature_map > (temperature_map.mean() + 2 * temperature_map.std())).sum()),
                'critical_area_percentage': float((temperature_map > 80).sum() / temperature_map.size * 100)
            }
            thermal_image_b64 = None
        
        # Assess thermal risk
        thermal_risk = thermal_simulator.assess_thermal_risk(temperature_map, temp_stats)
        
        # Perform standard coal analysis with generated properties
        cpt = analyzer.crossing_point_temperature(
            coal_properties['moisture'], 
            coal_properties['volatile_matter'], 
            coal_properties['ash'], 
            coal_properties['fixed_carbon']
        )
        li = analyzer.liability_index(
            coal_properties['moisture'], 
            coal_properties['volatile_matter'], 
            coal_properties['ash']
        )
        wits = analyzer.wits_index(
            coal_properties['moisture'], 
            coal_properties['volatile_matter'], 
            coal_properties['ash'], 
            env_params['oxygen_content']
        )
        oi = analyzer.olpinski_index(
            coal_properties['moisture'], 
            coal_properties['volatile_matter'], 
            coal_properties['ash']
        )
        
        # Combined risk assessment (standard + thermal)
        standard_risk = analyzer.risk_assessment(
            cpt, li, wits, oi, env_params['ambient_temperature'], env_params['wind_speed']
        )
        
        # Combine thermal and standard risk scores
        combined_risk_score = (standard_risk['risk_score'] + thermal_risk['thermal_risk_score']) / 2
        all_risk_factors = standard_risk['risk_factors'] + thermal_risk['thermal_risk_factors']
        
        # Determine overall risk level
        if combined_risk_score >= 80:
            overall_risk = "CRITICAL"
            color = "danger"
        elif combined_risk_score >= 60:
            overall_risk = "HIGH"
            color = "warning"
        elif combined_risk_score >= 40:
            overall_risk = "MODERATE"
            color = "info"
        else:
            overall_risk = "LOW"
            color = "success"
        
        combined_risk_assessment = {
            'overall_risk': overall_risk,
            'risk_score': combined_risk_score,
            'risk_factors': all_risk_factors,
            'color': color,
            'standard_risk_score': standard_risk['risk_score'],
            'thermal_risk_score': thermal_risk['thermal_risk_score']
        }
        
        # Generate comprehensive recommendations
        recommendations = analyzer.generate_recommendations(
            overall_risk, all_risk_factors, cpt
        )
        
        # Add thermal-specific recommendations
        if thermal_risk['thermal_risk_score'] > 50:
            thermal_recommendations = [
                "Implement continuous thermal monitoring with infrared cameras",
                "Establish thermal alert zones around detected hot spots",
                "Consider immediate pile restructuring to break up hot zones"
            ]
            recommendations.extend(thermal_recommendations)
        
        # Prepare comprehensive results
        results = {
            'image_info': {
                'filename': image_name,
                'scenario': scenario.replace('_', ' ').title(),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'image_features': image_features,
            'environmental_params': env_params,
            'coal_properties': coal_properties,
            'calculated_indices': {
                'cpt': cpt,
                'liability_index': li,
                'wits_index': wits,
                'olpinski_index': oi
            },
            'thermal_analysis': {
                'thermal_image': thermal_image_b64,
                'temperature_stats': temp_stats,
                'thermal_risk': thermal_risk
            },
            'combined_risk_assessment': combined_risk_assessment,
            'recommendations': recommendations
        }
        
        # Convert any NumPy types before rendering
        results = convert_numpy_types(results)
        return render_template('thermal_results.html', results=results)
        
    except Exception as e:
        logger.error(f"Error in thermal analysis: {e}")
        return render_template('thermal.html', error=f"Analysis failed: {str(e)}")

@app.route('/dataset/<path:filename>')
def dataset_image(filename):
    """Serve dataset images"""
    return send_from_directory(DATASET_PATH, filename)

@app.route('/batch_thermal_analysis')
def batch_thermal_analysis():
    """Run thermal analysis on multiple images for comparison"""
    try:
        if not os.path.exists(DATASET_PATH):
            return jsonify({'error': 'Dataset not found'}), 404
        
        image_files = [f for f in os.listdir(DATASET_PATH) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Analyze random sample of images (limit to prevent timeout)
        sample_size = min(10, len(image_files))
        sample_images = random.sample(image_files, sample_size)
        
        batch_results = []
        
        for image_name in sample_images:
            try:
                image_path = os.path.join(DATASET_PATH, image_name)
                
                # Quick analysis for batch processing
                image_features = thermal_simulator.analyze_image_features(image_path)
                if not image_features:
                    continue
                
                # Generate environmental parameters
                scenario = random.choice(['normal', 'hot_day', 'humid', 'poor_ventilation'])
                env_params = thermal_simulator.generate_environmental_parameters(image_features, scenario)
                
                # Generate coal properties
                coal_properties = thermal_simulator.generate_coal_properties_from_image(image_features, env_params)
                
                # Quick thermal simulation (smaller resolution for speed)
                thermal_map, temperature_map = thermal_simulator.simulate_thermal_distribution(image_path, env_params)
                if thermal_map is None:
                    continue
                
                # Calculate temperature statistics
                temp_stats = {
                    'min_temp': float(temperature_map.min()),
                    'max_temp': float(temperature_map.max()),
                    'avg_temp': float(temperature_map.mean()),
                    'critical_area_percentage': float((temperature_map > 80).sum() / temperature_map.size * 100),
                    'hot_spot_count': int((temperature_map > (temperature_map.mean() + 2 * temperature_map.std())).sum())
                }
                
                # Standard analysis
                cpt = analyzer.crossing_point_temperature(
                    coal_properties['moisture'], coal_properties['volatile_matter'], 
                    coal_properties['ash'], coal_properties['fixed_carbon']
                )
                
                # Risk assessment
                thermal_risk = thermal_simulator.assess_thermal_risk(temperature_map, temp_stats)
                standard_risk = analyzer.risk_assessment(
                    cpt, None, None, None, env_params['ambient_temperature'], env_params['wind_speed']
                )
                
                combined_risk_score = (standard_risk['risk_score'] + thermal_risk['thermal_risk_score']) / 2
                
                batch_results.append({
                    'image_name': image_name,
                    'scenario': scenario,
                    'max_temp': temp_stats['max_temp'],
                    'avg_temp': temp_stats['avg_temp'],
                    'critical_area_percentage': temp_stats['critical_area_percentage'],
                    'combined_risk_score': combined_risk_score,
                    'cpt': cpt,
                    'coal_properties': coal_properties,
                    'env_params': {
                        'ambient_temperature': env_params['ambient_temperature'],
                        'wind_speed': env_params['wind_speed'],
                        'relative_humidity': env_params['relative_humidity']
                    }
                })
                
            except Exception as e:
                logger.error(f"Error processing {image_name}: {e}")
                continue
        
        # Sort by risk score
        batch_results.sort(key=lambda x: x['combined_risk_score'], reverse=True)
        
        # Handle empty results
        if not batch_results:
            return render_template('batch_results.html', results=[], error="No samples could be processed successfully")
        
        # Convert any NumPy types before rendering
        batch_results = convert_numpy_types(batch_results)
        return render_template('batch_results.html', results=batch_results)
        
    except Exception as e:
        logger.error(f"Error in batch thermal analysis: {e}")
        return jsonify({'error': f'Batch analysis failed: {str(e)}'}), 500

@app.route('/about')
def about():
    """About page with information on coal spontaneous combustion"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)