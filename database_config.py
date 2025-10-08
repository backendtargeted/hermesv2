#!/usr/bin/env python3
"""
Database configuration and table creation script
Supports SQLite, PostgreSQL, MySQL, and other databases
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

def create_app_with_db(database_url=None):
    """Create Flask app with database configuration"""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Database configuration
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Default to SQLite if no URL provided
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
    
    return app, db, LandingPage

def create_tables(database_url=None):
    """Create database tables"""
    app, db, LandingPage = create_app_with_db(database_url)
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Available tables: {tables}")
            
            # Test database connection
            result = db.session.execute(db.text("SELECT 1"))
            print("✅ Database connection successful!")
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    return True

def test_database_operations(database_url=None):
    """Test basic database operations"""
    app, db, LandingPage = create_app_with_db(database_url)
    
    with app.app_context():
        try:
            # Test creating a landing page
            test_page = LandingPage(
                processed=False,
                images='["/api/image/test.png"]',
                main_image="/api/image/test.png"
            )
            
            db.session.add(test_page)
            db.session.commit()
            
            # Test retrieving the page
            retrieved_page = LandingPage.query.first()
            print(f"✅ Test page created and retrieved: {retrieved_page.id}")
            
            # Clean up test data
            db.session.delete(retrieved_page)
            db.session.commit()
            print("✅ Test data cleaned up")
            
        except Exception as e:
            print(f"❌ Error testing database operations: {e}")
            return False
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
        print(f"🔗 Using database URL: {database_url}")
    else:
        database_url = None
        print("🔗 Using default SQLite database")
    
    print("\n📊 Creating database tables...")
    if create_tables(database_url):
        print("\n🧪 Testing database operations...")
        if test_database_operations(database_url):
            print("\n🎉 Database setup completed successfully!")
        else:
            print("\n❌ Database operations test failed!")
    else:
        print("\n❌ Database table creation failed!")
