#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    pages_to_delete: str
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    pages_deleted: typing.NotRequired[float]
    remaining_pages: typing.NotRequired[float]
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter

def main(params: Inputs, context: Context) -> dict:
    """
    Delete specific pages from PDF file
    
    Args:
        params: Input parameters containing PDF path and pages to delete
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and deletion statistics
    """
    try:
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        # Parse pages to delete
        pages_to_delete = parse_page_list(params["pages_to_delete"], total_pages)
        
        pages_kept = 0
        # Add pages that are not in delete list
        for page_num in range(total_pages):
            if page_num not in pages_to_delete:
                writer.add_page(reader.pages[page_num])
                pages_kept += 1
        
        # Write output PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {
            "output_path": params["output_path"],
            "pages_deleted": len(pages_to_delete),
            "remaining_pages": pages_kept
        }
        
    except Exception as e:
        raise Exception(f"Error deleting pages from PDF: {str(e)}")

def parse_page_list(pages_str, total_pages):
    """Parse page list string like \"1,3,5-7\" into set of page indices (0-based)"""
    pages = set()
    
    for part in pages_str.split(','):
        part = part.strip()
        
        if '-' in part:
            start, end = part.split('-', 1)
            start = max(1, int(start.strip()))
            end = min(total_pages, int(end.strip()))
            
            for page_num in range(start, end + 1):
                pages.add(page_num - 1)
        else:
            page_num = int(part.strip())
            if 1 <= page_num <= total_pages:
                pages.add(page_num - 1)
    
    return pages