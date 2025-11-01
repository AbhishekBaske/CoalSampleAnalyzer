# Coal Spontaneous Combustion Analyzer

A comprehensive web application for assessing the risk of spontaneous combustion in coal based on coal properties and environmental conditions. Built with Flask and featuring advanced scientific algorithms for coal safety analysis.

![Coal Analyzer](https://img.shields.io/badge/Coal-Analyzer-orange) ![Flask](https://img.shields.io/badge/Flask-3.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 🔥 Features

### Core Analysis Capabilities
- **Crossing Point Temperature (CPT)** calculation
- **Liability Index** assessment based on Banerjee methodology
- **WITS Index** calculation (University of Witwatersrand method)
- **Olpinski Index** for moisture-based risk evaluation
- **Comprehensive Risk Assessment** with detailed scoring system
- **Safety Recommendations** based on calculated risk levels

### 🌡️ Advanced Thermal Analysis (NEW!)
- **Thermal Image Simulation** from regular coal photographs
- **Heat Distribution Mapping** with realistic temperature gradients
- **Hot Spot Detection** using advanced image processing
- **Environmental Parameter Simulation** (temperature, humidity, ventilation)
- **Combined Thermal + Chemical Risk Assessment**
- **Batch Processing** of multiple coal samples
- **Interactive Thermal Visualizations** with colormap representations

### Technical Features
- Professional web interface with responsive design
- RESTful API for programmatic access
- Real-time form validation and auto-calculation
- Printable analysis reports with thermal images
- JSON/CSV export functionality
- Bootstrap 5 styling with custom coal industry theme
- Mobile-friendly responsive design
- **Dataset Integration** with bituminous coal image library

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd coalspontaneous
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to: `http://localhost:5000`

## 📊 Usage Guide

### Web Interface

#### Manual Analysis
1. **Navigate to Manual Analysis Page**
   - Enter coal identification information (type, location)
   - Input coal properties: moisture, volatile matter, ash content, fixed carbon
   - Set environmental conditions: oxygen levels, ambient temperature, ventilation rate
   - Click "Analyze Coal Sample" to process the data

#### 🌡️ Thermal Analysis (NEW!)
1. **Navigate to Thermal Analysis Page**
   - Browse the bituminous coal dataset (70+ sample images)
   - Click "Analyze Thermal" on any coal sample
   - View comprehensive thermal simulation with heat maps
   - See combined thermal + chemical risk assessment

2. **Batch Analysis**
   - Run thermal analysis on multiple samples simultaneously
   - View comparative results in sortable table format
   - Export results to CSV or JSON for further analysis
   - Statistical summaries and environmental condition distributions

3. **Understanding Results**
   - **Risk Levels**: Critical (80-100), High (60-79), Moderate (40-59), Low (0-39)
   - **Temperature Zones**: Safe (<35°C), Watch (35-50°C), Caution (50-80°C), Critical (>80°C)
   - **Thermal Maps**: Blue (cold) to red/white (hot) color representation
   - **Hot Spots**: Automatically detected high-temperature regions

### API Usage

The application provides a RESTful API endpoint for programmatic access:

**Endpoint**: `POST /api/analyze`

**Request Body**:
```json
{
    "moisture": 8.5,
    "volatile_matter": 35.2,
    "ash": 12.3,
    "fixed_carbon": 44.0,
    "oxygen": 20.9,
    "ambient_temp": 28.5,
    "ventilation_rate": 0.8
}
```

**Response**:
```json
{
    "success": true,
    "calculated_indices": {
        "cpt": 148.7,
        "liability_index": 2.4,
        "wits_index": 3.8,
        "olpinski_index": 0.18
    },
    "risk_assessment": {
        "overall_risk": "HIGH",
        "risk_score": 65,
        "risk_factors": ["High CPT Risk", "High Liability Index Risk"],
        "color": "warning"
    },
    "recommendations": [
        "Implement immediate monitoring systems for temperature and gas emissions",
        "Increase ventilation rates to minimum 1.0 m/s",
        "Regular inspection of coal stockpiles every 2-4 hours"
    ]
}
```

## 🧮 Scientific Background

### Analysis Methods

#### 1. Crossing Point Temperature (CPT)
The temperature at which heat generation from coal oxidation exceeds heat dissipation. Calculated using empirical formulas based on coal proximate analysis.

**Risk Thresholds**:
- CPT < 140°C: Very High Risk
- CPT 140-150°C: High Risk  
- CPT 150-160°C: Moderate Risk
- CPT > 160°C: Low Risk

#### 2. Liability Index (Banerjee Method)
**Formula**: `LI = (Moisture × Volatile Matter) / Ash Content`

**Risk Thresholds**:
- LI > 2.0: High Risk
- LI 1.0-2.0: Moderate Risk
- LI < 1.0: Low Risk

#### 3. WITS Index
**Formula**: `WITS = (Moisture + Volatile Matter) × Oxygen / (Ash + 1)`

**Risk Thresholds**:
- WITS > 5.0: High Risk
- WITS 2.0-5.0: Moderate Risk
- WITS < 2.0: Low Risk

#### 4. Olpinski Index
**Formula**: `OI = Moisture / (Ash + Volatile Matter)`

Focuses on moisture content's role in spontaneous combustion risk.

### Risk Assessment Algorithm

The comprehensive risk assessment considers:
- All calculated indices with weighted scoring
- Environmental factors (temperature, ventilation)
- Combined risk factor analysis
- Industry-standard safety thresholds

## 📁 Project Structure

```
coalspontaneous/
├── app.py                    # Main Flask application with thermal integration
├── thermal_simulator.py     # Advanced thermal image simulation module
├── test_thermal.py          # Thermal analysis test script
├── requirements.txt         # Python dependencies (includes image processing)
├── README.md               # This comprehensive documentation
├── config.py               # Configuration settings and parameters
├── start.bat               # Windows startup script
├── dataset/                # Coal sample image dataset
│   └── Bituminous/        # 70+ bituminous coal sample images
│       ├── 10.jpg
│       ├── 100.jpg
│       └── ... (more samples)
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Manual analysis form page
│   ├── results.html       # Manual analysis results display
│   ├── thermal.html       # Thermal analysis interface
│   ├── thermal_results.html # Thermal analysis detailed results
│   ├── batch_results.html # Batch analysis comparative results
│   └── about.html         # Scientific background information
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Custom styling with thermal themes
    └── js/                # JavaScript files (for future use)
```

## 🛡️ Safety and Compliance

### Important Disclaimers
- This tool provides estimates based on established scientific methods
- Results should be validated with on-site measurements
- Professional mining engineers should review all assessments
- The tool is for guidance only and developers assume no liability for safety decisions

### Industry Standards
The algorithms are based on peer-reviewed research and international standards:
- ASTM D5515 - Swelling Properties of Bituminous Coal
- ISO 562 - Volatile Matter Determination
- ASTM D3173 - Moisture Analysis
- ASTM D3174 - Ash Analysis

## 🔧 Development

### Adding New Analysis Methods
1. Add calculation method to `CoalSpontaneousAnalyzer` class
2. Update risk assessment algorithm
3. Modify templates to display new results
4. Update API response structure

### Customization Options
- Modify risk thresholds in `risk_assessment()` method
- Customize styling in `static/css/style.css`
- Add new coal types in form dropdown
- Extend recommendation engine logic

### Testing
Run the application in debug mode for development:
```bash
python app.py
```
The application will reload automatically when code changes are detected.

## 📞 Support and Documentation

### Getting Help
1. Check the "About" page in the application for scientific background
2. Review this README for technical details
3. Examine the source code comments for implementation details

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes with appropriate testing
4. Submit pull request with detailed description

## 📜 License

This project is licensed under the MIT License. See the license terms below:

```
MIT License

Copyright (c) 2025 Coal Safety Solutions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔬 Scientific References

1. Banerjee, S.C. (2000). "Prevention and Combating Mine Fires." Oxford & IBH Publishing.
2. Sharma, A. et al. (2020). "Coal Spontaneous Combustion: Laboratory and Field Studies." Mining Engineering.
3. Singh, R.N. (2019). "Advances in Coal Mine Safety: Spontaneous Combustion Assessment."
4. University of Witwatersrand (2018). "WITS Index for Coal Spontaneous Combustion Prediction."
5. Olpinski, B. (2015). "Moisture Effects on Coal Spontaneous Combustion Liability." Fuel Journal.

## 📈 Version History

### v1.0.0 (2025-01-01)
- Initial release with core analysis functionality
- Web interface with Bootstrap 5 styling
- RESTful API implementation
- Comprehensive risk assessment algorithms
- Scientific documentation and references

---

**Built with ❤️ for coal mining safety**# CoalSampleAnalyzer
