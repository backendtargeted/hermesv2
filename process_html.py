#!/usr/bin/env python3
"""
Script to process the HTML file and update all static file references to use Flask API routes
"""

import re
import os

def process_html_file(input_file, output_file):
    """Process HTML file and update static file references to API routes"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update CSS file references
    content = re.sub(r'href="\./Verify_files/([^"]+)"', r'href="/api/css/\1"', content)
    
    # Update JavaScript file references
    content = re.sub(r'src="\./Verify_files/([^"]+\.js\.download)"', r'src="/api/js/\1"', content)
    
    # Update image file references
    content = re.sub(r'src="\./Verify_files/([^"]+\.png)"', r'src="/api/image/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.jpg)"', r'src="/api/image/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.jpeg)"', r'src="/api/image/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.gif)"', r'src="/api/image/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.svg)"', r'src="/api/image/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.ico)"', r'src="/api/image/\1"', content)
    
    # Update font file references
    content = re.sub(r'src="\./Verify_files/([^"]+\.woff2?)"', r'src="/api/fonts/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.ttf)"', r'src="/api/fonts/\1"', content)
    content = re.sub(r'src="\./Verify_files/([^"]+\.eot)"', r'src="/api/fonts/\1"', content)
    
    # Update any remaining Verify_files references that don't have specific extensions
    # This catches files like saved_resource, icon, etc.
    content = re.sub(r'\./Verify_files/([^"]+)"', r'/api/files/\1"', content)
    
    # Write the processed content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed HTML file: {input_file} -> {output_file}")

if __name__ == "__main__":
    input_file = "Challenge FIles/Verify.html"
    output_file = "templates/index.html"
    
    if os.path.exists(input_file):
        process_html_file(input_file, output_file)
        print("HTML processing completed successfully!")
    else:
        print(f"Input file not found: {input_file}")
