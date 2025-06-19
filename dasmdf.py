"""
DasMDF - Markdown to PDF Converter
CustomTkinter Version - WeasyPrint Engine Integration

A simple GUI application for converting Markdown files to PDF format.
Now includes WeasyPrint engine and HTML preview functionality.
"""

from pathlib import Path
import threading
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tempfile
import webbrowser
import markdown2
import pdfkit
from pygments.formatters import HtmlFormatter
from weasyprint import HTML
import subprocess
import asyncio
from playwright.async_api import async_playwright

class MarkdownToPDFConverter:
    def __init__(self):
        self.wkhtmltopdf_path = self.find_wkhtmltopdf()
        self.engine="playwright"
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("DasMDF - Markdown to PDF Converter")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        # Grid configuration for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
    
    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(self.root, text="DasMDF Converter", 
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
       
        main_container = ctk.CTkFrame(self.root)
        main_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        main_container.grid_columnconfigure((0, 1), weight=1)
        main_container.grid_rowconfigure(1, weight=1)

        md_label = ctk.CTkLabel(main_container, text="Markdown Content", font=ctk.CTkFont(size=16, weight="bold"))
        md_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.md_textbox = ctk.CTkTextbox(
            main_container,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.md_textbox.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew")
        
        # CSS section
        css_label = ctk.CTkLabel(main_container, text="CSS Styling", font=ctk.CTkFont(size=16, weight="bold"))
        css_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.css_textbox = ctk.CTkTextbox(
            main_container,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.css_textbox.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew")
        
        # Button container
        buttons_container = ctk.CTkFrame(main_container)
        buttons_container.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        buttons_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Buttons
        load_md_btn = ctk.CTkButton(
            buttons_container,
            text="Load Markdown",
            command=self.load_md_file,
            height=35
        )
        load_md_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        load_css_btn = ctk.CTkButton(
            buttons_container,
            text="Load CSS",
            command=self.load_css_file,
            height=35
        )
        load_css_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        preview_btn = ctk.CTkButton(
            buttons_container,
            text="Preview HTML",
            command=self.preview_doc,
            height=35,
            fg_color="gray",
            hover_color="darkgray"
        )
        preview_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        # Engine selection dropdown
        self.engine_var = tk.StringVar(value="playwright")
        engine_label = ctk.CTkLabel(
            buttons_container,
            text="Engine:",
            font=ctk.CTkFont(size=14)
        )
        engine_label.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        engine_options = ["playwright","weasyprint", "wkhtml"]
        engine_menu = ctk.CTkOptionMenu(
            buttons_container,
            variable=self.engine_var,
            values=engine_options,
            # width=120
        )
        engine_menu.grid(row=0, column=4, padx=5, pady=10, sticky="ew")
        
        
        convert_btn = ctk.CTkButton(
            buttons_container,
            text="Convert to PDF",
            command=self.convert_pdf,
            height=35,
            fg_color="green",
            hover_color="darkgreen"
        )
        convert_btn.grid(row=0, column=5, padx=5, pady=10, sticky="ew")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_container)
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_container, text="Ready to convert", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10))
        
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
    
    def update_status(self, message):
        self.status_label.configure(text=message)
        self.root.update_idletasks()

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
                self.update_status(f"Loaded: {Path(file_path).name}")
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
                self.update_status(f"Loaded CSS: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def md_to_html(self, md_content, css_content, pdfTitle="DasMDF Preview"):
        """Convert markdown to HTML with CSS styling."""
        # Convert markdown to HTML
        html_body = markdown2.markdown(md_content, extras=['strike', 'fenced-code-blocks', 'codehilite', 'tables', 'toc', 'attr_list', 'latex'])
        pygments_css = HtmlFormatter(style="default").get_style_defs('.codehilite')

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
            self.update_status("HTML preview opened in browser")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create preview: {e}")
    
    def convert_pdf(self):
        """Convert markdown to PDF using the selected engine."""
        self.update_status("Starting PDF conversion...")
        self.progress_bar.set(0.1)

        self.engine = self.engine_var.get()
        if self.engine not in ["playwright","weasyprint", "wkhtml"]:   
            messagebox.showerror("Error", "Invalid conversion engine selected!")
            return

        md_content = self.md_textbox.get("0.0", "end-1c").strip()
        if not md_content:
            messagebox.showerror("Error", "No markdown content to convert!")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        # Show a dialog to enter the PDF title
        # Extract the default title from the output file name (without extension)
        default_title = Path(output_path).stem

        # title_dialog = ctk.CTkInputDialog(
        #     title="Save as PDF",
        #     text="Please enter a title for your PDF:"
        # )

        # pdfTitle = title_dialog.get_input()
        pdfTitle=default_title

        # Exit if the user cancels the dialog (closes or presses cancel)
        if pdfTitle is None:
            return
        
        if output_path:
            if self.engine == "weasyprint":
                thread = threading.Thread(target=self.convert_to_pdf_thread_weasyprint, args=(output_path,pdfTitle))
                thread.daemon = True
                thread.start()
            elif self.engine == "wkhtml":
                thread = threading.Thread(target=self.convert_to_pdf_thread_wkhtml, args=(output_path,pdfTitle))
                thread.daemon = True
                thread.start()
            elif self.engine == "playwright":
                thread = threading.Thread(target=self.convert_to_pdf_thread_playwright, args=(output_path,pdfTitle))
                thread.daemon = True
                thread.start()

        # """Convert markdown to PDF using WeasyPrint."""
        # self.progress_bar.set(0.1)
        # self.update_status("Preparing conversion...")
    
        # md_content = self.md_textbox.get("1.0", tk.END).strip()
        # css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        # if not md_content:
        #     messagebox.showwarning("Warning", "Please add some markdown content!")
        #     return
        
        # self.progress_bar.set(0.3)
        # self.update_status("Converting Markdown to HTML...")
        # # Ask for save location
        # file_path = filedialog.asksaveasfilename(
        #     title="Save PDF As",
        #     defaultextension=".pdf",
        #     filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        # )
        
        # if not file_path:
        #     return
        
        # try:

        #     self.progress_bar.set(0.7)
        #     self.update_status("Generating PDF with WeasyPrint...")

        #     # Convert to HTML
        #     html_content = self.md_to_html(md_content, css_content)
            
        #     # Convert HTML to PDF using WeasyPrint
        #     html_doc = HTML(string=html_content)
        #     html_doc.write_pdf(file_path)

        #     self.progress_bar.set(1.0)
        #     self.update_status(f"PDF saved successfully: {Path(file_path).name}")

        #     if messagebox.askyesno("Success", f"PDF created successfully!\n\nFile: {Path(file_path).name}\n\nOpen the file now?"):
        #         if os.name == 'nt':
        #             os.startfile(file_path)
        #         elif sys.platform == 'darwin':
        #             subprocess.run(['open', output_path])
        #         else:
        #             subprocess.run(['xdg-open', output_path])
            
        # except Exception as e:
        #     messagebox.showerror("Error", f"Failed to convert to PDF: {e}")
    
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
                    subprocess.run([path, "--version"], capture_output=True, check=True)
                    return path
            except Exception:
                continue
        return None
    
    def convert_to_pdf_thread_wkhtml(self, output_path, pdfTitle):
        """Convert markdown to PDF using wkhtmltopdf."""
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        self.progress_bar.set(0.3)
        self.update_status("Preparing conversion with wkhtmltopdf...")

        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        
        file_path = output_path
        
        if not file_path:
            return
        
        try:
            # Convert to HTML
            self.progress_bar.set(0.5)
            self.update_status("[WKHTMLTOPDF] Converting Markdown to HTML...")

            html_content = self.md_to_html(md_content, css_content, pdfTitle)

            self.progress_bar.set(0.8)
            self.update_status("Generating high-quality PDF with wkhtmltopdf...")
            # Configure wkhtmltopdf options
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
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path) if self.wkhtmltopdf_path != "wkhtmltopdf" else None
            
            # Convert to PDF using pdfkit
            pdfkit.from_string(html_content, file_path, options=options, configuration=config)

            self.progress_bar.set(1.0)
            self.update_status(f"PDF saved successfully: {Path(file_path).name}")

            if messagebox.askyesno("Success", f"PDF created successfully!\n\nFile: {Path(file_path).name}\n\nOpen the file now?"):
                if os.name == 'nt':
                    os.startfile(file_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', file_path])
                else:
                    subprocess.run(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to PDF: {e}")

    def convert_to_pdf_thread_weasyprint(self, output_path, pdfTitle):
        """Convert markdown to PDF using WeasyPrint."""
        self.progress_bar.set(0.3)
        self.update_status("Preparing conversion with weasyprint...")
    
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        
        self.progress_bar.set(0.5)
        self.update_status("[WEASYPRINT] Converting Markdown to HTML...")
        
        if not output_path:
            return
        
        try:

            self.progress_bar.set(0.7)
            self.update_status("Generating PDF with WeasyPrint...")

            # Convert to HTML
            html_content = self.md_to_html(md_content, css_content, pdfTitle)
            
            # Convert HTML to PDF using WeasyPrint
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(output_path)

            self.progress_bar.set(1.0)
            self.update_status(f"PDF saved successfully: {Path(output_path).name}")

            if messagebox.askyesno("Success", f"PDF created successfully!\n\nFile: {Path(output_path).name}\n\nOpen the file now?"):
                if os.name == 'nt':
                    os.startfile(output_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', output_path])
                else:
                    subprocess.run(['xdg-open', output_path])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to PDF: {e}")

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
    
    def convert_to_pdf_thread_playwright(self, output_path, pdfTitle):
        """Convert markdown to PDF using Playwright."""
        md_content = self.md_textbox.get("1.0", tk.END).strip()
        css_content = self.css_textbox.get("1.0", tk.END).strip()
        
        self.progress_bar.set(0.3)
        self.update_status("Preparing conversion with Playwright...")

        if not md_content:
            messagebox.showwarning("Warning", "Please add some markdown content!")
            return
        
        file_path = output_path
        
        if not file_path:
            return
        
        try:
            self.progress_bar.set(0.5)
            self.update_status("[PLAYWRIGHT] Converting Markdown to HTML...")
            # Convert to HTML
            html_content = self.md_to_html(md_content, css_content, pdfTitle)
            
            self.progress_bar.set(0.8)
            self.update_status("Generating PDF with Playwright...")
            # Run async conversion
            asyncio.run(self.html_to_pdf_async(html_content, file_path))
            
            self.progress_bar.set(1.0)
            self.update_status(f"PDF saved successfully: {Path(file_path).name}")
            if messagebox.askyesno("Success", f"PDF created successfully!\n\nFile: {Path(file_path).name}\n\nOpen the file now?"):
                if os.name == 'nt':
                    os.startfile(file_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', file_path])
                else:
                    subprocess.run(['xdg-open', file_path])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to PDF: {e}")

    def run(self):
        self.root.mainloop()

def main():
    app = MarkdownToPDFConverter()
    app.run()

if __name__ == "__main__":
    main()
