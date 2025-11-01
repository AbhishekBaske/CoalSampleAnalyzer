import json
import base64
from PIL import Image
import io
import random

def handler(event, context):
    """
    Netlify serverless function for basic coal analysis
    """
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Mock analysis results (since we can't run full OpenCV in serverless)
        results = {
            'risk_level': random.choice(['Low', 'Medium', 'High']),
            'coal_type': random.choice(['Bituminous', 'Anthracite', 'Lignite']),
            'moisture_content': round(random.uniform(5, 15), 1),
            'spontaneous_combustion_risk': round(random.uniform(0.1, 0.9), 2),
            'recommendations': [
                "Monitor temperature regularly",
                "Ensure proper ventilation",
                "Consider moisture control measures"
            ],
            'message': 'Analysis completed (Demo Mode - Limited Functionality)'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(results)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }