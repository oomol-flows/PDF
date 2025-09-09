#!/usr/bin/env python3
"""
Create a test PDF file for compression testing
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import red, blue, green, black
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import os
import io

def create_test_pdf():
    """Create a test PDF with text and images for compression testing"""
    output_path = "/oomol-driver/oomol-storage/test_input.pdf"
    
    # Create a simple PDF with multiple pages and content
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Add title
    title = Paragraph("PDF Compression Test Document", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add some text content
    for i in range(5):
        text = f"""
        This is page {i+1} of the test document. This document contains various elements
        that can benefit from PDF compression including repeated text, metadata, and images.
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
        exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        """
        para = Paragraph(text, styles['Normal'])
        story.append(para)
        story.append(Spacer(1, 12))
    
    # Create a simple test image in memory
    img = PILImage.new('RGB', (200, 100), color=(73, 109, 137))
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    # Save the image temporarily
    temp_img_path = "/tmp/test_image.png"
    with open(temp_img_path, 'wb') as f:
        f.write(img_io.getvalue())
    
    # Add the image to PDF
    try:
        from reportlab.platypus import Image as ReportLabImage
        img_element = ReportLabImage(temp_img_path, width=2*inch, height=1*inch)
        story.append(img_element)
        story.append(Spacer(1, 12))
    except:
        pass
    
    # Build the PDF
    doc.build(story)
    
    # Clean up temp image
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)
    
    print(f"Test PDF created at: {output_path}")
    
    # Show file size
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"File size: {size} bytes")
    
    return output_path

if __name__ == "__main__":
    create_test_pdf()