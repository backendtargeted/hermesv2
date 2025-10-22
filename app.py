from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import qrcode
import uuid
import os
from datetime import datetime
import sqlite3
from werkzeug.utils import secure_filename
from PIL import Image
from qrcode.image.pil import PilImage

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directories exist
UPLOAD_FOLDER = 'static/images/bags'
QR_FOLDER = 'static/images/qr'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# Database setup
def init_db():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/bags.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bags (
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
            authentication_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add authentication_date column to existing tables if it doesn't exist
    try:
        cursor.execute('ALTER TABLE bags ADD COLUMN authentication_date TEXT')
    except sqlite3.OperationalError:
        # Column already exists, ignore the error
        pass
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_web_copy(src_path, dest_path, max_dim=1200):
    """Create a compressed, resized JPEG copy for web display while preserving aspect ratio."""
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        im.save(dest_path, format="JPEG", quality=85, optimize=True, progressive=True)

@app.route('/')
def index():
    return render_template('admin_form.html')

@app.route('/submit', methods=['POST'])
def submit_bag():
    try:
        # Process form data
        reference_number = request.form['reference_number']
        recipient = request.form['recipient']
        model = request.form['model']
        year = request.form['year']
        additional_stamps = request.form.get('additional_stamps', '')
        opinion_text = request.form.get('opinion_text', '')
        authentication_date = request.form.get('authentication_date', '')
        
        # Generate UUID (31 characters)
        bag_uuid = str(uuid.uuid4()).replace('-', '')[:31]
        
        # Handle file uploads
        front_image = request.files['front_image']
        stamp_image = request.files['stamp_image']
        
        if front_image and stamp_image and allowed_file(front_image.filename) and allowed_file(stamp_image.filename):
            # Save images with UUID naming
            front_filename = f"{bag_uuid}_front.jpg"
            stamp_filename = f"{bag_uuid}_stamp.jpg"
            
            front_path = os.path.join(UPLOAD_FOLDER, front_filename)
            stamp_path = os.path.join(UPLOAD_FOLDER, stamp_filename)
            
            # Store relative paths for template use (without static/ prefix)
            front_relative_path = f"images/bags/{front_filename}"
            stamp_relative_path = f"images/bags/{stamp_filename}"
            
            front_image.save(front_path)
            stamp_image.save(stamp_path)

            # Generate web-sized copies for faster page loads
            front_web_path = os.path.join(UPLOAD_FOLDER, f"{bag_uuid}_front_web.jpg")
            stamp_web_path = os.path.join(UPLOAD_FOLDER, f"{bag_uuid}_stamp_web.jpg")
            make_web_copy(front_path, front_web_path)
            make_web_copy(stamp_path, stamp_web_path)
            
            # Generate QR code (transparent background, no white border)
            qr_url = f"{request.url_root}opinion-long-code/{bag_uuid}"
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            qr.add_data(qr_url)
            qr.make(fit=True)
            qr_img = qr.make_image(image_factory=PilImage, fill_color="black", back_color=(255, 255, 255, 0))
            qr_img = qr_img.convert("RGBA").resize((123, 123), Image.Resampling.NEAREST)
            qr_path = os.path.join(QR_FOLDER, f"{bag_uuid}_qr.png")
            qr_img.save(qr_path)
            
            # Save to database
            conn = sqlite3.connect('data/bags.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bags (uuid, reference_number, recipient, model, year, additional_stamps, opinion_text, front_image_path, stamp_image_path, authentication_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bag_uuid, reference_number, recipient, model, year, additional_stamps, opinion_text, front_relative_path, stamp_relative_path, authentication_date))
            conn.commit()
            conn.close()
            
            return redirect(url_for('view_opinion', uuid=bag_uuid))
        else:
            return "Invalid file format. Please upload valid image files.", 400
            
    except Exception as e:
        return f"Error processing request: {str(e)}", 500

@app.route('/opinion-long-code/<uuid>')
def view_opinion(uuid):
    conn = sqlite3.connect('data/bags.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bags WHERE uuid = ?', (uuid,))
    bag = cursor.fetchone()
    conn.close()
    
    if not bag:
        return "Bag not found", 404
    
    # Format authentication date to match example: "Wednesday, February 21, 2024"
    raw_auth_date = bag[11] if len(bag) > 11 and bag[11] else None
    display_date = None
    date_iso = None
    if raw_auth_date:
        try:
            # Parse the date from the form (YYYY-MM-DD format)
            parsed_dt = datetime.strptime(raw_auth_date, "%Y-%m-%d")
            display_date = f"{parsed_dt.strftime('%A')}, {parsed_dt.strftime('%B')} {parsed_dt.day}, {parsed_dt.year}"
            date_iso = parsed_dt.isoformat()
        except ValueError:
            # Fallback to created_at if authentication_date is invalid
            raw_created_at = bag[10] if len(bag) > 10 else None
            if raw_created_at:
                try:
                    parsed_dt = datetime.strptime(raw_created_at, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        parsed_dt = datetime.fromisoformat(raw_created_at)
                    except Exception:
                        parsed_dt = None
                if parsed_dt:
                    display_date = f"{parsed_dt.strftime('%A')}, {parsed_dt.strftime('%B')} {parsed_dt.day}, {parsed_dt.year}"
                    date_iso = parsed_dt.isoformat()
    
    return render_template('opinion_template.html', bag=bag, display_date=display_date, date_iso=date_iso)

@app.route('/admin')
def admin_list():
    conn = sqlite3.connect('data/bags.db')
    cursor = conn.cursor()
    cursor.execute('SELECT uuid, reference_number, recipient, model, created_at FROM bags ORDER BY created_at DESC')
    bags = cursor.fetchall()
    conn.close()
    
    return render_template('admin_list.html', bags=bags)

@app.route('/static/images/bags/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/static/images/qr/<filename>')
def qr_file(filename):
    return send_from_directory(QR_FOLDER, filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
