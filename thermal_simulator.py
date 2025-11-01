import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import os
import random
import base64
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class ThermalSimulator:
    """
    Advanced thermal image simulation for coal spontaneous combustion analysis.
    
    This class converts regular coal images into thermal representations by:
    1. Analyzing image brightness and texture
    2. Simulating heat distribution patterns
    3. Applying realistic thermal colormap
    4. Generating environmental parameters
    """
    
    def __init__(self):
        # Thermal colormap (cold blue to hot red/yellow)
        self.thermal_colors = [
            '#000080',  # Deep blue (cold)
            '#0000ff',  # Blue
            '#00ffff',  # Cyan
            '#00ff00',  # Green
            '#ffff00',  # Yellow
            '#ff8000',  # Orange
            '#ff0000',  # Red
            '#ff00ff',  # Magenta (very hot)
            '#ffffff'   # White (extreme heat)
        ]
        
        # Create custom thermal colormap
        self.thermal_cmap = LinearSegmentedColormap.from_list(
            'thermal', self.thermal_colors, N=256
        )
        
        # Temperature ranges for coal analysis (Celsius)
        self.temp_ranges = {
            'safe': (15, 35),
            'watch': (35, 50),
            'caution': (50, 80),
            'danger': (80, 120),
            'critical': (120, 200)
        }
    
    def analyze_image_features(self, image_path):
        """
        Analyze coal image to extract features that influence thermal behavior
        """
        try:
            # Load and process image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Feature extraction
            features = {}
            
            # Brightness analysis (darker coal = higher carbon content = more heat prone)
            features['avg_brightness'] = np.mean(gray)
            features['brightness_std'] = np.std(gray)
            
            # Texture analysis (rough texture = more surface area = higher oxidation)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            features['texture_variance'] = np.var(laplacian)
            
            # Color analysis
            features['hue_mean'] = np.mean(hsv[:,:,0])
            features['saturation_mean'] = np.mean(hsv[:,:,1])
            features['value_mean'] = np.mean(hsv[:,:,2])
            
            # Edge density (indicates fragmentation/surface area)
            edges = cv2.Canny(gray, 50, 150)
            features['edge_density'] = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # Coal particle size estimation (based on contours)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 10]
                features['avg_particle_size'] = np.mean(areas) if areas else 0
                features['particle_count'] = len(areas)
            else:
                features['avg_particle_size'] = 0
                features['particle_count'] = 0
            
            return features
            
        except Exception as e:
            logger.error(f"Error analyzing image features: {e}")
            return None
    
    def generate_environmental_parameters(self, image_features, base_scenario='normal'):
        """
        Generate realistic environmental parameters based on image analysis and scenario
        """
        scenarios = {
            'normal': {
                'temp_range': (20, 30),
                'humidity_range': (40, 70),
                'wind_range': (0.5, 2.0),
                'oxygen_range': (20.5, 21.0)
            },
            'hot_day': {
                'temp_range': (35, 45),
                'humidity_range': (20, 40),
                'wind_range': (0.2, 1.0),
                'oxygen_range': (20.8, 21.0)
            },
            'humid': {
                'temp_range': (25, 35),
                'humidity_range': (80, 95),
                'wind_range': (0.1, 0.8),
                'oxygen_range': (20.0, 20.5)
            },
            'poor_ventilation': {
                'temp_range': (22, 32),
                'humidity_range': (50, 80),
                'wind_range': (0.05, 0.3),
                'oxygen_range': (19.5, 20.2)
            }
        }
        
        scenario = scenarios.get(base_scenario, scenarios['normal'])
        
        # Base environmental parameters
        env_params = {
            'ambient_temperature': random.uniform(*scenario['temp_range']),
            'relative_humidity': random.uniform(*scenario['humidity_range']),
            'wind_speed': random.uniform(*scenario['wind_range']),
            'oxygen_content': random.uniform(*scenario['oxygen_range']),
            'atmospheric_pressure': random.uniform(98, 102),  # kPa
            'pile_height': random.uniform(2.0, 8.0),  # meters
            'storage_duration': random.randint(1, 30)  # days
        }
        
        # Adjust based on image features if available
        if image_features:
            # Darker coal (lower brightness) tends to heat up more
            if image_features['avg_brightness'] < 80:
                env_params['ambient_temperature'] += random.uniform(2, 8)
            
            # High texture variance indicates more surface area
            if image_features['texture_variance'] > 500:
                env_params['wind_speed'] *= random.uniform(0.7, 0.9)  # Reduced ventilation effect
            
            # More particles = more heat generation potential
            if image_features['particle_count'] > 100:
                env_params['pile_height'] += random.uniform(0.5, 2.0)
        
        return env_params
    
    def simulate_thermal_distribution(self, image_path, env_params):
        """
        Create thermal image simulation based on coal features and environmental conditions
        """
        try:
            # Load original image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to grayscale for thermal analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Normalize image to 0-1 range
            normalized = gray.astype(np.float32) / 255.0
            
            # Invert brightness (darker areas = hotter in coal context)
            inverted = 1.0 - normalized
            
            # Apply Gaussian blur to simulate heat diffusion
            heat_diffusion = cv2.GaussianBlur(inverted, (21, 21), 0)
            
            # Add random hot spots (oxidation points)
            hot_spots = np.zeros_like(heat_diffusion)
            num_hotspots = random.randint(3, 12)
            
            for _ in range(num_hotspots):
                x = random.randint(20, heat_diffusion.shape[1] - 20)
                y = random.randint(20, heat_diffusion.shape[0] - 20)
                intensity = random.uniform(0.6, 1.0)
                size = random.randint(15, 40)
                
                # Create circular hot spot
                cv2.circle(hot_spots, (x, y), size, intensity, -1)
            
            # Blur hot spots for realistic heat spread
            hot_spots = cv2.GaussianBlur(hot_spots, (31, 31), 0)
            
            # Combine base thermal map with hot spots
            thermal_map = np.clip(heat_diffusion + hot_spots * 0.4, 0, 1)
            
            # Apply environmental factors
            base_temp = env_params['ambient_temperature']
            max_temp_increase = 150  # Maximum temperature rise
            
            # Environmental multipliers
            humidity_factor = 1.0 + (env_params['relative_humidity'] - 50) / 200  # Higher humidity = more heat retention
            wind_factor = max(0.5, 1.0 - env_params['wind_speed'] / 5.0)  # Less wind = more heat buildup
            pile_factor = 1.0 + (env_params['pile_height'] - 3.0) / 10.0  # Larger piles retain more heat
            duration_factor = 1.0 + (env_params['storage_duration'] - 1) / 50.0  # Longer storage = more oxidation
            
            # Calculate temperature distribution
            temp_multiplier = humidity_factor * wind_factor * pile_factor * duration_factor
            temperature_map = base_temp + (thermal_map * max_temp_increase * temp_multiplier)
            
            # Ensure realistic temperature bounds
            temperature_map = np.clip(temperature_map, base_temp, base_temp + 180)
            
            return thermal_map, temperature_map
            
        except Exception as e:
            logger.error(f"Error simulating thermal distribution: {e}")
            return None, None
    
    def create_thermal_visualization(self, thermal_map, temperature_map, original_image_path):
        """
        Create thermal image visualization and return as base64 string
        """
        try:
            # Ensure we're using the Agg backend
            plt.switch_backend('Agg')
            
            # Create thermal image with colormap
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            # Original image
            original_img = cv2.imread(original_image_path)
            original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            axes[0].imshow(original_rgb)
            axes[0].set_title('Original Coal Sample', fontsize=12, fontweight='bold')
            axes[0].axis('off')
            
            # Thermal map visualization
            thermal_display = axes[1].imshow(thermal_map, cmap=self.thermal_cmap, vmin=0, vmax=1)
            axes[1].set_title('Thermal Heat Distribution', fontsize=12, fontweight='bold')
            axes[1].axis('off')
            
            # Temperature map with values
            temp_display = axes[2].imshow(temperature_map, cmap=self.thermal_cmap, 
                                        vmin=np.min(temperature_map), vmax=np.max(temperature_map))
            axes[2].set_title('Temperature Map (°C)', fontsize=12, fontweight='bold')
            axes[2].axis('off')
            
            # Add colorbars
            plt.colorbar(thermal_display, ax=axes[1], fraction=0.046, pad=0.04, label='Heat Intensity')
            plt.colorbar(temp_display, ax=axes[2], fraction=0.046, pad=0.04, label='Temperature (°C)')
            
            plt.tight_layout()
            
            # Convert to base64 string
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            thermal_image_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            # Calculate temperature statistics
            temp_stats = {
                'min_temp': float(np.min(temperature_map)),
                'max_temp': float(np.max(temperature_map)),
                'avg_temp': float(np.mean(temperature_map)),
                'hot_spot_count': int(np.sum(temperature_map > (np.mean(temperature_map) + 2 * np.std(temperature_map)))),
                'critical_area_percentage': float(np.sum(temperature_map > 80) / temperature_map.size * 100)
            }
            
            return thermal_image_b64, temp_stats
            
        except Exception as e:
            logger.error(f"Error creating thermal visualization: {e}")
            return None, None
    
    def generate_coal_properties_from_image(self, image_features, env_params):
        """
        Generate realistic coal properties based on image analysis and environmental conditions
        """
        try:
            # Base properties for bituminous coal
            base_properties = {
                'moisture': (6.0, 15.0),
                'volatile_matter': (25.0, 45.0),
                'ash': (8.0, 25.0),
                'fixed_carbon': (35.0, 60.0)
            }
            
            # Generate base values
            properties = {}
            for prop, (min_val, max_val) in base_properties.items():
                properties[prop] = random.uniform(min_val, max_val)
            
            # Adjust based on image features
            if image_features:
                # Darker coal typically has higher carbon content
                if image_features['avg_brightness'] < 60:
                    properties['fixed_carbon'] += random.uniform(2, 8)
                    properties['volatile_matter'] += random.uniform(1, 5)
                
                # High texture (rough surface) may indicate weathering
                if image_features['texture_variance'] > 600:
                    properties['moisture'] += random.uniform(1, 3)
                    properties['ash'] += random.uniform(0.5, 2.0)
                
                # Fine particles may have different composition
                if image_features['avg_particle_size'] < 50:
                    properties['volatile_matter'] += random.uniform(2, 6)
            
            # Adjust based on environmental conditions
            if env_params['relative_humidity'] > 70:
                properties['moisture'] += random.uniform(1, 4)
            
            if env_params['storage_duration'] > 15:
                properties['moisture'] -= random.uniform(0.5, 2.0)  # Drying over time
                properties['ash'] += random.uniform(0.2, 1.0)  # Oxidation residue
            
            # Normalize to ensure total ≈ 100%
            total = sum(properties.values())
            if total > 0:
                factor = 100.0 / total
                for prop in properties:
                    properties[prop] *= factor
            
            # Ensure reasonable bounds
            properties['moisture'] = max(1.0, min(20.0, properties['moisture']))
            properties['volatile_matter'] = max(15.0, min(50.0, properties['volatile_matter']))
            properties['ash'] = max(5.0, min(35.0, properties['ash']))
            properties['fixed_carbon'] = max(25.0, min(70.0, properties['fixed_carbon']))
            
            return properties
            
        except Exception as e:
            logger.error(f"Error generating coal properties: {e}")
            return {
                'moisture': 10.0,
                'volatile_matter': 35.0,
                'ash': 15.0,
                'fixed_carbon': 40.0
            }
    
    def assess_thermal_risk(self, temperature_map, temp_stats):
        """
        Assess spontaneous combustion risk based on thermal analysis
        """
        risk_factors = []
        thermal_risk_score = 0
        
        # Maximum temperature assessment
        max_temp = temp_stats['max_temp']
        if max_temp > 120:
            risk_factors.append(f"Critical hot spots detected ({max_temp:.1f}°C)")
            thermal_risk_score += 40
        elif max_temp > 80:
            risk_factors.append(f"Dangerous temperatures observed ({max_temp:.1f}°C)")
            thermal_risk_score += 30
        elif max_temp > 50:
            risk_factors.append(f"Elevated temperatures detected ({max_temp:.1f}°C)")
            thermal_risk_score += 20
        
        # Average temperature assessment
        avg_temp = temp_stats['avg_temp']
        if avg_temp > 45:
            risk_factors.append(f"High average temperature ({avg_temp:.1f}°C)")
            thermal_risk_score += 15
        
        # Critical area assessment
        critical_percentage = temp_stats['critical_area_percentage']
        if critical_percentage > 20:
            risk_factors.append(f"Large critical temperature zone ({critical_percentage:.1f}%)")
            thermal_risk_score += 20
        elif critical_percentage > 10:
            risk_factors.append(f"Moderate critical temperature zone ({critical_percentage:.1f}%)")
            thermal_risk_score += 10
        
        # Hot spot count
        hot_spots = temp_stats['hot_spot_count']
        if hot_spots > 10:
            risk_factors.append(f"Multiple hot spots detected ({hot_spots})")
            thermal_risk_score += 15
        elif hot_spots > 5:
            risk_factors.append(f"Several hot spots present ({hot_spots})")
            thermal_risk_score += 8
        
        return {
            'thermal_risk_score': min(thermal_risk_score, 100),
            'thermal_risk_factors': risk_factors,
            'temperature_statistics': temp_stats
        }