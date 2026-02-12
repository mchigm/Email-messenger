# AI Email Messenger

An intelligent email-based messaging system powered by AI that transforms traditional email communication into a smart, context-aware messaging experience.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/mchigm/Email-messenger.git
cd Email-messenger
pip install -r requirements.txt

# Download required NLP data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Run in GUI mode
python main.py --mode gui

# Or run in voice command mode
python main.py --mode stt
```

For detailed instructions, see [USAGE.md](USAGE.md). For architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Overview

This AI messenger revolutionizes email communication by:
- **AI Context Understanding**: Automatically analyzes email content and extracts meaningful context
- **Smart Token Generation**: Converts emails into intelligent tokens for efficient transmission
- **AI-Powered Response Generation**: Creates personalized responses based on user preferences
- **Multi-Input Support**: Supports both GUI and Speech-to-Text (STT) command input
- **Telnet-Based Communication**: Enables direct email transmission over telnet

## Features

### 🤖 AI-Powered Communication
- Context-aware email processing using natural language understanding
- Intelligent token generation for efficient message transmission
- Automated response generation based on recipient preferences

### 🎤 Multiple Input Methods
- **GUI Mode**: User-friendly graphical interface for composing and managing messages
- **STT Mode**: Voice command input for hands-free operation

### 📧 Smart Email Handling
- Telnet-based email transmission
- AI-driven content analysis and token generation
- Preference-based email reconstruction at receiver end

## How It Works

1. **Compose**: User creates a message using GUI or voice commands (STT)
2. **Process**: AI analyzes the email content and extracts context
3. **Transmit**: Generates tokens and sends to recipient via telnet
4. **Reconstruct**: Receiver's AI generates a new email based on tokens and user preferences
5. **Deliver**: Final message is delivered to recipient

## Installation

```bash
# Clone the repository
git clone https://github.com/mchigm/Email-messenger.git
cd Email-messenger

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

### GUI Mode
```bash
python main.py --mode gui
```

### STT Mode (Voice Commands)
```bash
python main.py --mode stt
```

## Configuration

Edit `config.py` to customize:
- AI model settings
- Email server configuration
- User preferences
- STT engine settings

## Requirements

- Python 3.7+
- Speech recognition library
- GUI framework (tkinter)
- AI/NLP libraries for context processing

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
