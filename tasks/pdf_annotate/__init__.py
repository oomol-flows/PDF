#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    annotation_type: str
    page_number: int
    x_position: float
    y_position: float
    annotation_text: str
    color: str
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

def main(params: Inputs, context: Context) -> dict:
    """
    Add annotations to PDF file
    
    Args:
        params: Input parameters containing PDF path and annotation settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path
    """
    try:
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        target_page = params["page_number"] - 1  # Convert to 0-based index
        
        if target_page < 0 or target_page >= total_pages:
            raise ValueError(f"Page {params['page_number']} does not exist in PDF")
        
        # Process each page
        for page_index, page in enumerate(reader.pages):
            if page_index == target_page:
                # Add annotation to target page
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Create annotation overlay
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                
                # Calculate position
                x_pos = params["x_position"] * page_width
                y_pos = params["y_position"] * page_height
                
                # Set color
                try:
                    color = HexColor(params["color"])
                    can.setFillColor(color)
                    can.setStrokeColor(color)
                except:
                    # Default to yellow if color parsing fails
                    can.setFillColor(HexColor("#FFFF00"))
                    can.setStrokeColor(HexColor("#FFFF00"))
                
                if params["annotation_type"] == "text":
                    # Text annotation
                    can.setFont("Helvetica", 12)
                    can.drawString(x_pos, y_pos, params["annotation_text"])
                    
                elif params["annotation_type"] == "highlight":
                    # Highlight annotation (rectangle)
                    text_width = len(params["annotation_text"]) * 7  # Approximate width
                    can.setFillAlpha(0.3)  # Semi-transparent
                    can.rect(x_pos, y_pos - 2, text_width, 14, fill=1, stroke=0)
                    can.setFillAlpha(1.0)  # Reset transparency
                    can.setFillColor(HexColor("#000000"))  # Black text
                    can.drawString(x_pos, y_pos, params["annotation_text"])
                    
                elif params["annotation_type"] == "note":
                    # Note annotation (circle with text)
                    can.circle(x_pos, y_pos, 8, fill=1)
                    can.setFillColor(HexColor("#000000"))  # Black text
                    can.setFont("Helvetica", 8)
                    can.drawString(x_pos + 15, y_pos - 3, params["annotation_text"])
                    
                elif params["annotation_type"] == "stamp":
                    # Stamp annotation (bordered rectangle with text)
                    text_width = len(params["annotation_text"]) * 8
                    text_height = 20
                    can.rect(x_pos, y_pos, text_width, text_height, fill=0, stroke=1)
                    can.setFillColor(HexColor("#000000"))  # Black text
                    can.setFont("Helvetica-Bold", 10)
                    can.drawString(x_pos + 5, y_pos + 5, params["annotation_text"])
                
                can.save()
                
                # Merge annotation with original page
                packet.seek(0)
                annotation_pdf = PdfReader(packet)
                if annotation_pdf.pages:
                    page.merge_page(annotation_pdf.pages[0])
            
            writer.add_page(page)
        
        # Write annotated PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {"output_path": params["output_path"]}
        
    except Exception as e:
        raise Exception(f"Error adding annotation to PDF: {str(e)}")