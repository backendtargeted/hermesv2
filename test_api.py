#!/usr/bin/env python3
"""
Simple test script to verify the Landing Pages CRUD API
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    """Test all CRUD operations"""
    print("Testing Landing Pages CRUD API...")
    
    # Test 1: Create a new landing page
    print("\n1. Creating a new landing page...")
    create_data = {
        "processed": False,
        "images": '["/api/image/logo.png", "/api/image/banner.jpg"]',
        "main_image": "/api/image/logo.png"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/landing-pages", json=create_data)
        if response.status_code == 201:
            page_data = response.json()
            page_id = page_data['id']
            print(f"✅ Created landing page with ID: {page_id}")
        else:
            print(f"❌ Failed to create landing page: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on localhost:5000")
        return
    
    # Test 2: Get all landing pages
    print("\n2. Getting all landing pages...")
    try:
        response = requests.get(f"{BASE_URL}/api/landing-pages")
        if response.status_code == 200:
            pages = response.json()
            print(f"✅ Retrieved {len(pages)} landing page(s)")
        else:
            print(f"❌ Failed to get landing pages: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting landing pages: {e}")
    
    # Test 3: Get specific landing page
    print(f"\n3. Getting landing page {page_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/landing-pages/{page_id}")
        if response.status_code == 200:
            page = response.json()
            print(f"✅ Retrieved landing page: {page['id']}")
        else:
            print(f"❌ Failed to get landing page: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting landing page: {e}")
    
    # Test 4: Update landing page
    print(f"\n4. Updating landing page {page_id}...")
    update_data = {
        "processed": True,
        "main_image": "/api/image/new-banner.jpg"
    }
    try:
        response = requests.put(f"{BASE_URL}/api/landing-pages/{page_id}", json=update_data)
        if response.status_code == 200:
            updated_page = response.json()
            print(f"✅ Updated landing page. Processed: {updated_page['processed']}")
        else:
            print(f"❌ Failed to update landing page: {response.status_code}")
    except Exception as e:
        print(f"❌ Error updating landing page: {e}")
    
    # Test 5: Delete landing page
    print(f"\n5. Deleting landing page {page_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/api/landing-pages/{page_id}")
        if response.status_code == 200:
            print("✅ Successfully deleted landing page")
        else:
            print(f"❌ Failed to delete landing page: {response.status_code}")
    except Exception as e:
        print(f"❌ Error deleting landing page: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api()
