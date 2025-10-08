# Hermes - Flask Landing Page Application

A Flask application that serves a minified HTML page with preserved styling and provides a CRUD API for managing landing pages.

## Features

- **Preserved Styling**: Maintains exact Challenge Files styling and layout
- **API Routes**: All static files served through Flask API routes instead of static files
- **CRUD API**: Complete Create, Read, Update, Delete operations for landing pages
- **Docker Support**: Containerized application with Docker and Docker Compose
- **Database**: SQLite database for storing landing page data

## Data Model

Each landing page contains:
- **id**: Unique identifier (UUID)
- **processed**: Boolean flag indicating if the page has been processed
- **last_modified**: Timestamp of last modification
- **images**: JSON string containing array of image URLs/paths
- **main_image**: Main image URL/path

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Main page: http://localhost:5000
   - API documentation: See `API_DOCUMENTATION.md`

### Option 2: Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Main page: http://localhost:5000
   - API endpoints: http://localhost:5000/api/landing-pages

## API Endpoints

### Landing Pages CRUD API

- `GET /api/landing-pages` - Get all landing pages
- `GET /api/landing-pages/<id>` - Get specific landing page
- `POST /api/landing-pages` - Create new landing page
- `PUT /api/landing-pages/<id>` - Update landing page
- `DELETE /api/landing-pages/<id>` - Delete landing page

### Static File API Routes

- `GET /api/image/<filename>` - Serve images
- `GET /api/css/<filename>` - Serve CSS files
- `GET /api/js/<filename>` - Serve JavaScript files
- `GET /api/fonts/<filename>` - Serve font files
- `GET /api/files/<filename>` - Serve other files

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## Project Structure

```
hermes/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
├── .dockerignore                  # Docker ignore file
├── test_api.py                    # API test script
├── process_html.py                # HTML processing utility
├── templates/
│   └── index.html                 # Main HTML template
├── Challenge FIles/               # Original challenge files
│   ├── Verify.html               # Original HTML file
│   └── Verify_files/             # Static assets
└── API_DOCUMENTATION.md          # Detailed API documentation
```

## Development Notes

- The original HTML file has been processed to replace all static file references with API routes
- All styling, fonts, and layout are preserved exactly as in the Challenge Files
- The application uses SQLite for data persistence
- Database file is created automatically on first run

## Docker Commands

```bash
# Build the image
docker build -t hermes-app .

# Run the container
docker run -p 5000:5000 hermes-app

# Run with Docker Compose
docker-compose up --build

# Stop the application
docker-compose down
```

## API Examples

### Create a landing page:
```bash
curl -X POST http://localhost:5000/api/landing-pages \
  -H "Content-Type: application/json" \
  -d '{
    "processed": false,
    "images": "[\"/api/image/logo.png\"]",
    "main_image": "/api/image/logo.png"
  }'
```

### Get all landing pages:
```bash
curl -X GET http://localhost:5000/api/landing-pages
```

For more detailed API documentation, see `API_DOCUMENTATION.md`.
