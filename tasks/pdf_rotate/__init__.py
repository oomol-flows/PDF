#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    rotation_angle: int
    page_range: str
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter
import re

def main(params: Inputs, context: Context) -> dict:
    """
    Rotate PDF pages by specified angle
    
    Args:
        params: Input parameters containing PDF path and rotation settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and rotation statistics
    """
    try:
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        if total_pages == 0:
            raise ValueError("PDF has no pages")
        
        # Parse page range
        if params["page_range"].strip().lower() == "all":
            pages_to_rotate = set(range(total_pages))
        else:
            pages_to_rotate = parse_page_range(params["page_range"], total_pages)
        
        pages_rotated = 0
        
        # Process each page
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            
            # Rotate if this page is in the range
            if page_num in pages_to_rotate:
                page.rotate(params["rotation_angle"])
                pages_rotated += 1
            
            writer.add_page(page)
        
        # Write rotated PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {
            "output_path": params["output_path"],
            "pages_rotated": pages_rotated
        }
        
    except Exception as e:
        raise Exception(f"Error rotating PDF: {str(e)}")

def parse_page_range(range_str, total_pages):
    """Parse page range string like \"1-3,5,7-9\" into set of page indices (0-based)"""
    pages = set()
    
    for part in range_str.split(','):
        part = part.strip()
        
        if '-' in part:
            # Range like "1-3"
            start, end = part.split('-', 1)
            start = max(1, int(start.strip()))
            end = min(total_pages, int(end.strip()))
            
            for page_num in range(start, end + 1):
                pages.add(page_num - 1)  # Convert to 0-based index
        else:
            # Single page like "5"
            page_num = int(part.strip())
            if 1 <= page_num <= total_pages:
                pages.add(page_num - 1)  # Convert to 0-based index
    
    return pages