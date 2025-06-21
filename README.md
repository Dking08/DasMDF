# DasMDF - Markdown to PDF Converter

**DasMDF** is a modern desktop GUI tool that converts Markdown (`.md`) files into beautifully formatted PDF documents using multiple rendering engines. Built using **PyQt6** (with a legacy version in CustomTkinter), DasMDF is fast, flexible, and ready for open-source contribution.

---

## ⬇️ Download

A ready-to-use **Windows executable** for the PyQt6 version is available—no setup required!  
The `.exe` includes all dependencies, including **wkhtmltopdf** and **Playwright** (note: this increases the file size).

- [Download the latest release from GitHub](https://github.com/Dking08/DasMDF/releases)

Just download, extract, and run the executable.

---

## 🧠 Why DasMDF?

- Convert Markdown to PDF in a click
- Supports **multiple rendering engines**
- **PyQt6 UI** for rich, responsive user experience
- Code highlighting, LaTeX, emoji & image rendering support (engine-dependent)
- Simple, elegant design for daily use

---

## 📁 Project Structure

```plaintext
DasMDF/
├── pyqt6_version/
│   ├── dasmdf.py
│   ├── requirements.txt
│   └── icon/
│       └── icon.png
├── ctk\_version/   ← Legacy version (CustomTkinter)
│   ├── dasmdf.py
│   └── requirements.txt
├── assets/
│   └── \*.css
├── LICENSE
└── README.md

````

---

## 🖥️ Current Version: PyQt6

The **PyQt6 version** is the primary and actively developed version of DasMDF.  
We transitioned from CustomTkinter because:

- CTk lacks proper emoji rendering in text boxes
- PyQt6 provides more flexibility, better widget control, and cross-platform rendering consistency

To run:

```bash
cd pyqt6_version
pip install -r requirements.txt
python dasmdf.py
````

---

## 🧪 Legacy Version: CustomTkinter

You can still use the legacy CTk GUI version (not actively maintained):

```bash
cd ctk_version
pip install -r requirements.txt
python dasmdf.py
```

---

## 🧠 Rendering Engines

| Engine          | Type              | Quality  | Speed      | Supports                                               |
| --------------- | ----------------- | -------- | ---------- | ------------------------------------------------------ |
| **Playwright**  | Headless browser  | ⭐ Best   | ⚡ Fastest  | Full CSS, LaTeX (MathJax), code, images, emojis        |
| **WeasyPrint**  | Pure Python       | ⭐ Medium | 🐢 Slowest | CSS, code highlighting, limited image/emoji/LaTeX      |
| **wkhtmltopdf** | Native executable | ⭐ Low    | 🚀 Faster  | Basic CSS, poor LaTeX, partial image, no emoji support |

---

## 📦 Installation

### 1. Install `wkhtmltopdf`

- **Windows**: [Download](https://wkhtmltopdf.org/downloads.html) and add to PATH
- **Linux**:

  ```bash
  sudo apt install wkhtmltopdf
  ```

### 2. Install Python dependencies

Use the relevant version's requirements file:

```bash
# For PyQt6 version
cd pyqt6_version
pip install -r requirements.txt

# For CTk version (legacy)
cd ctk_version
pip install -r requirements.txt
```

### 3. Install Playwright Browsers (shared)

```bash
playwright install
```

---

## 📌 Roadmap

- ✅ **Switch to PyQt6**
- ✅ Version-specific `requirements.txt`
- ✅ **Executable build for PyQt6 (with all dependencies)**
- 🔜 Markdown live preview
- 🔜 Settings and export options
- 🔜 CLI support (optional)

---

## 🤝 Contributing

We welcome pull requests and issue reports!
Please follow [PEP8](https://peps.python.org/pep-0008/) guidelines and keep your commits clean and descriptive.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [PyQt6](https://riverbankcomputing.com/software/pyqt/)
- [Playwright](https://playwright.dev/)
- [WeasyPrint](https://weasyprint.org/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)
- [Python-Markdown](https://python-markdown.github.io/)
