#!/usr/bin/env python3
"""
DasMDF - Markdown to PDF Converter
PyQt6 Version - Base Foundation

A professional GUI application for converting Markdown files to PDF format.
This is the main PyQt6 implementation with enhanced features and capabilities.
"""

import subprocess
import sys
import os
from pathlib import Path
import tempfile
import webbrowser
import markdown2
from pygments.formatters import HtmlFormatter
from weasyprint import HTML
import pdfkit
import asyncio
from playwright.async_api import async_playwright
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QTextEdit, QPushButton, QProgressBar, 
    QFileDialog, QMessageBox, QComboBox, QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class ConversionThread(QThread):
    """Thread for handling PDF conversion to prevent UI freezing"""
    progress_updated = pyqtSignal(float)
    status_updated = pyqtSignal(str)
    conversion_finished = pyqtSignal(bool, str)

    def __init__(self, engine, md_content, css_content, output_path, pdf_title, wkhtmltopdf_path=None):
        """Initialize the conversion thread with necessary parameters."""
        super().__init__()
        self.engine = engine
        self.md_content = md_content
        self.css_content = css_content
        self.output_path = output_path
        self.pdf_title = pdf_title
        self.wkhtmltopdf_path = wkhtmltopdf_path

    def run(self):
        try:
            if self.engine == "weasyprint":
                self.convert_with_weasyprint()
            elif self.engine == "wkhtml":
                self.conert_with_wkhtml()
            elif self.engine == "playwright":
                self.convert_with_playwright()
            else:
                self.conversion_finished.emit(
                    False, "Unsupported conversion engine selected."
                )
            
        except Exception as e:
            self.conversion_finished.emit(False, f"Failed to convert to PDF:\n\n{str(e)}")
    
    def md_to_html(self, md_content, css_content, pdfTitle="DasMDF Preview"):
        """Convert markdown to HTML with CSS styling."""
        # Convert markdown to HTML
        html_body = markdown2.markdown(
            md_content,
            extras=[
                'strike', 'fenced-code-blocks', 'codehilite', 'tables',
                'toc', 'attr_list', 'latex'
            ]
        )
        pygments_css = HtmlFormatter(style="default").get_style_defs(
            '.codehilite'
        )

        # Create full HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{pdfTitle}</title>
    <style>
    pre, code {{
            white-space: pre-wrap;
            word-break: break-word;
            overflow-wrap: anywhere;
            }}
        {css_content}
        {pygments_css}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

</head>
<body>
    {html_body}
</body>
</html>"""

        return html_content

    def convert_with_weasyprint(self):
        self.progress_updated.emit(0.3)
        self.status_updated.emit("Preparing conversion with weasyprint...")

        self.progress_updated.emit(0.5)
        self.status_updated.emit("[WEASYPRINT] Converting Markdown to HTML...")
        try:
            html_content = self.md_to_html(self.md_content, self.css_content, self.pdf_title)
            self.progress_updated.emit(0.7)
            self.status_updated.emit("Generating PDF with WeasyPrint...")

            # Convert HTML to PDF
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(self.output_path)
            self.progress_updated.emit(1.0)
            self.status_updated.emit("[WEASYPRINT] Conversion completed successfully!")

            self.conversion_finished.emit(True, f"PDF saved to: {self.output_path}", "weasyprint")

        except Exception as e:
            self.progress_updated.emit(0.0)
            self.status_updated.emit(f"[WEASYPRINT] Conversion failed: {str(e)}")
            self.conversion_finished.emit(False, f"Conversion failed: {str(e)}")
    
    def conert_with_wkhtml(self):
        """Convert markdown to PDF using wkhtmltopdf."""
        self.progress_updated.emit(0.3)
        self.status_updated.emit("Preparing conversion with wkhtmltopdf...")
        if not self.wkhtmltopdf_path:
            self.conversion_finished.emit(False, "wkhtmltopdf executable not found.")
            return

        self.progress_updated.emit(0.5)
        self.status_updated.emit("[WKHTMLTOPDF] Converting Markdown to HTML...")

        try:
            html_content = self.md_to_html(self.md_content, self.css_content, self.pdf_title)
            self.progress_updated.emit(0.7)
            self.status_updated.emit("Generating PDF with wkhtmltopdf...")

            options = {
                'page-size': 'A4',
                # 'margin-top': '20mm',
                # 'margin-right': '20mm',
                # 'margin-bottom': '20mm',
                # 'margin-left': '20mm',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
                'disable-smart-shrinking': None,
                'dpi': 300,
                'image-dpi': 300,
                'image-quality': 100,
                'lowquality': False,
                'minimum-font-size': 8,
                'zoom': 1.0
            }

            options['enable-javascript'] = None
            options['javascript-delay'] = 1000

            # Set the path to wkhtmltopdf if we found it
            config = (
                pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
                if self.wkhtmltopdf_path != "wkhtmltopdf"
                else None
            )

            # Convert to PDF using pdfkit
            pdfkit.from_string(
                html_content, self.output_path, options=options, configuration=config
            )
            self.progress_updated.emit(1.0)
            self.status_updated.emit("[WKHTMLTOPDF] Conversion completed successfully!")

            self.conversion_finished.emit(True, f"PDF saved to: {self.output_path}", "wkhtmltopdf")
        except Exception as e:
            self.progress_updated.emit(0.0)
            self.status_updated.emit(f"[WKHTMLTOPDF] Conversion failed: {str(e)}")
            self.conversion_finished.emit(False, f"Conversion failed: {str(e)}")
    
    async def html_to_pdf_async(self, html_content, output_path):
        """Convert HTML to PDF using Playwright asynchronously."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set HTML content and wait for network idle
            await page.set_content(html_content, wait_until="networkidle")

            # Generate PDF with options
            await page.pdf(
                path=output_path,
                format='A4',
                print_background=True
            )

            await browser.close()
    
    def convert_with_playwright(self):
        """Convert markdown to PDF using Playwright."""
        self.progress_updated.emit(0.3)
        self.status_updated.emit("Preparing conversion with Playwright...")

        try:

            self.progress_updated.emit(0.5)
            self.status_updated.emit("[PLAYWRIGHT] Converting Markdown to HTML...")

            html_content = self.md_to_html(self.md_content, self.css_content, self.pdf_title)

            self.progress_updated.emit(0.7)
            self.status_updated.emit("Generating PDF with Playwright...")

            asyncio.run(self.html_to_pdf_async(html_content, self.output_path))

            self.progress_updated.emit(1.0)
            self.status_updated.emit("[PLAYWRIGHT] Conversion completed successfully!")

            self.conversion_finished.emit(True, f"PDF saved to: {self.output_path}", "playwright")

        except Exception as e:
            self.progress_updated.emit(0.0)
            self.status_updated.emit(f"[PLAYWRIGHT] Conversion failed: {str(e)}")
            self.conversion_finished.emit(False, f"Conversion failed: {str(e)}")

class MarkdownToPDFConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()
        self.wkhtmltopdf_path = self.find_wkhtmltopdf()
    
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
                self.update_status(f"Loaded: {Path(file_path).name}")
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
                self.update_status(f"Loaded CSS: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSS file: {str(e)}")
    
    def preview_document(self):
        """Preview the document (placeholder)."""
        try:
            md_content = self.md_textbox.toPlainText()
            css_content = self.css_textbox.toPlainText()
            
            if not md_content.strip():
                QMessageBox.warning(self, "Warning", "No markdown content to preview!")
                return
            
            html_content = ConversionThread.md_to_html(
                self, md_content, css_content, pdfTitle="DasMDF Preview"
            )
            
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False, encoding='utf-8'
            ) as f:
                f.write(html_content)
                temp_file = f.name

            # Open in browser
            webbrowser.open(f'file://{os.path.abspath(temp_file)}')
            self.update_status("Preview opened in browser.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to preview HTML: {str(e)}")

    def find_wkhtmltopdf(self):
        """Find the wkhtmltopdf executable in the system PATH."""
        # First, try searching in PATH
        for path in os.environ["PATH"].split(os.pathsep):
            exe_path = Path(path) / "wkhtmltopdf"
            if exe_path.exists() and exe_path.is_file():
                return str(exe_path)

        # Then, try common installation paths (Windows)
        common_paths = [
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
            "wkhtmltopdf"  # If in PATH as a command
        ]
        for path in common_paths:
            try:
                if os.path.exists(path):
                    return path
                elif path == "wkhtmltopdf":
                    subprocess.run(
                        [path, "--version"], capture_output=True, check=True
                    )
                    return path
            except Exception:
                continue
        return None
    
    def convert_to_pdf(self):
        engine = self.engine_combo.currentText()
        md_content = self.md_textbox.toPlainText().strip()
        
        if not md_content:
            QMessageBox.critical(self, "Error", "No markdown content to convert!")
            return
        
        # Get PDF title
        pdf_title, ok = QInputDialog.getText(self, "Save as PDF", "Please enter a title for your PDF:")
        if not ok:
            self.update_status("PDF conversion cancelled.")
            return
        if not pdf_title:
            pdf_title = "DasMDF Document"
        
        # Get output path
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF files (*.pdf);;All files (*.*)"
        )
        
        if not output_path:
            self.update_status("PDF conversion cancelled.")
            return
        
        css_content = self.css_textbox.toPlainText()
        
        # Create and start conversion thread
        self.conversion_thread = ConversionThread(
            engine, md_content, css_content, output_path, pdf_title, self.wkhtmltopdf_path
        )
        # Connect signals
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.status_updated.connect(self.update_status)
        self.conversion_thread.conversion_finished.connect(self.on_conversion_finished)
        
        self.conversion_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)
        QApplication.processEvents()

    def update_progress(self, value):
        self.progress_bar.setValue(int(value * 100))
    
    def on_conversion_finished(self, success, message, engine=None):
        self.progress_bar.setValue(0)
        
        if success:
            if engine:
                self.update_status(f"Conversion completed successfully with {engine}!")
            else:
                self.update_status("Conversion completed successfully!")
            
            reply = QMessageBox.question(
                self, 
                "Success", 
                f"PDF created successfully!\n\nFile: {message.split(': ')[-1]}\n\nOpen the file now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                output_path = self.conversion_thread.output_path
                if os.name == 'nt':
                    os.startfile(output_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', output_path])
                else:
                    subprocess.run(['xdg-open', output_path])
        else:
            QMessageBox.critical(self, "Error", message)
        
        self.update_status("Ready to convert")

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
