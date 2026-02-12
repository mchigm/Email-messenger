# AI Email Messenger - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Introduction

The AI Email Messenger is an intelligent email communication system that uses artificial intelligence to understand, tokenize, and reconstruct email messages. It offers two input modes:
- **GUI Mode**: Graphical user interface for easy message composition
- **STT Mode**: Speech-to-Text for hands-free voice command operation

## System Architecture

### How It Works

```
[User Input] → [AI Context Extraction] → [Token Generation] → 
[Telnet Transmission] → [Token Reception] → [AI Reconstruction] → [Email Delivery]
```

### Key Components

1. **AI Processor** (`ai_processor.py`)
   - Extracts context from email content
   - Generates intelligent tokens
   - Reconstructs emails based on preferences

2. **Email Handler** (`email_handler.py`)
   - Manages telnet-based transmission
   - Handles SMTP fallback
   - Token serialization/deserialization

3. **GUI Interface** (`gui.py`)
   - User-friendly message composition
   - Preference configuration
   - Real-time status updates

4. **STT Input** (`stt_input.py`)
   - Voice command recognition
   - Speech-to-text conversion
   - Voice-based confirmation

5. **Core Messenger** (`messenger.py`)
   - Coordinates all components
   - Message flow management
   - Error handling

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Microphone (for STT mode)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/mchigm/Email-messenger.git
cd Email-messenger
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data:
```python
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Configuration

### Environment Variables

Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` to customize settings:

#### AI Configuration
- `AI_MODEL_NAME`: Transformer model to use (default: `distilbert-base-uncased`)
- `MAX_TOKEN_LENGTH`: Maximum token length (default: `512`)
- `CONFIDENCE_THRESHOLD`: AI confidence threshold (default: `0.7`)

#### Email Configuration
- `SMTP_SERVER`: SMTP server address (default: `localhost`)
- `SMTP_PORT`: SMTP port (default: `25`)
- `TELNET_HOST`: Telnet server host (default: `localhost`)
- `TELNET_PORT`: Telnet port (default: `23`)

#### STT Configuration
- `STT_ENGINE`: Speech recognition engine (default: `google`)
- `STT_LANGUAGE`: Language code (default: `en-US`)
- `STT_TIMEOUT`: Listening timeout in seconds (default: `5`)

#### GUI Configuration
- `WINDOW_WIDTH`: Window width in pixels (default: `800`)
- `WINDOW_HEIGHT`: Window height in pixels (default: `600`)

#### User Preferences
- `DEFAULT_TONE`: Default email tone (`professional`, `casual`, `formal`, `friendly`)
- `DEFAULT_LENGTH`: Default email length (`short`, `medium`, `long`)

## Usage

### GUI Mode

Start the GUI interface:
```bash
python main.py --mode gui
```

#### Steps:
1. Enter recipient email address
2. Enter subject line
3. Compose your message in the text area
4. Select tone and length preferences
5. Click "Send via AI"
6. Check status bar for confirmation

### STT Mode

Start voice command mode:
```bash
python main.py --mode stt
```

#### Voice Commands:
- **"Send message"**: Compose and send a new message
- **"Help"**: Show available commands
- **"Quit"**: Exit the application

#### Workflow:
1. Say "send message"
2. Speak recipient email address
3. Speak your message (up to 30 seconds)
4. Confirm with "yes" or cancel with "no"

### Python API

Use the messenger programmatically:

```python
from messenger import Messenger

# Initialize
messenger = Messenger()

# Send message
success = messenger.send_message(
    recipient="recipient@example.com",
    subject="Test Message",
    content="Hello from AI Messenger!",
    preferences={'tone': 'friendly', 'length': 'medium'}
)

# Reconstruct received message
reconstructed = messenger.receive_and_reconstruct(
    raw_message='{"tokens": [...]}',
    preferences={'tone': 'professional'}
)
```

## Advanced Features

### AI Context Understanding

The AI processor analyzes:
- **Sentiment**: Positive, negative, or neutral tone
- **Key phrases**: Important sentences from the message
- **Word count**: Length analysis
- **Tokenization**: Intelligent word extraction

### Token Generation

Tokens include:
- Sentiment markers
- Key content words
- Metadata (length, word count)
- Context indicators

### Preference-Based Reconstruction

Customize how received messages are reconstructed:
- **Tone**: Professional, casual, formal, or friendly
- **Length**: Short, medium, or long format
- **Style**: Greeting and closing variations

## Troubleshooting

### Common Issues

#### 1. Module Import Errors
```
Solution: Ensure all dependencies are installed
pip install -r requirements.txt
```

#### 2. Microphone Not Detected (STT Mode)
```
Solution: Check microphone permissions and PyAudio installation
sudo apt-get install portaudio19-dev  # Linux
pip install pyaudio
```

#### 3. Telnet Connection Failed
```
Solution: The system automatically falls back to SMTP
Configure SMTP_SERVER and SMTP_PORT in .env file
```

#### 4. AI Model Download Issues
```
Solution: Ensure stable internet connection
Models are downloaded automatically on first run
```

#### 5. Speech Recognition Not Working
```
Solution: Check STT_ENGINE setting in .env
Try switching between 'google' and 'sphinx' engines
```

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python main.py --mode gui
```

Check logs in `messenger.log`

### Performance Tips

1. **First Run**: Initial model download may take time
2. **Voice Input**: Speak clearly and at moderate pace
3. **Large Messages**: Break into smaller chunks for better processing
4. **Network**: Ensure stable connection for AI services

## Getting Help

- Check examples in `examples.py`
- Review logs in `messenger.log`
- Report issues on GitHub

## License

See LICENSE file for details.
