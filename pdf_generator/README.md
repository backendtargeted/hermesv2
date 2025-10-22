# PDF Generator for Opinion Pages

A standalone Flask application that converts opinion pages from your Hermes app into PDF documents.

## Features

- Convert any opinion page URL to PDF
- Custom filename support
- Beautiful web interface
- List and download previously generated PDFs
- Automatic PDF formatting optimized for printing

## Installation

1. **Install Python dependencies:**
   ```bash
   cd pdf_generator
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the web interface:**
   Open your browser and go to: `http://localhost:5001`

## Usage

1. **Enter the opinion page URL** in the form
2. **Optionally specify a custom filename** for the PDF
3. **Click "Generate PDF"** to create the PDF
4. **Download the PDF** automatically or from the recent PDFs list

## Example URLs

You can use URLs like:
- `https://leon-data-hermes-app.el1i26.easypanel.host/opinion-long-code/2482c10f37244c68925380a8cee4c08`
- `https://leon-data-hermes-app.el1i26.easypanel.host/opinion-long-code/0459f0cb1af641648cea3f01093f8b2`

## Generated Files

- PDFs are saved in the `generated_pdfs/` directory
- Files are automatically named with timestamps if no custom name is provided
- You can download PDFs directly from the web interface

## Requirements

- Python 3.7+
- Internet connection (to fetch opinion pages)
- WeasyPrint (for PDF generation)
- Flask (web framework)

## Troubleshooting

- **"Error fetching URL"**: Check that the URL is accessible and correct
- **"Error generating PDF"**: Ensure WeasyPrint is properly installed
- **Permission errors**: Make sure the `generated_pdfs` directory is writable

## Notes

- The application runs on port 5001 to avoid conflicts with your main app
- PDFs are optimized for A4 paper size
- Interactive elements are hidden in the PDF output
- Images are automatically resized to fit the page
