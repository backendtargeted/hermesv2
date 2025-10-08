# Landing Pages CRUD API Documentation

This Flask application provides a CRUD API for managing landing pages with the following data structure:

## Data Model

- **id**: String (UUID) - Primary key
- **processed**: Boolean - Whether the landing page has been processed
- **last_modified**: DateTime - When the page was last updated
- **images**: String (JSON) - Array of image URLs/paths
- **main_image**: String - Main image URL/path

## API Endpoints

### 1. Get All Landing Pages
```
GET /api/landing-pages
```
Returns a list of all landing pages.

**Response:**
```json
[
  {
    "id": "uuid-string",
    "processed": false,
    "last_modified": "2025-10-07T23:30:00.000Z",
    "images": "[]",
    "main_image": ""
  }
]
```

### 2. Get Single Landing Page
```
GET /api/landing-pages/<page_id>
```
Returns a specific landing page by ID.

**Response:**
```json
{
  "id": "uuid-string",
  "processed": true,
  "last_modified": "2025-10-07T23:30:00.000Z",
  "images": "[\"/api/image/logo.png\", \"/api/image/banner.jpg\"]",
  "main_image": "/api/image/logo.png"
}
```

### 3. Create Landing Page
```
POST /api/landing-pages
Content-Type: application/json
```

**Request Body:**
```json
{
  "processed": false,
  "images": "[\"/api/image/logo.png\"]",
  "main_image": "/api/image/logo.png"
}
```

**Response:** 201 Created
```json
{
  "id": "generated-uuid",
  "processed": false,
  "last_modified": "2025-10-07T23:30:00.000Z",
  "images": "[\"/api/image/logo.png\"]",
  "main_image": "/api/image/logo.png"
}
```

### 4. Update Landing Page
```
PUT /api/landing-pages/<page_id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "processed": true,
  "images": "[\"/api/image/logo.png\", \"/api/image/banner.jpg\"]",
  "main_image": "/api/image/banner.jpg"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "processed": true,
  "last_modified": "2025-10-07T23:35:00.000Z",
  "images": "[\"/api/image/logo.png\", \"/api/image/banner.jpg\"]",
  "main_image": "/api/image/banner.jpg"
}
```

### 5. Delete Landing Page
```
DELETE /api/landing-pages/<page_id>
```

**Response:**
```json
{
  "message": "Landing page deleted successfully"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```

## Example Usage with curl

### Create a new landing page:
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

### Update a landing page:
```bash
curl -X PUT http://localhost:5000/api/landing-pages/<page_id> \
  -H "Content-Type: application/json" \
  -d '{
    "processed": true,
    "main_image": "/api/image/new-banner.jpg"
  }'
```

### Delete a landing page:
```bash
curl -X DELETE http://localhost:5000/api/landing-pages/<page_id>
```
