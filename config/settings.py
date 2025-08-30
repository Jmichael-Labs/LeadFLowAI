#!/usr/bin/env python3
"""
🤖 LeadFlow AI - Configuration Settings
Centralized configuration for all LeadFlow AI modules
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LeadFlowConfig:
    """Main configuration class for LeadFlow AI"""
    
    # Directory settings
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    
    # LinkedIn Scraper Settings
    LINKEDIN_USER = os.getenv('LINKEDIN_USER', '')
    LINKEDIN_PASS = os.getenv('LINKEDIN_PASS', '')
    MAX_INVESTORS_PER_CITY = int(os.getenv('MAX_INVESTORS_PER_CITY', 30))
    MAX_CITIES_PER_RUN = int(os.getenv('MAX_CITIES_PER_RUN', 5))
    
    # Property Scanner Settings
    MAX_PROPERTIES_PER_CITY = int(os.getenv('MAX_PROPERTIES_PER_CITY', 15))
    MIN_PROPERTY_VALUE = int(os.getenv('MIN_PROPERTY_VALUE', 150000))
    MIN_URGENCY_SCORE = int(os.getenv('MIN_URGENCY_SCORE', 7))
    
    # AI Scoring Thresholds
    HIGH_QUALITY_SCORE = int(os.getenv('HIGH_QUALITY_SCORE', 80))
    MEDIUM_QUALITY_SCORE = int(os.getenv('MEDIUM_QUALITY_SCORE', 60))
    MIN_PROPERTY_POTENTIAL = int(os.getenv('MIN_PROPERTY_POTENTIAL', 50))
    
    # Automation Settings
    DELAY_BETWEEN_SEARCHES = (3, 8)  # Random delay range in seconds
    DELAY_BETWEEN_CITIES = (15, 30)  # Random delay range between cities
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # Export Settings
    CSV_ENCODING = 'utf-8'
    INCLUDE_HEADERS = True
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Contact Information
    CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'jmichaeloficial@gmail.com')
    COMPANY_NAME = 'LeadFlow AI'
    
    # Target Cities (high-value real estate markets)
    TARGET_CITIES = [
        'Miami', 'Atlanta', 'Phoenix', 'Dallas', 'Denver',
        'Austin', 'Charlotte', 'Tampa', 'Orlando', 'Jacksonville',
        'Fort Worth', 'San Antonio', 'Nashville', 'Memphis', 'Las Vegas',
        'Raleigh', 'Virginia Beach', 'Oklahoma City', 'Louisville', 'Milwaukee'
    ]
    
    # Real Estate Investor Search Terms
    INVESTOR_SEARCH_TERMS = [
        'real estate investor',
        'property investor', 
        'fix and flip',
        'rental property investor',
        'cash buyer real estate',
        'real estate wholesaler',
        'property developer',
        'real estate entrepreneur',
        'multifamily investor',
        'commercial real estate investor',
        'house flipper',
        'buy and hold investor'
    ]
    
    # Property Types for Inheritance Search
    PROPERTY_TYPES = [
        'Single Family',
        'Condo',
        'Townhouse',
        'Duplex',
        'Multi-Family',
        'Commercial'
    ]
    
    # Quality Scoring Weights
    SCORING_WEIGHTS = {
        'title_keywords': 0.3,
        'location_premium': 0.2,
        'search_relevance': 0.2,
        'profile_completeness': 0.1,
        'activity_level': 0.2
    }
    
    # Output File Templates
    OUTPUT_TEMPLATES = {
        'investors': 'leadflow_investors_{timestamp}.csv',
        'properties': 'leadflow_properties_{timestamp}.csv',
        'inheritance': 'leadflow_inheritance_{timestamp}.csv',
        'report': 'leadflow_report_{timestamp}.txt'
    }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [cls.DATA_DIR, cls.TEMPLATES_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def get_output_path(cls, file_type, timestamp=None):
        """Get standardized output file path"""
        if timestamp is None:
            import time
            timestamp = int(time.time())
            
        filename = cls.OUTPUT_TEMPLATES.get(file_type, f'leadflow_output_{timestamp}.csv')
        filename = filename.format(timestamp=timestamp)
        
        return os.path.join(cls.DATA_DIR, filename)
    
    @classmethod
    def validate_settings(cls):
        """Validate configuration settings"""
        required_settings = []
        
        # Check critical settings
        if cls.MAX_INVESTORS_PER_CITY <= 0:
            required_settings.append("MAX_INVESTORS_PER_CITY must be > 0")
            
        if cls.MAX_CITIES_PER_RUN <= 0:
            required_settings.append("MAX_CITIES_PER_RUN must be > 0")
            
        if cls.MIN_PROPERTY_VALUE <= 0:
            required_settings.append("MIN_PROPERTY_VALUE must be > 0")
        
        if required_settings:
            raise ValueError("Configuration errors: " + "; ".join(required_settings))
        
        return True

# Chrome Driver Options
CHROME_OPTIONS = [
    "--no-sandbox",
    "--disable-dev-shm-usage", 
    "--disable-blink-features=AutomationControlled",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-images",  # Faster loading
    "--disable-javascript",  # For basic scraping
]

# User Agents Pool
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Initialize configuration on import
LeadFlowConfig.ensure_directories()
LeadFlowConfig.validate_settings()