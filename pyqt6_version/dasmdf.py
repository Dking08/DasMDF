#!/usr/bin/env python3
"""
DasMDF - Markdown to PDF Converter
PyQt6 Version - Base Foundation

A professional GUI application for converting Markdown files to PDF format.
This is the main PyQt6 implementation with enhanced features and capabilities.
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QTextEdit, 
                            QPushButton, QFileDialog, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MarkdownToPDFConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main application window."""
        self.setWindowTitle("DasMDF - Markdown to PDF Converter")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
    
    def create_widgets(self):
        """Create and arrange the GUI widgets."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title section
        self.create_title_section(main_layout)
        
        # Content area
        self.create_content_area(main_layout)
        
        # Button section
        self.create_button_section(main_layout)
    
    def create_title_section(self, parent_layout):
        """Create the title section."""
        title_label = QLabel("DasMDF Converter")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(title_label)
    
    def create_content_area(self, parent_layout):
        """Create the main content area with text editors."""
        # Content frame
        content_frame = QFrame()
        content_layout = QGridLayout(content_frame)
        parent_layout.addWidget(content_frame)
        
        # Markdown section
        md_label = QLabel("Markdown Content")
        md_font = QFont()
        md_font.setPointSize(16)
        md_font.setBold(True)
        md_label.setFont(md_font)
        content_layout.addWidget(md_label, 0, 0)
        
        self.md_textbox = QTextEdit()
        mono_font = QFont("Consolas", 10)
        self.md_textbox.setFont(mono_font)
        content_layout.addWidget(self.md_textbox, 1, 0)
        
        # CSS section
        css_label = QLabel("CSS Styling")
        css_label.setFont(md_font)
        content_layout.addWidget(css_label, 0, 1)
        
        self.css_textbox = QTextEdit()
        self.css_textbox.setFont(mono_font)
        content_layout.addWidget(self.css_textbox, 1, 1)
        
        # Set equal column widths
        content_layout.setColumnStretch(0, 1)
        content_layout.setColumnStretch(1, 1)
        
        # Add default content
        self.add_default_content()
    
    def create_button_section(self, parent_layout):
        """Create the button section."""
        button_layout = QHBoxLayout()
        parent_layout.addLayout(button_layout)
        
        # Load MD button
        self.load_md_btn = QPushButton("Load MD")
        self.load_md_btn.clicked.connect(self.load_markdown_file)
        button_layout.addWidget(self.load_md_btn)
        
        # Load CSS button
        self.load_css_btn = QPushButton("Load CSS")
        self.load_css_btn.clicked.connect(self.load_css_file)
        button_layout.addWidget(self.load_css_btn)
        
        # Preview button
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(self.preview_document)
        button_layout.addWidget(self.preview_btn)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_to_pdf)
        button_layout.addWidget(self.convert_btn)
    
    def add_default_content(self):
        """Add default sample content."""
        # Default markdown
        default_md = """# Sample Document

This is a **sample** markdown document for the PyQt6 version.

## Features
- Professional PyQt6 interface
- Enhanced functionality
- Multiple engine support (coming soon)

### Code Example

```python
print("DasMDF - Markdown to PDF Converter (PyQt6)")
```

> This is a blockquote example for the PyQt6 version.

### Table Example
| Feature | Status |
|---------|--------|
| PyQt6 Interface | ✓ |
| Markdown Support | ✓ |
| CSS Styling | ✓ |
| PDF Export | Coming Soon |
"""
        self.md_textbox.setPlainText(default_md)
        
        # Default CSS
        default_css = """body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 40px;
    color: #2c3e50;
}

h1, h2, h3 {
    color: #34495e;
    font-weight: 600;
}

h1 {
    font-size: 2em;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.3em;
}

h2 {
    font-size: 1.5em;
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 0.3em;
}

blockquote {
    margin: 1em 0;
    padding: 0.8em 1.2em;
    border-left: 4px solid #3498db;
    background-color: #f8f9fa;
    font-style: italic;
}

code {
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 1em;
    margin: 1em 0;
    overflow-x: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
}"""
        self.css_textbox.setPlainText(default_css)
    
    def load_markdown_file(self):
        """Load a markdown file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Markdown File", 
            "", 
            "Markdown files (*.md *.markdown);;Text files (*.txt);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.md_textbox.setPlainText(content)
                QMessageBox.information(self, "Success", f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    
    def load_css_file(self):
        """Load a CSS file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select CSS File", 
            "", 
            "CSS files (*.css);;Text files (*.txt);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.css_textbox.setPlainText(content)
                QMessageBox.information(self, "Success", f"Loaded CSS: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSS file: {str(e)}")
    
    def preview_document(self):
        """Preview the document (placeholder)."""
        QMessageBox.information(
            self, 
            "Preview", 
            "Preview functionality will be implemented in the next version.\n\n"
            "This will show a rendered preview of your markdown content."
        )
    
    def convert_to_pdf(self):
        """Convert to PDF (placeholder)."""
        md_content = self.md_textbox.toPlainText().strip()
        
        if not md_content:
            QMessageBox.warning(self, "Warning", "Please add some markdown content first.")
            return
        
        QMessageBox.information(
            self, 
            "Convert to PDF", 
            "PDF conversion functionality will be implemented in the next version.\n\n"
            f"Ready to convert {len(md_content)} characters of markdown content."
        )

def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Print startup info
    print("DasMDF - Markdown to PDF Converter (PyQt6)")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("Starting PyQt6 GUI...")
    
    converter = MarkdownToPDFConverter()
    converter.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
