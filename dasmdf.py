"""
DasMDF - Markdown to PDF Converter
CustomTkinter Version - Initial Implementation

A simple GUI application for converting Markdown files to PDF format.
"""

import customtkinter as ctk
import sys
import os

class MarkdownToPDFConverter:
    """Main application class for the Markdown to PDF converter."""
    
    def __init__(self):
        """Initialize the application."""
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main application window."""
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("DasMDF - Markdown to PDF Converter")
        self.root.geometry("600x400")
        self.root.minsize(500, 300)
    
    def create_widgets(self):
        """Create and arrange the GUI widgets."""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame, 
            text="DasMDF Converter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Convert Markdown files to PDF format",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 20))
        
        placeholder_label = ctk.CTkLabel(
            main_frame,
            text="Core functionality will be implemented in upcoming versions",
            font=ctk.CTkFont(size=12)
        )
        placeholder_label.pack(pady=20)
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()

def main():
    """Main entry point of the application."""
    try:
        app = MarkdownToPDFConverter()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()