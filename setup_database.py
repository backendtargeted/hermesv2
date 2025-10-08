#!/usr/bin/env python3
"""
Database setup script
Usage: python setup_database.py [DATABASE_URL]
"""

import sys
import os
from database_config import create_tables, test_database_operations

def main():
    """Main setup function"""
    
    # Get database URL from command line argument or environment variable
    if len(sys.argv) > 1:
        database_url = sys.argv[1]
    else:
        database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ No database URL provided!")
        print("Usage: python setup_database.py [DATABASE_URL]")
        print("Or set DATABASE_URL environment variable")
        print("\nExamples:")
        print("  python setup_database.py 'postgresql://user:pass@localhost/dbname'")
        print("  python setup_database.py 'mysql://user:pass@localhost/dbname'")
        print("  python setup_database.py 'sqlite:///landing_pages.db'")
        return False
    
    print(f"🔗 Database URL: {database_url}")
    print("\n📊 Creating database tables...")
    
    if create_tables(database_url):
        print("\n🧪 Testing database operations...")
        if test_database_operations(database_url):
            print("\n🎉 Database setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Set the DATABASE_URL environment variable:")
            print(f"   set DATABASE_URL={database_url}")
            print("2. Run the Flask application:")
            print("   python app.py")
            return True
        else:
            print("\n❌ Database operations test failed!")
            return False
    else:
        print("\n❌ Database table creation failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
