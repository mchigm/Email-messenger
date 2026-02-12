"""
Configuration settings for AI Email Messenger
"""
import os
from dotenv import load_dotenv

load_dotenv()

# AI Model Configuration
AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'distilbert-base-uncased')
MAX_TOKEN_LENGTH = int(os.getenv('MAX_TOKEN_LENGTH', '512'))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'localhost')
SMTP_PORT = int(os.getenv('SMTP_PORT', '25'))
TELNET_HOST = os.getenv('TELNET_HOST', 'localhost')
TELNET_PORT = int(os.getenv('TELNET_PORT', '23'))

# STT Configuration
STT_ENGINE = os.getenv('STT_ENGINE', 'google')
STT_LANGUAGE = os.getenv('STT_LANGUAGE', 'en-US')
STT_TIMEOUT = int(os.getenv('STT_TIMEOUT', '5'))

# GUI Configuration
WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '800'))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
THEME = os.getenv('THEME', 'default')

# User Preferences
DEFAULT_TONE = os.getenv('DEFAULT_TONE', 'professional')
DEFAULT_LENGTH = os.getenv('DEFAULT_LENGTH', 'medium')
AUTO_SEND = os.getenv('AUTO_SEND', 'false').lower() == 'true'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'messenger.log')
