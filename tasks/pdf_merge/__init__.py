#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_files: list[str]
    output_path: str
    preserve_bookmarks: bool
    add_page_numbers: bool
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    total_pages: typing.NotRequired[float]
    file_count: typing.NotRequired[float]
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

def main(params: Inputs, context: Context) -> dict:
    """
    Merge multiple PDF files into a single document
    
    Args:
        params: Input parameters containing PDF files and merge settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and merge statistics
    """
    try:
        if not params["pdf_files"]:
            raise ValueError("No PDF files provided for merging")
        
        # Initialize PDF writer
        writer = PdfWriter()
        total_pages = 0
        
        # Process each input PDF
        for file_index, pdf_path in enumerate(params["pdf_files"]):
            if not os.path.exists(pdf_path):
                continue
                
            reader = PdfReader(pdf_path)
            file_pages = len(reader.pages)
            
            # Add all pages from current PDF
            for page_index, page in enumerate(reader.pages):
                # Add page numbers if requested
                if params["add_page_numbers"]:
                    current_page_num = total_pages + page_index + 1
                    page = add_page_number(page, current_page_num)
                
                writer.add_page(page)
            
            # Preserve bookmarks if requested
            if params["preserve_bookmarks"] and reader.outline:
                try:
                    # Add bookmarks with offset
                    for bookmark in reader.outline:
                        if isinstance(bookmark, list):
                            # Handle nested bookmarks
                            for sub_bookmark in bookmark:
                                writer.add_outline_item(
                                    sub_bookmark.title, 
                                    total_pages + sub_bookmark.page.idnum
                                )
                        else:
                            writer.add_outline_item(
                                bookmark.title, 
                                total_pages + bookmark.page.idnum
                            )
                except Exception as e:
                    # Continue if bookmark processing fails
                    pass
            
            total_pages += file_pages
        
        # Write merged PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {
            "output_path": params["output_path"],
            "total_pages": total_pages,
            "file_count": len([f for f in params["pdf_files"] if os.path.exists(f)])
        }
        
    except Exception as e:
        raise Exception(f"Error merging PDFs: {str(e)}")

def add_page_number(page, page_num):
    """Add page number to a PDF page"""
    try:
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Create page number overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Draw page number at bottom center
        can.setFont("Helvetica", 10)
        can.drawCentredText(page_width / 2, 20, str(page_num))
        can.save()
        
        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        page_num_pdf = PdfReader(packet)
        
        # Merge page number with original page
        if page_num_pdf.pages:
            page.merge_page(page_num_pdf.pages[0])
        
        return page
    except:
        # Return original page if page numbering fails
        return page