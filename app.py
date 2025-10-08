from flask import Flask, render_template, send_file, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import base64
import uuid

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///landing_pages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Landing Page Model
class LandingPage(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    processed = db.Column(db.Boolean, default=False)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.Column(db.Text)  # JSON string of image URLs/paths
    main_image = db.Column(db.String(500))  # Main image URL/path
    
    def to_dict(self):
        return {
            'id': self.id,
            'processed': self.processed,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
            'images': self.images,
            'main_image': self.main_image
        }

@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@app.route('/api/image/<filename>')
def serve_image(filename):
    """Serve images via API route instead of static files"""
    try:
        # Map filename to actual file path
        image_path = os.path.join('Challenge FIles', 'Verify_files', filename)
        if os.path.exists(image_path):
            return send_file(image_path)
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/css/<filename>')
def serve_css(filename):
    """Serve CSS files via API route"""
    try:
        css_path = os.path.join('Challenge FIles', 'Verify_files', filename)
        if os.path.exists(css_path):
            return send_file(css_path, mimetype='text/css')
        else:
            return jsonify({'error': 'CSS file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/js/<filename>')
def serve_js(filename):
    """Serve JavaScript files via API route"""
    try:
        js_path = os.path.join('Challenge FIles', 'Verify_files', filename)
        if os.path.exists(js_path):
            return send_file(js_path, mimetype='application/javascript')
        else:
            return jsonify({'error': 'JavaScript file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fonts/<filename>')
def serve_fonts(filename):
    """Serve font files via API route"""
    try:
        font_path = os.path.join('Challenge FIles', 'Verify_files', filename)
        if os.path.exists(font_path):
            return send_file(font_path)
        else:
            return jsonify({'error': 'Font file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/<filename>')
def serve_files(filename):
    """Serve any other files via API route (fallback for files that don't fit other categories)"""
    try:
        file_path = os.path.join('Challenge FIles', 'Verify_files', filename)
        if os.path.exists(file_path):
            # Determine MIME type based on file extension
            if filename.endswith('.css'):
                return send_file(file_path, mimetype='text/css')
            elif filename.endswith('.js'):
                return send_file(file_path, mimetype='application/javascript')
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
                return send_file(file_path)
            elif filename.endswith(('.woff', '.woff2', '.ttf', '.eot')):
                return send_file(file_path)
            else:
                return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Landing Pages CRUD API

@app.route('/api/landing-pages', methods=['GET'])
def get_landing_pages():
    """Get all landing pages"""
    try:
        pages = LandingPage.query.all()
        return jsonify([page.to_dict() for page in pages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/landing-pages/<page_id>', methods=['GET'])
def get_landing_page(page_id):
    """Get a specific landing page by ID"""
    try:
        page = LandingPage.query.get_or_404(page_id)
        return jsonify(page.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/landing-pages', methods=['POST'])
def create_landing_page():
    """Create a new landing page"""
    try:
        data = request.get_json()
        
        # Create new landing page
        page = LandingPage(
            processed=data.get('processed', False),
            images=data.get('images', '[]'),  # Default to empty JSON array
            main_image=data.get('main_image', '')
        )
        
        db.session.add(page)
        db.session.commit()
        
        return jsonify(page.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/landing-pages/<page_id>', methods=['PUT'])
def update_landing_page(page_id):
    """Update a specific landing page"""
    try:
        page = LandingPage.query.get_or_404(page_id)
        data = request.get_json()
        
        # Update fields
        if 'processed' in data:
            page.processed = data['processed']
        if 'images' in data:
            page.images = data['images']
        if 'main_image' in data:
            page.main_image = data['main_image']
        
        page.last_modified = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(page.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/landing-pages/<page_id>', methods=['DELETE'])
def delete_landing_page(page_id):
    """Delete a specific landing page"""
    try:
        page = LandingPage.query.get_or_404(page_id)
        db.session.delete(page)
        db.session.commit()
        
        return jsonify({'message': 'Landing page deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
