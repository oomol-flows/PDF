#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    compression_level: typing.Literal["low", "medium", "high", "maximum"]
    image_quality: float
    remove_duplicates: bool
class Outputs(typing.TypedDict):
    output_path: str
    original_size: float
    compressed_size: float
    compression_ratio: float
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import os

def main(params: Inputs, context: Context) -> dict:
    """
    Compress PDF file to reduce file size
    
    Args:
        params: Input parameters containing PDF path and compression settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and compression statistics
    """
    try:
        # Get original file size
        original_size = os.path.getsize(params["pdf_path"])
        
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        
        # Set compression options based on level
        compression_settings = {
            "low": {"remove_links": False, "remove_images": False, "compress_streams": True},
            "medium": {"remove_links": True, "remove_images": False, "compress_streams": True},
            "high": {"remove_links": True, "remove_images": False, "compress_streams": True},
            "maximum": {"remove_links": True, "remove_images": False, "compress_streams": True}
        }
        
        settings = compression_settings[params["compression_level"]]
        
        # Process each page
        for page in reader.pages:
            # Remove links if specified
            if settings["remove_links"]:
                if "/Annots" in page:
                    del page["/Annots"]
            
            # Compress page content streams
            if settings["compress_streams"]:
                page.compress_content_streams()
            
            writer.add_page(page)
        
        # Apply compression settings
        if params["remove_duplicates"]:
            writer.remove_duplicates()
        
        # Compress images based on quality setting
        if params["compression_level"] in ["high", "maximum"]:
            # Note: Advanced image compression would require additional processing
            # This is a basic implementation
            pass
        
        # Write compressed PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        # Calculate compression statistics
        compressed_size = os.path.getsize(params["output_path"])
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        return {
            "output_path": params["output_path"],
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2)
        }
        
    except Exception as e:
        raise Exception(f"Error compressing PDF: {str(e)}")