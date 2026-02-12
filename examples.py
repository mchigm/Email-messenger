"""
Example usage of AI Email Messenger
"""

# Example 1: Basic message sending
def example_basic_send():
    from messenger import Messenger
    
    messenger = Messenger()
    
    # Send a message
    success = messenger.send_message(
        recipient="friend@example.com",
        subject="Hello from AI Messenger",
        content="Hi! This is a test message being sent through the AI messenger system.",
        preferences={
            'tone': 'friendly',
            'length': 'medium'
        }
    )
    
    if success:
        print("Message sent successfully!")
    else:
        print("Failed to send message")


# Example 2: Receiving and reconstructing
def example_receive():
    import json
    from messenger import Messenger
    
    messenger = Messenger()
    
    # Simulate received tokenized message
    raw_message = json.dumps({
        'tokens': ['SENTIMENT:POSITIVE', 'hello', 'friend', 'meeting', 'tomorrow', 'LENGTH:50'],
        'sender': 'sender@example.com',
        'type': 'ai-messenger-tokens'
    })
    
    # Reconstruct the message
    reconstructed = messenger.receive_and_reconstruct(
        raw_message=raw_message,
        preferences={
            'tone': 'professional',
            'length': 'medium'
        }
    )
    
    print("Reconstructed message:")
    print(reconstructed)


# Example 3: Using the AI processor directly
def example_ai_processor():
    from ai_processor import AIProcessor
    
    processor = AIProcessor()
    
    # Extract context
    email_text = "I'm really excited about our upcoming meeting tomorrow!"
    context = processor.extract_context(email_text)
    
    print("Extracted context:")
    print(f"Sentiment: {context['sentiment']}")
    print(f"Key phrases: {context['key_phrases']}")
    
    # Generate tokens
    tokens = processor.generate_tokens(context)
    print(f"\nGenerated {len(tokens)} tokens")
    
    # Reconstruct
    reconstructed = processor.reconstruct_email(
        tokens=tokens,
        preferences={'tone': 'casual', 'length': 'short'}
    )
    
    print("\nReconstructed email:")
    print(reconstructed)


if __name__ == '__main__':
    print("AI Email Messenger - Examples\n")
    print("="*50)
    
    print("\nExample 1: Basic message sending")
    print("-"*50)
    # Note: This will fail without proper SMTP/Telnet setup
    # example_basic_send()
    print("(Requires SMTP/Telnet configuration)")
    
    print("\nExample 2: AI Processing")
    print("-"*50)
    example_ai_processor()
    
    print("\nExample 3: Message reconstruction")
    print("-"*50)
    example_receive()
