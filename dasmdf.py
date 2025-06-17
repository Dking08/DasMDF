"""
DasMDF - Markdown to PDF Converter
CustomTkinter Version - WeasyPrint Engine Integration

A simple GUI application for converting Markdown files to PDF format.
Now includes WeasyPrint engine and HTML preview functionality.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tempfile
import webbrowser
import markdown2
from weasyprint import HTML

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
        
        # Preview button
        self.preview_btn = ctk.CTkButton(buttons_container, text="Preview", 
                                        width=100, command=self.preview_doc)
        self.preview_btn.pack(side="left", padx=10)
        
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
- PDF conversion with WeasyPrint

### Code Example
````python
def hello_world():
    print("Hello, World!")
````

> This is a blockquote example.

### Table Example
| Feature | Status |
|---------|--------|
| Markdown | ✓ |
| CSS | ✓ |
| Preview | ✓ |
| PDF Export | ✓ |
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

h2 {
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 5px;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 0;
    padding-left: 20px;
    font-style: italic;
    background-color: #f8f9fa;
    padding: 10px 20px;
}

code {
    background-color: #f8f8f8;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
}

pre {
    background-color: #f8f8f8;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
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
    
    def md_to_html(self, md_content, css_content):
        """Convert markdown to HTML with CSS styling."""
        # Convert markdown to HTML
        html_body = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks', 'codehilite'])
        
        # Create full HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DasMDF Preview</title>
    <style>
        {css_content}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
        
        return html_content
    
    def preview_doc(self):
        """Preview the markdown document in browser."""
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        
        try:
            # Convert to HTML
            html_content = self.md_to_html(md_content, css_content)
            
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                           delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_file = f.name
            
            # Open in browser
            webbrowser.open(f'file://{os.path.abspath(temp_file)}')
            messagebox.showinfo("Preview", "Preview opened in your default browser!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create preview: {e}")
    
    def convert_pdf(self):
        """Convert markdown to PDF using WeasyPrint."""
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Convert to HTML
            html_content = self.md_to_html(md_content, css_content)
            
            # Convert HTML to PDF using WeasyPrint
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(file_path)
            
            messagebox.showinfo("Success", f"PDF saved successfully!\nLocation: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to PDF: {e}")
    
    def run(self):
        self.root.mainloop()

def main():
    app = MarkdownToPDFConverter()
    app.run()

if __name__ == "__main__":
    main()
