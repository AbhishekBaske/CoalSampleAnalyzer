# Coal Spontaneous Combustion Analyzer Configuration
# This file contains configurable parameters for the analysis algorithms

# Risk Assessment Thresholds
RISK_THRESHOLDS = {
    "cpt": {
        "very_high": 140,
        "high": 150,
        "moderate": 160
    },
    "liability_index": {
        "high": 2.0,
        "moderate": 1.0
    },
    "wits_index": {
        "high": 5.0,
        "moderate": 2.0
    },
    "environmental": {
        "high_temp": 30,
        "poor_ventilation": 0.5
    }
}

# Risk Scoring Weights
RISK_WEIGHTS = {
    "cpt_very_high": 40,
    "cpt_high": 30,
    "cpt_moderate": 20,
    "cpt_low": 10,
    "li_high": 25,
    "li_moderate": 15,
    "li_low": 5,
    "wits_high": 20,
    "wits_moderate": 10,
    "wits_low": 5,
    "high_temp": 15,
    "poor_ventilation": 15
}

# Overall Risk Categories
OVERALL_RISK_CATEGORIES = {
    "critical": {"min": 80, "max": 100, "color": "danger"},
    "high": {"min": 60, "max": 79, "color": "warning"},
    "moderate": {"min": 40, "max": 59, "color": "info"},
    "low": {"min": 0, "max": 39, "color": "success"}
}

# Default Environmental Values
DEFAULT_VALUES = {
    "oxygen": 20.9,
    "ambient_temp": 25.0,
    "ventilation_rate": 1.0
}

# Application Settings
APP_CONFIG = {
    "debug": True,
    "host": "0.0.0.0",
    "port": 5000,
    "secret_key": "coal_spontaneous_analyzer_2025"
}