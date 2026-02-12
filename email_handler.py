"""
Email Handler Module
Manages email transmission over telnet and SMTP
"""
import telnetlib
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import json

from config import SMTP_SERVER, SMTP_PORT, TELNET_HOST, TELNET_PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailHandler:
    """Handles email transmission and reception"""
    
    def __init__(self):
        """Initialize email handler"""
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.telnet_host = TELNET_HOST
        self.telnet_port = TELNET_PORT
        logger.info("Email Handler initialized")
    
    def send_via_telnet(
        self,
        recipient: str,
        tokens: List[str],
        sender: str = "ai-messenger@localhost"
    ) -> bool:
        """
        Send tokenized message via telnet
        
        Args:
            recipient: Email address of recipient
            tokens: List of message tokens
            sender: Email address of sender
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert tokens to JSON payload
            payload = json.dumps({
                'tokens': tokens,
                'sender': sender,
                'recipient': recipient
            })
            
            logger.info(f"Sending {len(tokens)} tokens to {recipient} via telnet")
            
            # Connect via telnet (simplified implementation)
            # In real implementation, this would connect to actual telnet server
            with telnetlib.Telnet(self.telnet_host, self.telnet_port, timeout=10) as tn:
                # Send HELO command
                tn.write(b"HELO localhost\r\n")
                tn.read_until(b"250", timeout=5)
                
                # Send MAIL FROM
                tn.write(f"MAIL FROM:<{sender}>\r\n".encode())
                tn.read_until(b"250", timeout=5)
                
                # Send RCPT TO
                tn.write(f"RCPT TO:<{recipient}>\r\n".encode())
                tn.read_until(b"250", timeout=5)
                
                # Send DATA
                tn.write(b"DATA\r\n")
                tn.read_until(b"354", timeout=5)
                
                # Send payload
                tn.write(payload.encode() + b"\r\n.\r\n")
                tn.read_until(b"250", timeout=5)
                
                # Quit
                tn.write(b"QUIT\r\n")
            
            logger.info(f"Successfully sent tokens to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending via telnet: {e}")
            logger.info("Telnet connection failed - using fallback SMTP")
            return self._send_via_smtp(recipient, tokens, sender)
    
    def _send_via_smtp(
        self,
        recipient: str,
        tokens: List[str],
        sender: str
    ) -> bool:
        """
        Fallback method: Send via SMTP
        
        Args:
            recipient: Email address of recipient
            tokens: List of message tokens
            sender: Email address of sender
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = 'AI Messenger - Tokenized Message'
            
            # Convert tokens to payload
            payload = json.dumps({
                'tokens': tokens,
                'sender': sender,
                'type': 'ai-messenger-tokens'
            })
            
            msg.attach(MIMEText(payload, 'plain'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.send_message(msg)
            
            logger.info(f"Successfully sent tokens to {recipient} via SMTP")
            return True
            
        except Exception as e:
            logger.error(f"Error sending via SMTP: {e}")
            return False
    
    def send_reconstructed_email(
        self,
        recipient: str,
        content: str,
        sender: str = "ai-messenger@localhost",
        subject: str = "Message from AI Messenger"
    ) -> bool:
        """
        Send reconstructed email to recipient
        
        Args:
            recipient: Email address of recipient
            content: Reconstructed email content
            sender: Email address of sender
            subject: Email subject
            
        Returns:
            True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.send_message(msg)
            
            logger.info(f"Successfully sent reconstructed email to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending reconstructed email: {e}")
            return False
    
    def receive_tokens(self, raw_message: str) -> Optional[List[str]]:
        """
        Extract tokens from received message
        
        Args:
            raw_message: Raw message content
            
        Returns:
            List of tokens if valid, None otherwise
        """
        try:
            data = json.loads(raw_message)
            if 'tokens' in data:
                tokens = data['tokens']
                logger.info(f"Received {len(tokens)} tokens")
                return tokens
            return None
        except Exception as e:
            logger.error(f"Error receiving tokens: {e}")
            return None
