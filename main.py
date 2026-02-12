"""
Main Entry Point for AI Email Messenger
Supports both GUI and STT modes
"""
import argparse
import logging
import sys

from messenger import Messenger
from gui import MessengerGUI
from stt_input import STTInput
from config import LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_gui_mode():
    """Run messenger in GUI mode"""
    logger.info("Starting in GUI mode")
    
    try:
        # Initialize messenger
        messenger = Messenger()
        
        # Create callback for GUI
        def send_callback(recipient, subject, message, preferences):
            return messenger.send_message(recipient, subject, message, preferences)
        
        # Initialize and run GUI
        gui = MessengerGUI(messenger_callback=send_callback)
        gui.run()
        
    except Exception as e:
        logger.error(f"Error in GUI mode: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def run_stt_mode():
    """Run messenger in STT (voice command) mode"""
    logger.info("Starting in STT mode")
    
    try:
        # Initialize components
        messenger = Messenger()
        stt = STTInput()
        
        print("\n" + "="*50)
        print("AI Email Messenger - Voice Command Mode")
        print("="*50 + "\n")
        
        while True:
            print("\nListening for command...")
            print("Say 'send message', 'quit', or 'help'")
            
            command = stt.get_command()
            
            if not command:
                print("Could not understand command. Please try again.")
                continue
            
            command_lower = command.lower()
            
            if 'quit' in command_lower or 'exit' in command_lower:
                print("Goodbye!")
                break
            
            elif 'help' in command_lower:
                print("\nAvailable commands:")
                print("- 'send message' - Compose and send a message")
                print("- 'quit' - Exit the application")
                continue
            
            elif 'send' in command_lower or 'message' in command_lower:
                # Get recipient
                print("\nSay the recipient email address:")
                recipient = stt.listen("Listening for recipient...")
                
                if not recipient:
                    print("Could not get recipient. Cancelled.")
                    continue
                
                print(f"Recipient: {recipient}")
                
                # Get message content
                print("\nSay your message:")
                content = stt.get_email_content()
                
                if not content:
                    print("Could not get message content. Cancelled.")
                    continue
                
                print(f"\nMessage captured ({len(content)} characters)")
                print(f"Preview: {content[:100]}...")
                
                # Confirm
                if stt.confirm_action("Send this message?"):
                    print("\nSending message...")
                    
                    success = messenger.process_stt_message(
                        recipient=recipient,
                        voice_content=content
                    )
                    
                    if success:
                        print("✓ Message sent successfully!")
                    else:
                        print("✗ Failed to send message")
                else:
                    print("Message cancelled")
            
            else:
                print(f"Unknown command: {command}")
                print("Say 'help' for available commands")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        logger.info("STT mode interrupted by user")
    except Exception as e:
        logger.error(f"Error in STT mode: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Email Messenger - Smart email communication with AI'
    )
    parser.add_argument(
        '--mode',
        choices=['gui', 'stt'],
        default='gui',
        help='Mode to run the messenger (default: gui)'
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting AI Email Messenger in {args.mode} mode")
    print(f"\nStarting AI Email Messenger in {args.mode.upper()} mode...\n")
    
    if args.mode == 'gui':
        run_gui_mode()
    else:  # args.mode == 'stt'
        run_stt_mode()


if __name__ == '__main__':
    main()
