"""
AI Processor Module
Handles context understanding and token generation from email content
"""
import logging
from typing import Dict, List, Optional, Any
import nltk
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

from config import AI_MODEL_NAME, MAX_TOKEN_LENGTH, CONFIDENCE_THRESHOLD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIProcessor:
    """AI-powered email content processor"""
    
    def __init__(self):
        """Initialize AI models and tokenizer"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Initialize tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(AI_MODEL_NAME)
            self.model = AutoModel.from_pretrained(AI_MODEL_NAME)
            
            # Initialize sentiment analyzer
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            logger.info(f"AI Processor initialized with model: {AI_MODEL_NAME}")
        except Exception as e:
            logger.error(f"Error initializing AI Processor: {e}")
            raise
    
    def extract_context(self, email_content: str) -> Dict[str, Any]:
        """
        Extract context and meaning from email content
        
        Args:
            email_content: Raw email text content
            
        Returns:
            Dictionary containing extracted context information
        """
        try:
            # Tokenize the content
            tokens = nltk.word_tokenize(email_content.lower())
            
            # Remove stopwords
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [w for w in tokens if w not in stop_words and w.isalnum()]
            
            # Analyze sentiment
            sentiment = self.sentiment_analyzer(email_content[:512])[0]
            
            # Extract key phrases (simplified approach)
            sentences = nltk.sent_tokenize(email_content)
            key_phrases = sentences[:3] if len(sentences) > 3 else sentences
            
            context = {
                'tokens': filtered_tokens[:50],  # Limit to top 50 tokens
                'sentiment': sentiment['label'],
                'sentiment_score': sentiment['score'],
                'key_phrases': key_phrases,
                'word_count': len(tokens),
                'sentence_count': len(sentences)
            }
            
            logger.info(f"Context extracted: {sentiment['label']} ({sentiment['score']:.2f})")
            return context
            
        except Exception as e:
            logger.error(f"Error extracting context: {e}")
            return {'error': str(e)}
    
    def generate_tokens(self, context: Dict[str, Any]) -> List[str]:
        """
        Generate intelligent tokens from extracted context
        
        Args:
            context: Dictionary containing extracted context
            
        Returns:
            List of generated tokens
        """
        try:
            if 'error' in context:
                return []
            
            # Create token representation
            tokens = []
            
            # Add sentiment token
            tokens.append(f"SENTIMENT:{context['sentiment']}")
            
            # Add key content tokens
            content_tokens = context.get('tokens', [])[:20]
            tokens.extend(content_tokens)
            
            # Add metadata tokens
            tokens.append(f"LENGTH:{context.get('word_count', 0)}")
            
            logger.info(f"Generated {len(tokens)} tokens")
            return tokens
            
        except Exception as e:
            logger.error(f"Error generating tokens: {e}")
            return []
    
    def reconstruct_email(
        self,
        tokens: List[str],
        preferences: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Reconstruct email from tokens based on user preferences
        
        Args:
            tokens: List of tokens representing the message
            preferences: User preferences for reconstruction (tone, length, etc.)
            
        Returns:
            Reconstructed email content
        """
        try:
            if not tokens:
                return "Empty message"
            
            # Parse tokens
            sentiment = "neutral"
            content_tokens = []
            metadata = {}
            
            for token in tokens:
                if token.startswith("SENTIMENT:"):
                    sentiment = token.split(":")[1]
                elif token.startswith("LENGTH:"):
                    metadata['length'] = int(token.split(":")[1])
                else:
                    content_tokens.append(token)
            
            # Get preferences
            prefs = preferences or {}
            tone = prefs.get('tone', 'professional')
            length = prefs.get('length', 'medium')
            
            # Reconstruct message
            base_message = " ".join(content_tokens)
            
            # Apply tone adjustments
            greeting = self._get_greeting(tone)
            closing = self._get_closing(tone)
            
            # Construct email
            email_parts = [greeting]
            
            if sentiment.lower() == 'positive':
                email_parts.append("I hope this message finds you well.")
            
            email_parts.append(f"The main points are: {base_message}")
            email_parts.append(closing)
            
            reconstructed = "\n\n".join(email_parts)
            
            logger.info(f"Email reconstructed with {tone} tone")
            return reconstructed
            
        except Exception as e:
            logger.error(f"Error reconstructing email: {e}")
            return "Error reconstructing message"
    
    def _get_greeting(self, tone: str) -> str:
        """Get appropriate greeting based on tone"""
        greetings = {
            'professional': 'Dear Recipient,',
            'casual': 'Hey there!',
            'formal': 'To Whom It May Concern,',
            'friendly': 'Hi friend!'
        }
        return greetings.get(tone, 'Hello,')
    
    def _get_closing(self, tone: str) -> str:
        """Get appropriate closing based on tone"""
        closings = {
            'professional': 'Best regards',
            'casual': 'Cheers',
            'formal': 'Sincerely',
            'friendly': 'Take care'
        }
        return closings.get(tone, 'Best')
