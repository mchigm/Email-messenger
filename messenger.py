"""
Core Messenger Module
Coordinates AI processing, email handling, and user interfaces
"""
import logging
from typing import Dict, Optional

from ai_processor import AIProcessor
from email_handler import EmailHandler
from config import DEFAULT_TONE, DEFAULT_LENGTH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Messenger:
    """Core messenger that coordinates all components"""
    
    def __init__(self):
        """Initialize messenger components"""
        try:
            self.ai_processor = AIProcessor()
            self.email_handler = EmailHandler()
            logger.info("Messenger initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing messenger: {e}")
            raise
    
    def send_message(
        self,
        recipient: str,
        subject: str,
        content: str,
        preferences: Optional[Dict[str, str]] = None,
        sender: str = "ai-messenger@localhost"
    ) -> bool:
        """
        Send a message through the AI messenger system
        
        Args:
            recipient: Email address of recipient
            subject: Email subject
            content: Message content
            preferences: User preferences for AI processing
            sender: Email address of sender
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Sending message to {recipient}")
            
            # Step 1: Extract context using AI
            logger.info("Step 1: Extracting context with AI...")
            context = self.ai_processor.extract_context(content)
            
            if 'error' in context:
                logger.error("Failed to extract context")
                return False
            
            # Step 2: Generate tokens
            logger.info("Step 2: Generating tokens...")
            tokens = self.ai_processor.generate_tokens(context)
            
            if not tokens:
                logger.error("Failed to generate tokens")
                return False
            
            # Step 3: Send tokens via telnet
            logger.info("Step 3: Sending tokens via telnet...")
            send_success = self.email_handler.send_via_telnet(
                recipient=recipient,
                tokens=tokens,
                sender=sender
            )
            
            if not send_success:
                logger.error("Failed to send tokens")
                return False
            
            logger.info(f"Message sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def receive_and_reconstruct(
        self,
        raw_message: str,
        preferences: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Receive tokenized message and reconstruct it
        
        Args:
            raw_message: Raw message containing tokens
            preferences: User preferences for reconstruction
            
        Returns:
            Reconstructed email content or None if failed
        """
        try:
            logger.info("Receiving and reconstructing message...")
            
            # Step 1: Extract tokens from message
            tokens = self.email_handler.receive_tokens(raw_message)
            
            if not tokens:
                logger.error("Failed to extract tokens")
                return None
            
            # Step 2: Reconstruct email using AI
            prefs = preferences or {
                'tone': DEFAULT_TONE,
                'length': DEFAULT_LENGTH
            }
            
            reconstructed = self.ai_processor.reconstruct_email(tokens, prefs)
            
            logger.info("Message reconstructed successfully")
            return reconstructed
            
        except Exception as e:
            logger.error(f"Error receiving/reconstructing message: {e}")
            return None
    
    def process_stt_message(
        self,
        recipient: str,
        voice_content: str,
        preferences: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Process and send message from STT input
        
        Args:
            recipient: Email address of recipient
            voice_content: Message content from voice input
            preferences: User preferences
            
        Returns:
            True if successful, False otherwise
        """
        return self.send_message(
            recipient=recipient,
            subject="Voice Message via AI Messenger",
            content=voice_content,
            preferences=preferences
        )
