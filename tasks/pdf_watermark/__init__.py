#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    watermark_text: typing.Optional[str]
    watermark_image: typing.Optional[str]
    output_path: str
    position_x: float
    position_y: float
    opacity: float
    font_size: int
    rotation: float
    color: str
#endregion

from oocana import Context
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import os

def main(params: Inputs, context: Context) -> dict:
    """
    Add watermark to PDF file
    
    Args:
        params: Input parameters containing PDF path, watermark settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path
    """
    try:
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        
        # Process each page
        for page_num, page in enumerate(reader.pages):
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            # Create watermark overlay
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            
            # Calculate position
            x_pos = params["position_x"] * page_width
            y_pos = params["position_y"] * page_height
            
            # Set transparency
            can.setFillAlpha(params["opacity"])
            
            if params.get("watermark_text") and params["watermark_text"].strip():
                # Text watermark
                can.setFillColor(HexColor(params["color"]))
                can.setFont("Helvetica", params["font_size"])
                
                # Rotate and draw text
                can.translate(x_pos, y_pos)
                can.rotate(params["rotation"])
                can.drawCentredText(0, 0, params["watermark_text"])
                
            elif params.get("watermark_image") and os.path.exists(params["watermark_image"]):
                # Image watermark
                img = Image.open(params["watermark_image"])
                img_width, img_height = img.size
                
                # Scale image to reasonable size
                max_size = min(page_width, page_height) * 0.3
                if img_width > max_size or img_height > max_size:
                    ratio = min(max_size / img_width, max_size / img_height)
                    new_width = int(img_width * ratio)
                    new_height = int(img_height * ratio)
                else:
                    new_width, new_height = img_width, img_height
                
                # Draw image with rotation
                can.translate(x_pos, y_pos)
                can.rotate(params["rotation"])
                can.drawImage(
                    ImageReader(params["watermark_image"]), 
                    -new_width/2, -new_height/2, 
                    new_width, new_height
                )
            
            can.save()
            
            # Move to the beginning of the BytesIO buffer
            packet.seek(0)
            watermark_pdf = PdfReader(packet)
            
            # Merge watermark with original page
            if watermark_pdf.pages:
                page.merge_page(watermark_pdf.pages[0])
            
            writer.add_page(page)
        
        # Write output PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {"output_path": params["output_path"]}
        
    except Exception as e:
        raise Exception(f"Error adding watermark to PDF: {str(e)}")