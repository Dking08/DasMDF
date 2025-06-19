# DasMDF - Markdown to PDF Converter

**DasMDF** is a Python-based desktop application with a modern **CustomTkinter** GUI that converts Markdown (`.md`) files into beautiful PDF documents using multiple rendering engines. Designed to be simple, fast, and flexible, it's perfect for developers, students, researchers, and writers.

## 🌟 Highlights

- Sleek and responsive **CustomTkinter** GUI
- Single-file architecture (`dasmdf.py`)
- Supports **three powerful rendering engines**
- Converts Markdown to PDF in one click
- Preview-friendly engine features (like LaTeX, code, emojis)

## 🧠 Rendering Engines Overview

### 🔹 1. **Playwright**

- **Type**: Chromium browser (headless)
- **Quality**: ⭐ Best
- **Speed**: ⚡ Fastest
- **Supports**:
  - Full CSS
  - LaTeX (MathJax)
  - Code highlighting
  - Emojis, images

### 🔹 2. **WeasyPrint**

- **Type**: Pure Python
- **Quality**: ⭐ Medium
- **Speed**: 🐢 Slowest
- **Supports**:
  - CSS, code highlighting
  - Emojis and LaTeX (poor rendering)
  - Basic image support

### 🔹 3. **wkhtmltopdf**

- **Type**: Native executable
- **Quality**: ⭐ Lowest
- **Speed**: 🚀 Faster than WeasyPrint
- **Supports**:
  - Basic CSS, image support
  - Poor LaTeX
  - No emoji support

## 📦 Installation

### 1. Install `wkhtmltopdf`

- **Windows**: [Download here](https://wkhtmltopdf.org/downloads.html)  
- **Linux**:

  ```bash
  sudo apt install wkhtmltopdf

    ```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install
```

## 🖥️ Usage

Run the GUI app:

```bash
python dasmdf.py
```

Use the interface to:

- Write or load a Markdown file
- Write or load a CSS file (optional)
- Choose an engine
- Export to PDF with a single click

## 🗃️ Branches

- `main` – stable release
- `dev` – experimental features, testing

## 🧩 Project Structure

```plaintext
DasMDF/
├── dasmdf.py
├── requirements.txt
└── README.md
```

## 🤝 Contributing

We’d love your help!
Fork the repo, raise issues, or submit PRs. All contributions are welcome—UI, logic, performance, or docs.

Please follow [PEP8](https://peps.python.org/pep-0008/) and use meaningful commit messages.

## 📜 License

MIT License – see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Playwright](https://playwright.dev/)
- [WeasyPrint](https://weasyprint.org/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)
- [Python-Markdown](https://python-markdown.github.io/)

---

> ⚠️ Note: This app is GUI-only and doesn’t support CLI usage currently.

---
