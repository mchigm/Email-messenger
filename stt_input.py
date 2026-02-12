"""
Speech-to-Text Input Module
Handles voice command input for the messenger
"""
import logging
import speech_recognition as sr
from typing import Optional

from config import STT_ENGINE, STT_LANGUAGE, STT_TIMEOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class STTInput:
    """Speech-to-Text input handler"""
    
    def __init__(self):
        """Initialize STT components"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.engine = STT_ENGINE
            self.language = STT_LANGUAGE
            self.timeout = STT_TIMEOUT
            
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.info(f"STT Input initialized with {self.engine} engine")
        except Exception as e:
            logger.error(f"Error initializing STT: {e}")
            raise
    
    def listen(self, prompt: str = "Listening...") -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            prompt: Message to display while listening
            
        Returns:
            Recognized text or None if failed
        """
        try:
            logger.info(prompt)
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=self.timeout)
            
            logger.info("Processing speech...")
            
            # Use selected engine (default: google)
            if self.engine == 'sphinx':
                text = self.recognizer.recognize_sphinx(audio)
            else:
                text = self.recognizer.recognize_google(audio, language=self.language)
            
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return None
    
    def get_command(self) -> Optional[str]:
        """
        Get voice command from user
        
        Returns:
            Command text or None if failed
        """
        return self.listen("Say a command...")
    
    def get_email_content(self) -> Optional[str]:
        """
        Get email content via voice input
        
        Returns:
            Email content or None if failed
        """
        logger.info("Ready to record email content")
        logger.info("Speak your message (you have 30 seconds)")
        
        try:
            with self.microphone as source:
                # Extended timeout for longer messages
                audio = self.recognizer.listen(source, timeout=30, phrase_time_limit=30)
            
            logger.info("Processing your message...")
            
            # Use selected engine (default: google)
            if self.engine == 'sphinx':
                text = self.recognizer.recognize_sphinx(audio)
            else:
                text = self.recognizer.recognize_google(audio, language=self.language)
            
            logger.info(f"Message captured ({len(text)} characters)")
            return text
            
        except Exception as e:
            logger.error(f"Error capturing email content: {e}")
            return None
    
    def confirm_action(self, question: str = "Please confirm") -> bool:
        """
        Get yes/no confirmation via voice
        
        Args:
            question: Question to ask user
            
        Returns:
            True for yes, False for no
        """
        logger.info(f"{question} (Say 'yes' or 'no')")
        
        response = self.listen("Waiting for confirmation...")
        
        if response:
            response_lower = response.lower()
            if 'yes' in response_lower or 'confirm' in response_lower:
                return True
            elif 'no' in response_lower or 'cancel' in response_lower:
                return False
        
        return False
