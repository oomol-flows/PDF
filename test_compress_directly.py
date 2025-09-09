#!/usr/bin/env python3
"""
Direct test of PDF compression task
"""
import sys
import os

# Add the tasks directory to Python path
sys.path.insert(0, '/app/workspace/tasks/pdf_compress')

from __init__ import main, Inputs
from oocana import Context

def test_compression():
    """Test the PDF compression functionality directly"""
    
    # Mock context object
    class MockContext:
        def __init__(self):
            pass
    
    # Test parameters
    params: Inputs = {
        "input_pdf": "/oomol-driver/oomol-storage/test_input.pdf",
        "output_path": "/oomol-driver/oomol-storage/compressed_output.pdf", 
        "compression_level": 7,
        "optimize_images": True,
        "remove_metadata": True
    }
    
    context = MockContext()
    
    try:
        print("Testing PDF compression...")
        print(f"Input file: {params['input_pdf']}")
        
        # Check if input file exists
        if not os.path.exists(params["input_pdf"]):
            print(f"Error: Input file does not exist: {params['input_pdf']}")
            return
        
        # Get original file size
        original_size = os.path.getsize(params["input_pdf"])
        print(f"Original size: {original_size} bytes")
        
        # Run compression
        result = main(params, context)
        
        print("Compression completed successfully!")
        print(f"Results: {result}")
        
        # Verify output file exists
        if os.path.exists(result["output_path"]):
            actual_size = os.path.getsize(result["output_path"])
            print(f"Output file created: {result['output_path']}")
            print(f"Actual compressed size: {actual_size} bytes")
        else:
            print("Warning: Output file was not created")
            
    except Exception as e:
        print(f"Error during compression: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_compression()