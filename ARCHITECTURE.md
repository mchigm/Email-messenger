# AI Email Messenger - Technical Architecture

## System Overview

The AI Email Messenger is a sophisticated messaging system that combines artificial intelligence with traditional email protocols to create an intelligent, context-aware communication platform.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                         │
├─────────────────────────────────┬───────────────────────────────┤
│          GUI Mode               │         STT Mode              │
│   (Graphical Interface)         │   (Voice Commands)            │
│   - tkinter-based               │   - SpeechRecognition         │
│   - Message composition         │   - Voice input               │
│   - Preference selection        │   - Verbal confirmation       │
└─────────────────┬───────────────┴──────────────┬────────────────┘
                  │                              │
                  └──────────────┬───────────────┘
                                 ▼
                  ┌──────────────────────────────┐
                  │     CORE MESSENGER           │
                  │   (messenger.py)             │
                  │   - Workflow coordination    │
                  │   - Component integration    │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌────────────────┐    ┌──────────────────┐    ┌────────────────┐
│  AI PROCESSOR  │    │  EMAIL HANDLER   │    │  CONFIGURATION │
│(ai_processor.py)│    │(email_handler.py)│    │  (config.py)   │
├────────────────┤    ├──────────────────┤    ├────────────────┤
│ Context        │    │ Telnet Send      │    │ Environment    │
│ Extraction     │    │ SMTP Fallback    │    │ Variables      │
│                │    │ Token Serialize  │    │ Defaults       │
│ Token          │    │ Token Deserialize│    │ Preferences    │
│ Generation     │    │                  │    │                │
│                │    │                  │    │                │
│ Email          │    │                  │    │                │
│ Reconstruction │    │                  │    │                │
└────────────────┘    └──────────────────┘    └────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌────────────────┐    ┌──────────────────┐
│   NLP/AI       │    │   NETWORK        │
│   MODELS       │    │   PROTOCOLS      │
├────────────────┤    ├──────────────────┤
│ Transformers   │    │ Telnet           │
│ NLTK           │    │ SMTP             │
│ Tokenizer      │    │ TCP/IP           │
└────────────────┘    └──────────────────┘
```

## Message Flow

### Sending Flow

```
1. User Composes Message
   ├─ GUI: Text input with preferences
   └─ STT: Voice recording with recognition
              ↓
2. AI Context Extraction (ai_processor.py)
   ├─ Tokenize text
   ├─ Remove stopwords
   ├─ Analyze sentiment
   └─ Extract key phrases
              ↓
3. Token Generation (ai_processor.py)
   ├─ Create sentiment tokens
   ├─ Select key content tokens
   └─ Add metadata tokens
              ↓
4. Transmission (email_handler.py)
   ├─ Primary: Telnet
   └─ Fallback: SMTP
              ↓
5. Network Delivery
   └─ JSON payload with tokens
```

### Receiving Flow

```
1. Receive Tokenized Message
   └─ JSON payload via telnet/SMTP
              ↓
2. Token Extraction (email_handler.py)
   ├─ Deserialize JSON
   └─ Parse token list
              ↓
3. AI Reconstruction (ai_processor.py)
   ├─ Parse sentiment tokens
   ├─ Extract content tokens
   ├─ Apply user preferences
   │  ├─ Tone (professional/casual/formal/friendly)
   │  └─ Length (short/medium/long)
   └─ Generate email text
              ↓
4. Delivery
   └─ Present to user or forward via email
