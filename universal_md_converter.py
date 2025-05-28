#!/usr/bin/env python3
"""
Universal Markdown Converter - GUI Application
A comprehensive, portable GUI tool for converting Markdown files to HTML and PDF
Combines all conversion functionality into a single script with an easy-to-use interface

Features:
- Convert single MD files to HTML/PDF
- Batch convert multiple files
- Professional styling with preserved formatting
- Option to remove auto-generated headers
- Cross-platform compatibility
- Easy-to-use graphical interface
- No external dependencies except standard libraries + markdown

Usage:
    python universal_md_converter.py                            # Launch GUI application

The application will automatically launch the GUI interface for easy file conversion.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# Try to import markdown, provide fallback if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    print("⚠️  Warning: 'markdown' library not found. Install with: pip install markdown")

class MarkdownConverter:
    """Main converter class with all functionality"""

    def __init__(self):
        self.css_template = self._create_css_template()
        self.html_template = self._create_html_template()

    def _create_css_template(self):
        """Create comprehensive CSS styling"""
        return """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: bold;
            page-break-after: avoid;
        }

        h1 {
            font-size: 2.2em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }

        h2 {
            font-size: 1.8em;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 0.2em;
        }

        h3 { font-size: 1.4em; color: #34495e; }
        h4 { font-size: 1.2em; color: #34495e; }

        p {
            margin-bottom: 1em;
            text-align: justify;
        }

        ul, ol {
            margin-bottom: 1em;
            padding-left: 2em;
        }

        li { margin-bottom: 0.3em; }

        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 0.9em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
            vertical-align: top;
        }

        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }

        tr:nth-child(even) { background-color: #f8f9fa; }
        tr:hover { background-color: #e8f4fd; }

        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', Consolas, monospace;
            font-size: 0.9em;
            color: #e74c3c;
            border: 1px solid #e1e1e1;
        }

        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 1.2em;
            overflow-x: auto;
            margin: 1em 0;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }

        pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
            border: none;
        }

        blockquote {
            border-left: 4px solid #3498db;
            margin: 1em 0;
            padding: 1em 1em 1em 2em;
            color: #666;
            font-style: italic;
            background-color: #f9f9f9;
            border-radius: 0 4px 4px 0;
        }

        a {
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        a:hover {
            color: #2980b9;
            text-decoration: underline;
        }

        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 2em 0;
        }

        strong, b { font-weight: bold; color: #2c3e50; }
        em, i { font-style: italic; }

        .status-complete { color: #27ae60; font-weight: bold; }
        .status-progress { color: #f39c12; font-weight: bold; }
        .status-pending { color: #95a5a6; font-weight: bold; }

        @media print {
            body { font-size: 12pt; line-height: 1.4; }
            h1, h2, h3 { page-break-after: avoid; }
            table, pre { page-break-inside: avoid; }
        }

        @media (max-width: 768px) {
            body { padding: 10px; }
            table { font-size: 0.8em; }
            th, td { padding: 8px 10px; }
        }
        """

    def _create_html_template(self):
        """Create HTML template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    {header_section}
    <div class="content">
        {content}
    </div>
    {footer_section}
</body>
</html>"""

    def _create_header_section(self, title, date):
        """Create header section (can be omitted)"""
        return f"""    <div class="header">
        <h1 class="document-title">{title}</h1>
        <p class="document-meta">Generated on {date} | <a href="#" onclick="window.print()">Print to PDF</a></p>
    </div>"""

    def _create_footer_section(self):
        """Create footer section (can be omitted)"""
        return """    <div class="footer">
        <hr>
        <p style="text-align: center; color: #666; font-size: 0.9em;">
            Converted with Universal Markdown Converter
        </p>
    </div>"""

    def convert_md_to_html(self, input_file, output_file=None, include_headers=True):
        """Convert Markdown file to HTML"""
        if not MARKDOWN_AVAILABLE:
            raise ImportError("Markdown library not available. Install with: pip install markdown")

        input_path = Path(input_file)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if output_file is None:
            output_file = input_path.with_suffix('.html')

        # Read Markdown content
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Configure Markdown extensions
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes'
        ]

        # Convert Markdown to HTML
        md = markdown.Markdown(extensions=extensions)
        html_content = md.convert(md_content)

        # Create complete HTML document
        from datetime import datetime

        # Conditionally include header and footer sections
        if include_headers:
            header_section = self._create_header_section(
                input_path.stem.replace('_', ' ').title(),
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            footer_section = self._create_footer_section()
        else:
            header_section = ""
            footer_section = ""

        full_html = self.html_template.format(
            title=input_path.stem.replace('_', ' ').title(),
            css=self.css_template,
            content=html_content,
            header_section=header_section,
            footer_section=footer_section
        )

        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        return str(output_file)

    def html_to_pdf_chrome(self, html_file, pdf_file):
        """Convert HTML to PDF using Chrome/Chromium"""
        chrome_paths = [
            "chrome", "google-chrome", "chromium", "chromium-browser",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]

        for chrome_path in chrome_paths:
            try:
                subprocess.run([chrome_path, "--version"],
                             capture_output=True, check=True, timeout=5)

                cmd = [
                    chrome_path, "--headless", "--disable-gpu",
                    "--print-to-pdf=" + str(pdf_file),
                    "--print-to-pdf-no-header",
                    "--no-margins", str(html_file)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    return True

            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return False

    def convert_md_to_pdf(self, input_file, output_file=None, include_headers=True):
        """Convert Markdown file to PDF"""
        input_path = Path(input_file)

        if output_file is None:
            output_file = input_path.with_suffix('.pdf')

        # Step 1: Convert to HTML
        html_file = self.convert_md_to_html(input_file, include_headers=include_headers)

        # Step 2: Convert HTML to PDF
        if self.html_to_pdf_chrome(html_file, output_file):
            # Clean up temporary HTML file
            try:
                os.unlink(html_file)
            except:
                pass
            return str(output_file)
        else:
            # Fallback: keep HTML and provide instructions
            print(f"⚠️  Chrome not found. HTML file created: {html_file}")
            print(f"📋 To create PDF: Open {html_file} in browser → Ctrl+P → Save as PDF")
            try:
                webbrowser.open(f"file://{Path(html_file).absolute()}")
            except:
                pass
            return str(html_file)

    def batch_convert(self, input_dir, output_dir=None, to_pdf=False, pattern="*.md", include_headers=True):
        """Batch convert multiple files"""
        input_path = Path(input_dir)
        if not input_path.exists():
            raise ValueError(f"Input directory not found: {input_dir}")

        if output_dir is None:
            output_path = input_path
        else:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

        md_files = list(input_path.glob(pattern))
        if not md_files:
            return []

        results = []
        for md_file in md_files:
            try:
                if to_pdf:
                    output_file = output_path / f"{md_file.stem}.pdf"
                    result = self.convert_md_to_pdf(str(md_file), str(output_file), include_headers=include_headers)
                else:
                    output_file = output_path / f"{md_file.stem}.html"
                    result = self.convert_md_to_html(str(md_file), str(output_file), include_headers=include_headers)

                results.append(result)
                print(f"✅ {md_file.name} → {Path(result).name}")

            except Exception as e:
                print(f"❌ Error converting {md_file.name}: {e}")

        return results

class ConverterGUI:
    """Graphical User Interface for the converter"""

    def __init__(self):
        self.converter = MarkdownConverter()
        self.root = tk.Tk()
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI interface"""
        self.root.title("Universal Markdown Converter")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Set window icon if available
        try:
            # Try to set an icon (will work if icon file exists)
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass  # Ignore if icon not found

        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Universal Markdown Converter",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # File selection
        ttk.Label(main_frame, text="Select Markdown File:").grid(row=1, column=0, sticky=tk.W)
        self.file_var = tk.StringVar()
        file_entry = ttk.Entry(main_frame, textvariable=self.file_var, width=50)
        file_entry.grid(row=1, column=1, padx=(10, 5), sticky=(tk.W, tk.E))

        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=1, column=2, padx=(5, 0))

        # Directory selection for batch
        ttk.Label(main_frame, text="Or Select Directory:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(main_frame, textvariable=self.dir_var, width=50)
        dir_entry.grid(row=2, column=1, padx=(10, 5), sticky=(tk.W, tk.E))

        browse_dir_btn = ttk.Button(main_frame, text="Browse", command=self.browse_directory)
        browse_dir_btn.grid(row=2, column=2, padx=(5, 0))

        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, pady=(20, 10), sticky=(tk.W, tk.E))

        self.output_format = tk.StringVar(value="html")
        ttk.Radiobutton(output_frame, text="HTML", variable=self.output_format,
                       value="html").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(output_frame, text="PDF (requires Chrome)", variable=self.output_format,
                       value="pdf").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))

        # Remove headers option
        self.remove_headers = tk.BooleanVar(value=False)
        ttk.Checkbutton(output_frame, text="Remove headers (Generated on... | Print to PDF)",
                       variable=self.remove_headers).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))

        # Output directory
        ttk.Label(output_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=40)
        output_entry.grid(row=1, column=1, padx=(10, 5), sticky=(tk.W, tk.E))

        output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        output_browse_btn.grid(row=1, column=2, padx=(5, 0))

        # Convert buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 10))

        convert_btn = ttk.Button(button_frame, text="Convert File", command=self.convert_file)
        convert_btn.grid(row=0, column=0, padx=(0, 10))

        batch_btn = ttk.Button(button_frame, text="Batch Convert", command=self.batch_convert)
        batch_btn.grid(row=0, column=1, padx=(10, 0))

        # Progress and log
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))

        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.log_text = tk.Text(log_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(1, weight=1)

    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def browse_file(self):
        """Browse for markdown file"""
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md *.markdown"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)

    def browse_directory(self):
        """Browse for directory"""
        dirname = filedialog.askdirectory(title="Select Directory with Markdown Files")
        if dirname:
            self.dir_var.set(dirname)

    def browse_output_dir(self):
        """Browse for output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_dir_var.set(dirname)

    def convert_file(self):
        """Convert single file"""
        if not self.file_var.get():
            messagebox.showerror("Error", "Please select a markdown file")
            return

        def convert_thread():
            try:
                self.progress.start()
                self.log(f"Converting {Path(self.file_var.get()).name}...")

                output_dir = self.output_dir_var.get() or str(Path(self.file_var.get()).parent)
                include_headers = not self.remove_headers.get()  # Invert because checkbox is "remove"

                if self.output_format.get() == "pdf":
                    result = self.converter.convert_md_to_pdf(
                        self.file_var.get(),
                        str(Path(output_dir) / f"{Path(self.file_var.get()).stem}.pdf"),
                        include_headers=include_headers
                    )
                else:
                    result = self.converter.convert_md_to_html(
                        self.file_var.get(),
                        str(Path(output_dir) / f"{Path(self.file_var.get()).stem}.html"),
                        include_headers=include_headers
                    )

                self.log(f"✅ Success: {result}")
                messagebox.showinfo("Success", f"File converted successfully!\n{result}")

            except Exception as e:
                self.log(f"❌ Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress.stop()

        threading.Thread(target=convert_thread, daemon=True).start()

    def batch_convert(self):
        """Batch convert directory"""
        if not self.dir_var.get():
            messagebox.showerror("Error", "Please select a directory")
            return

        def batch_thread():
            try:
                self.progress.start()
                self.log(f"Batch converting directory: {self.dir_var.get()}")

                output_dir = self.output_dir_var.get() or self.dir_var.get()
                to_pdf = self.output_format.get() == "pdf"
                include_headers = not self.remove_headers.get()  # Invert because checkbox is "remove"

                results = self.converter.batch_convert(
                    self.dir_var.get(), output_dir, to_pdf, include_headers=include_headers
                )

                self.log(f"✅ Batch conversion completed: {len(results)} files")
                messagebox.showinfo("Success", f"Batch conversion completed!\n{len(results)} files converted")

            except Exception as e:
                self.log(f"❌ Batch conversion error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress.stop()

        threading.Thread(target=batch_thread, daemon=True).start()

    def run(self):
        """Run the GUI"""
        self.log("Universal Markdown Converter ready!")
        self.log("Select a file or directory to convert...")
        self.root.mainloop()

def main():
    """Main function - Launch GUI application"""
    # Check if markdown is available
    if not MARKDOWN_AVAILABLE:
        # Show error dialog and offer to install (only if not frozen)
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            if getattr(sys, 'frozen', False):
                # Running as executable - markdown should be bundled
                messagebox.showerror(
                    "Missing Dependencies",
                    "This executable appears to be corrupted or incomplete.\n\n"
                    "The required markdown library is missing.\n\n"
                    "Please download a fresh copy of the application."
                )
            else:
                # Running as script - offer to install
                result = messagebox.askyesno(
                    "Missing Dependencies",
                    "Markdown library is required but not installed.\n\n"
                    "Would you like to install it automatically?\n\n"
                    "This will run: pip install markdown"
                )

                if result:
                    try:
                        print("📦 Installing required dependencies...")
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'markdown'])
                        messagebox.showinfo("Success", "Dependencies installed successfully!\nPlease restart the application.")
                        print("✅ Dependencies installed successfully!")
                        print("Please restart the application to use the new dependencies.")
                    except subprocess.CalledProcessError as e:
                        messagebox.showerror("Installation Failed", f"Failed to install dependencies.\n\nError: {e}\n\nPlease install manually: pip install markdown")
                        print(f"❌ Failed to install dependencies: {e}")
                else:
                    messagebox.showinfo("Manual Installation", "Please install manually:\npip install markdown")
                    print("Please install manually: pip install markdown")

            root.destroy()
            return

        except ImportError:
            print("❌ Markdown library not found and GUI not available.")
            print("Please install manually: pip install markdown")
            return

    # Launch GUI
    try:
        app = ConverterGUI()
        app.run()
    except ImportError as e:
        # Show error dialog for missing tkinter
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing GUI Library", f"GUI requires tkinter.\n\nError: {e}")
            root.destroy()
        except:
            print("❌ GUI requires tkinter. Please install tkinter.")
            print(f"Error: {e}")
    except Exception as e:
        # Show error dialog for other exceptions
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", f"Error starting application:\n\n{e}")
            root.destroy()
        except:
            print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
