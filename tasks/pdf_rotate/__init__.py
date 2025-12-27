#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str | None
    rotation_angle: typing.Literal["90", "180", "270"]
    page_range: str | None
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    pages_rotated: typing.NotRequired[float]
#endregion

from oocana import Context
from pypdf import PdfReader, PdfWriter
import os

def string_to_number(value: str) -> float:
    """
    Convert string to number (int or float)
    
    Args:
        value: String representation of a number
        
    Returns:
        Numeric value as float
        
    Raises:
        ValueError: If string cannot be converted to number
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    
    value = value.strip()
    if not value:
        raise ValueError("Empty string cannot be converted to number")
    
    try:
        # Try integer first
        if '.' not in value and 'e' not in value.lower():
            return float(int(value))
        else:
            # Handle float
            return float(value)
    except ValueError as e:
        raise ValueError(f"Cannot convert '{value}' to number: {str(e)}")

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
        # Apply default values for nullable parameters
        page_range = params.get("page_range") or "all"

        # Set default output path if not provided
        if not params.get("output_path"):
            input_filename = os.path.basename(params["pdf_path"])
            name, ext = os.path.splitext(input_filename)
            output_path = os.path.join(context.session_dir, f"{name}_rotated{ext}")
        else:
            output_path = params["output_path"]

        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        total_pages = len(reader.pages)

        if total_pages == 0:
            raise ValueError("PDF has no pages")

        # Parse page range
        if page_range.strip().lower() == "all":
            pages_to_rotate = set(range(total_pages))
        else:
            pages_to_rotate = parse_page_range(page_range, total_pages)
        
        pages_rotated = 0
        
        # Process each page
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            
            # Rotate if this page is in the range
            if page_num in pages_to_rotate:
                rotation_degrees = int(string_to_number(params["rotation_angle"]))
                page.rotate(rotation_degrees)
                pages_rotated += 1
            
            writer.add_page(page)
        
        # Write rotated PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {
            "output_path": output_path,
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
            start = max(1, int(string_to_number(start.strip())))
            end = min(total_pages, int(string_to_number(end.strip())))
            
            for page_num in range(start, end + 1):
                pages.add(page_num - 1)  # Convert to 0-based index
        else:
            # Single page like "5"
            page_num = int(string_to_number(part.strip()))
            if 1 <= page_num <= total_pages:
                pages.add(page_num - 1)  # Convert to 0-based index
    
    return pages