```

## Component Details

### 1. AI Processor (`ai_processor.py`)

**Purpose**: Core AI engine for understanding and generating email content

**Key Features**:
- Context extraction using NLP
- Sentiment analysis with transformers
- Token generation and encoding
- Preference-based reconstruction

**Dependencies**:
- `transformers`: For pre-trained AI models
- `nltk`: For natural language processing
- `torch`: For neural network inference

**API**:
```python
extract_context(email_content: str) -> Dict
generate_tokens(context: Dict) -> List[str]
reconstruct_email(tokens: List[str], preferences: Dict) -> str
```

### 2. Email Handler (`email_handler.py`)

**Purpose**: Manages network communication and message transmission

**Key Features**:
- Telnet-based token transmission
- SMTP fallback for reliability
- JSON serialization
- Token deserialization

**Protocols**:
- Primary: Telnet (port 23)
- Fallback: SMTP (port 25)

**API**:
```python
send_via_telnet(recipient: str, tokens: List[str]) -> bool
send_reconstructed_email(recipient: str, content: str) -> bool
receive_tokens(raw_message: str) -> List[str]
```

### 3. GUI Interface (`gui.py`)

**Purpose**: Graphical user interface for message composition

**Key Features**:
- tkinter-based cross-platform GUI
- Real-time status updates
- Preference selection
- Message composition area

**Components**:
- Recipient input fields
- Message text area
- Tone selector (dropdown)
- Length selector (dropdown)
- Send/Clear/Quit buttons
- Status bar

### 4. STT Input (`stt_input.py`)

**Purpose**: Voice command interface using speech recognition

**Key Features**:
- Microphone input capture
- Speech-to-text conversion
- Command recognition
- Verbal confirmation

**Supported Engines**:
- Google Speech Recognition (default)
- CMU Sphinx (offline)

**API**:
```python
listen(prompt: str) -> str
get_command() -> str
get_email_content() -> str
confirm_action(question: str) -> bool
```

### 5. Core Messenger (`messenger.py`)

**Purpose**: Orchestrates all components and manages workflow

**Key Features**:
- Component initialization
- Workflow coordination
- Error handling
- Logging

**API**:
```python
send_message(recipient, subject, content, preferences) -> bool
receive_and_reconstruct(raw_message, preferences) -> str
process_stt_message(recipient, voice_content, preferences) -> bool
```

### 6. Configuration (`config.py`)

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading
- Default values
- Type conversion
- Validation

## Data Flow

### Token Structure

```json
{
  "tokens": [
    "SENTIMENT:POSITIVE",
    "meeting",
    "tomorrow",
    "excited",
    "project",
    "LENGTH:150"
  ],
  "sender": "user@example.com",
  "recipient": "colleague@example.com",
  "type": "ai-messenger-tokens"
}
```

### Context Structure

```python
{
  'tokens': ['meeting', 'tomorrow', 'excited', ...],
  'sentiment': 'POSITIVE',
  'sentiment_score': 0.95,
  'key_phrases': ['meeting tomorrow', 'excited about', ...],
  'word_count': 45,
  'sentence_count': 3
}
```

### Preferences Structure

```python
{
  'tone': 'professional',  # or 'casual', 'formal', 'friendly'
  'length': 'medium',      # or 'short', 'long'
}
```

## Security Considerations

1. **Token Privacy**: Tokens are compressed representations, not encrypted
2. **Network Security**: Use TLS/SSL for production telnet/SMTP
3. **Input Validation**: All user inputs are sanitized
4. **Error Handling**: Graceful failures without data exposure

## Performance Optimization

1. **Model Caching**: AI models loaded once at startup
2. **Lazy Loading**: Components initialized on-demand
3. **Async Operations**: Network calls can be made asynchronous
4. **Token Limitation**: Maximum 50 content tokens per message

## Extensibility

### Adding New Input Modes
Implement interface matching GUI/STT callback patterns

### Adding New AI Models
Configure via `AI_MODEL_NAME` environment variable

### Adding New Protocols
Extend `email_handler.py` with new transmission methods

### Custom Preferences
Add to preferences dictionary and handle in reconstruction

## Testing Strategy

1. **Unit Tests**: Each component tested independently
2. **Integration Tests**: End-to-end message flow
3. **Mock Services**: Simulated telnet/SMTP for testing
4. **Voice Testing**: Pre-recorded audio for STT validation

## Deployment

### Development
```bash
python main.py --mode gui
```

### Production
- Use systemd service for daemon mode
- Configure proper SMTP/telnet servers
- Set up logging rotation
- Enable SSL/TLS for security

## Future Enhancements

1. **Encryption**: End-to-end encryption of tokens
2. **Multi-language**: Support for multiple languages
3. **Attachments**: Handle file attachments
4. **Group Chat**: Multi-recipient support
5. **Mobile App**: iOS/Android interfaces
6. **Web Interface**: Browser-based GUI
