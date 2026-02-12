"""
GUI Module
Graphical User Interface for the AI Email Messenger
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging
from typing import Optional

from config import WINDOW_WIDTH, WINDOW_HEIGHT, THEME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessengerGUI:
    """GUI interface for AI Email Messenger"""
    
    def __init__(self, messenger_callback=None):
        """
        Initialize GUI
        
        Args:
            messenger_callback: Callback function to handle message sending
        """
        self.messenger_callback = messenger_callback
        self.root = tk.Tk()
        self.root.title("AI Email Messenger")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        self._create_widgets()
        logger.info("GUI initialized")
    
    def _create_widgets(self):
        """Create and layout GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="AI Email Messenger",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Recipient section
        recipient_frame = ttk.LabelFrame(main_frame, text="Recipient", padding="5")
        recipient_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        recipient_frame.columnconfigure(1, weight=1)
        
        ttk.Label(recipient_frame, text="To:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.recipient_entry = ttk.Entry(recipient_frame, width=50)
        self.recipient_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(recipient_frame, text="Subject:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.subject_entry = ttk.Entry(recipient_frame, width=50)
        self.subject_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Message composition section
        message_frame = ttk.LabelFrame(main_frame, text="Compose Message", padding="5")
        message_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        message_frame.columnconfigure(0, weight=1)
        
        self.message_text = scrolledtext.ScrolledText(
            message_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=('Arial', 10)
        )
        self.message_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Preferences section
        pref_frame = ttk.LabelFrame(main_frame, text="AI Preferences", padding="5")
        pref_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(pref_frame, text="Tone:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.tone_var = tk.StringVar(value="professional")
        tone_combo = ttk.Combobox(
            pref_frame,
            textvariable=self.tone_var,
            values=["professional", "casual", "formal", "friendly"],
            state="readonly",
            width=15
        )
        tone_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(pref_frame, text="Length:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.length_var = tk.StringVar(value="medium")
        length_combo = ttk.Combobox(
            pref_frame,
            textvariable=self.length_var,
            values=["short", "medium", "long"],
            state="readonly",
            width=15
        )
        length_combo.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Buttons section
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.send_button = ttk.Button(
            button_frame,
            text="Send via AI",
            command=self._on_send
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self._on_clear
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = ttk.Button(
            button_frame,
            text="Quit",
            command=self._on_quit
        )
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E))
    
    def _on_send(self):
        """Handle send button click"""
        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient email address")
            return
        
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        # Get preferences
        preferences = {
            'tone': self.tone_var.get(),
            'length': self.length_var.get()
        }
        
        # Call messenger callback if provided
        if self.messenger_callback:
            self.status_var.set("Processing message with AI...")
            self.root.update_idletasks()
            
            try:
                result = self.messenger_callback(recipient, subject, message, preferences)
                if result:
                    self.status_var.set("Message sent successfully!")
                    messagebox.showinfo("Success", "Message sent via AI messenger")
                    self._on_clear()
                else:
                    self.status_var.set("Failed to send message")
                    messagebox.showerror("Error", "Failed to send message")
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                self.status_var.set("Error occurred")
                messagebox.showerror("Error", f"Error: {str(e)}")
        else:
            logger.warning("No messenger callback configured")
            messagebox.showinfo("Info", f"Would send to: {recipient}\n\nMessage: {message[:100]}...")
    
    def _on_clear(self):
        """Clear all input fields"""
        self.recipient_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.message_text.delete("1.0", tk.END)
        self.status_var.set("Cleared")
    
    def _on_quit(self):
        """Handle quit button click"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
    
    def run(self):
        """Start the GUI event loop"""
        logger.info("Starting GUI")
        self.root.mainloop()
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()
