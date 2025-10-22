from flask import Flask, render_template, request, send_file, jsonify
import requests
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os
import tempfile
from datetime import datetime
import uuid

app = Flask(__name__)

# Create output directory
OUTPUT_DIR = 'generated_pdfs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pdf_from_url(url, filename=None):
    """Generate PDF from a given URL"""
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Get HTML content
        html_content = response.text
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"opinion_{timestamp}.pdf"
        
        # Ensure filename has .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Create PDF
        html_doc = HTML(string=html_content, base_url=url)
        
        # Custom CSS for better PDF formatting
        css_content = """
        @page {
            size: A4;
            margin: 1cm;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.4;
            color: #333;
        }
        
        .container {
            max-width: 100%;
        }
        
        img {
            max-width: 100%;
            height: auto;
        }
        
        /* Hide any interactive elements */
        button, input, select, textarea {
            display: none !important;
        }
        
        /* Ensure proper spacing */
        .mb-4 {
            margin-bottom: 1rem;
        }
        
        .mt-4 {
            margin-top: 1rem;
        }
        """
        
        css_doc = CSS(string=css_content)
        
        # Generate PDF
        pdf_path = os.path.join(OUTPUT_DIR, filename)
        html_doc.write_pdf(pdf_path, stylesheets=[css_doc])
        
        return pdf_path, None
        
    except requests.RequestException as e:
        return None, f"Error fetching URL: {str(e)}"
    except Exception as e:
        return None, f"Error generating PDF: {str(e)}"

@app.route('/')
def index():
    return render_template('pdf_generator.html')

@app.route('/generate', methods=['POST'])
def generate_pdf():
    try:
        url = request.form.get('url', '').strip()
        filename = request.form.get('filename', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL format
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'error': 'Please provide a valid URL starting with http:// or https://'}), 400
        
        # Generate PDF
        pdf_path, error = generate_pdf_from_url(url, filename)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Return success response with download link
        filename = os.path.basename(pdf_path)
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/download/{filename}',
            'message': f'PDF generated successfully: {filename}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_pdf(filename):
    """Download the generated PDF"""
    try:
        pdf_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(pdf_path):
            return "File not found", 404
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

@app.route('/list')
def list_pdfs():
    """List all generated PDFs"""
    try:
        pdf_files = []
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith('.pdf'):
                file_path = os.path.join(OUTPUT_DIR, filename)
                file_stats = os.stat(file_path)
                pdf_files.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'created': datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    'download_url': f'/download/{filename}'
                })
        
        # Sort by creation time (newest first)
        pdf_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({'pdfs': pdf_files})
        
    except Exception as e:
        return jsonify({'error': f'Error listing files: {str(e)}'}), 500

if __name__ == '__main__':
    print("PDF Generator starting...")
    print("Access the application at: http://localhost:5001")
    print("Generated PDFs will be saved in the 'generated_pdfs' directory")
    app.run(debug=True, host='0.0.0.0', port=5001)
