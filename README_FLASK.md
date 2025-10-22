# Bababebi Dynamic Flask App

A dynamic Flask application that generates landing pages for Hermès handbag authentication certificates. This app transforms the static template into a dynamic system where users can submit bag information via a form and generate unique opinion pages with QR codes.

## Features

- **Dynamic Opinion Pages**: Generate unique landing pages for each verified bag
- **QR Code Generation**: Automatic QR code creation linking to `/opinion/{31-char-uuid}`
- **Image Upload**: Upload front and stamp photos for each bag
- **Admin Interface**: Simple form-based interface to add new bags
- **Database Storage**: SQLite database to store all bag information
- **Preserved Layout**: Maintains exact original styling and functionality

## Project Structure

```
hermes/
├── app.py                          # Flask application
├── bags.db                         # SQLite database (auto-created)
├── requirements.txt                # Python dependencies
├── templates/
│   ├── admin_form.html            # Form to add new bags
│   ├── opinion_template.html      # Dynamic opinion template
│   └── admin_list.html            # List all bags
├── static/
│   ├── css/
│   │   └── styles.css             # Original styles (unchanged)
│   ├── js/
│   │   ├── jquery.min.js          # Original JS files
│   │   └── custom.js              # Original custom JS
│   └── images/
│       ├── logo_con_letras_0.png  # Static images
│       ├── logo_con_letras_footer_opinions.png
│       ├── fb-art.png
│       ├── instagram-art.png
│       ├── bababebi_fondo.jpg
│       ├── bags/                  # Uploaded bag images
│       │   ├── {uuid}_front.jpg
│       │   └── {uuid}_stamp.jpg
│       └── qr/                    # Generated QR codes
│           └── {uuid}_qr.png
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hermes
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Admin form: http://localhost:5000/
   - Admin list: http://localhost:5000/admin
   - Opinion pages: http://localhost:5000/opinion/{uuid}

## Usage

### Adding a New Bag

1. Navigate to http://localhost:5000/
2. Fill out the form with:
   - Reference Number (required)
   - Recipient (required)
   - Model (required)
   - Year of Manufacture (required)
   - Additional Stamps (optional)
   - Opinion Text (optional - uses default if empty)
   - Front Image (required)
   - Stamp Image (required)
3. Click "Create Opinion"
4. You'll be redirected to the generated opinion page

### Viewing All Bags

- Navigate to http://localhost:5000/admin to see all created bags
- Click "View Opinion" to see any bag's opinion page

### QR Code Functionality

- Each bag gets a unique 31-character UUID
- QR codes are automatically generated linking to `/opinion/{uuid}`
- QR codes are saved as PNG files in `static/images/qr/`

## API Endpoints

- `GET /` - Admin form to add new bags
- `POST /submit` - Process form submission and create new bag
- `GET /opinion/<uuid>` - Display opinion page for specific bag
- `GET /admin` - List all bags
- `GET /static/images/bags/<filename>` - Serve uploaded bag images
- `GET /static/images/qr/<filename>` - Serve generated QR codes

## Database Schema

The SQLite database (`bags.db`) contains a single table:

```sql
CREATE TABLE bags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    reference_number TEXT NOT NULL,
    recipient TEXT NOT NULL,
    model TEXT NOT NULL,
    year TEXT NOT NULL,
    additional_stamps TEXT,
    opinion_text TEXT,
    front_image_path TEXT,
    stamp_image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Key Features Implemented

### Dynamic Content Replacement
- **Reference #**: Dynamic from form input
- **Date**: Current timestamp when bag is created
- **Recipient**: Dynamic from form input
- **Model**: Dynamic from form input
- **Year**: Dynamic from form input
- **Additional Stamps**: Dynamic from form input
- **Opinion Text**: Dynamic from form input (with default)
- **QR Code**: Generated with unique UUID-based URL
- **Images**: Uploaded and stored with UUID naming

### Preserved Functionality
- **Exact Layout**: Maintains original styling and structure
- **Image Lightbox**: Original JavaScript functionality preserved
- **Responsive Design**: Original CSS responsive behavior maintained
- **Social Links**: Facebook and Instagram links preserved
- **Disclaimer Text**: Original legal disclaimer maintained

## File Upload Handling

- **Supported Formats**: PNG, JPG, JPEG, GIF
- **File Size Limit**: 16MB per file
- **Storage**: Files saved with UUID naming convention
- **Security**: Filename sanitization and validation

## QR Code Generation

- **Library**: qrcode[pil] for Python
- **Format**: PNG images
- **Size**: 10x10 box size with 5px border
- **Content**: Full URL to opinion page
- **Naming**: `{uuid}_qr.png`

## Development Notes

- **Database**: SQLite for simplicity (no external dependencies)
- **File Storage**: Local filesystem storage
- **No Authentication**: As requested, no auth system implemented
- **Error Handling**: Basic error handling for file uploads and database operations
- **Debug Mode**: Enabled for development

## Production Considerations

For production deployment, consider:
- Adding authentication/authorization
- Using a production WSGI server (Gunicorn, uWSGI)
- Implementing proper error handling and logging
- Using a production database (PostgreSQL, MySQL)
- Adding file upload validation and virus scanning
- Implementing rate limiting and security headers

## License

This project is created for educational purposes. The original content belongs to bababebi.com.
