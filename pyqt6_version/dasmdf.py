#!/usr/bin/env python3
"""
DasMDF - Markdown to PDF Converter
PyQt6 Version - Base Foundation

A professional GUI application for converting Markdown files to PDF format.
This is the main PyQt6 implementation with enhanced features and capabilities.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QTextEdit, QPushButton, QProgressBar, 
    QFileDialog, QMessageBox, QComboBox, QFrame
)
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

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title_label = QLabel("Markdown to DasMDF")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Content frame
        content_frame = QFrame()
        content_layout = QGridLayout()
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)
        
        # Markdown section
        md_label = QLabel("Markdown Content")
        md_font = QFont()
        md_font.setPointSize(12)
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
        
        # Button layout
        button_layout = QHBoxLayout()
        content_layout.addLayout(button_layout, 2, 0, 1, 2)
        
        # Buttons
        load_md_btn = QPushButton("Load Markdown")
        load_md_btn.clicked.connect(self.load_markdown_file)
        button_layout.addWidget(load_md_btn)
        
        load_css_btn = QPushButton("Load CSS")
        load_css_btn.clicked.connect(self.load_css_file)
        button_layout.addWidget(load_css_btn)
        
        preview_btn = QPushButton("Preview HTML")
        preview_btn.clicked.connect(self.preview_document)
        button_layout.addWidget(preview_btn)
        
        # Engine selection
        engine_label = QLabel("Engine:")
        button_layout.addWidget(engine_label)
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["playwright", "weasyprint", "wkhtml", "md2pdf"])
        button_layout.addWidget(self.engine_combo)
        
        convert_btn = QPushButton("Convert to PDF")
        convert_btn.clicked.connect(self.convert_to_pdf)
        convert_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(convert_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        content_layout.addWidget(self.progress_bar, 3, 0, 1, 2)
        
        # Status label
        self.status_label = QLabel("Ready to convert")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.status_label, 4, 0, 1, 2)
        
        # Add default content
        self.add_default_content()
    
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
    
    # Set dark theme
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QTextEdit {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            color: #ffffff;
        }
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 8px;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #606060;
        }
        QComboBox {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 5px;
            color: #ffffff;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            border: none;
        }
        QProgressBar {
            border: 1px solid #555555;
            text-align: center;
            background-color: #3c3c3c;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
        }
        QLabel {
            color: #ffffff;
        }
    """)
    
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
