#!/usr/bin/env python3
"""
DasMDF - Markdown to PDF Converter
CustomTkinter Version - Core GUI Implementation

A simple GUI application for converting Markdown files to PDF format.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

class MarkdownToPDFConverter:
    def __init__(self):
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("DasMDF - Markdown to PDF Converter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
    
    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="DasMDF Converter", 
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Content frame for text areas
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left side - Markdown
        md_frame = ctk.CTkFrame(content_frame)
        md_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        md_label = ctk.CTkLabel(md_frame, text="Markdown Content", 
                               font=ctk.CTkFont(size=16, weight="bold"))
        md_label.pack(pady=(10, 5))
        
        self.md_textbox = ctk.CTkTextbox(md_frame, height=400)
        self.md_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Right side - CSS
        css_frame = ctk.CTkFrame(content_frame)
        css_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        css_label = ctk.CTkLabel(css_frame, text="CSS Styles", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        css_label.pack(pady=(10, 5))
        
        self.css_textbox = ctk.CTkTextbox(css_frame, height=400)
        self.css_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Bottom buttons frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Buttons container
        buttons_container = ctk.CTkFrame(button_frame)
        buttons_container.pack(pady=15)
        
        # Load MD button
        self.load_md_btn = ctk.CTkButton(buttons_container, text="Load MD", 
                                        width=100, command=self.load_md_file)
        self.load_md_btn.pack(side="left", padx=(0, 10))
        
        # Load CSS button
        self.load_css_btn = ctk.CTkButton(buttons_container, text="Load CSS", 
                                         width=100, command=self.load_css_file)
        self.load_css_btn.pack(side="left", padx=10)
        
        # Convert button
        self.convert_btn = ctk.CTkButton(buttons_container, text="Convert", 
                                        width=100, command=self.convert_pdf)
        self.convert_btn.pack(side="left", padx=(10, 0))
        
        # Add some default content
        self.add_default_content()
    
    def add_default_content(self):
        # Default markdown
        default_md = """# Sample Document

This is a **sample** markdown document for testing.

## Features
- Easy markdown editing
- Custom CSS styling
- PDF conversion

### Code Example
```python
def hello_world():
    print("Hello, World!")
```

> This is a blockquote example.
"""
        self.md_textbox.insert("1.0", default_md)
        
        # Default CSS
        default_css = """body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 40px;
    color: #333;
}

h1, h2, h3 {
    color: #2c3e50;
}

h1 {
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 0;
    padding-left: 20px;
    font-style: italic;
}

code {
    background-color: #f8f8f8;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
}"""
        self.css_textbox.insert("1.0", default_css)
    
    def load_md_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.md_textbox.delete("1.0", tk.END)
                self.md_textbox.insert("1.0", content)
                messagebox.showinfo("Success", "Markdown file loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def load_css_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSS File",
            filetypes=[("CSS files", "*.css"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.css_textbox.delete("1.0", tk.END)
                self.css_textbox.insert("1.0", content)
                messagebox.showinfo("Success", "CSS file loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def convert_pdf(self):
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        messagebox.showinfo("Convert", "PDF conversion functionality coming soon!")
    
    def run(self):
        self.root.mainloop()

def main():
    app = MarkdownToPDFConverter()
    app.run()

if __name__ == "__main__":
    main()
