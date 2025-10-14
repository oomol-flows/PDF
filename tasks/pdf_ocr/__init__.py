#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    language: typing.Literal["eng", "chi_sim", "chi_tra", "jpn", "kor", "fra", "deu", "spa", "rus"]
    dpi: float
    preserve_images: bool
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    pages_processed: typing.NotRequired[float]
    confidence_score: typing.NotRequired[float]
#endregion

from oocana import Context
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io
import os

def main(params: Inputs, context: Context) -> dict:
    """
    Perform OCR on scanned PDF to make it searchable
    
    Args:
        params: Input parameters containing PDF path and OCR settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and OCR statistics
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(
            params["pdf_path"],
            dpi=params["dpi"],
            fmt='RGB'
        )
        
        writer = PdfWriter()
        total_confidence = 0
        pages_processed = 0
        
        for page_num, image in enumerate(images):
            # Perform OCR on the image
            ocr_data = pytesseract.image_to_data(
                image, 
                lang=params["language"], 
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate confidence score
            confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
            page_confidence = sum(confidences) / len(confidences) if confidences else 0
            total_confidence += page_confidence
            
            # Create searchable PDF page
            page_width, page_height = image.size
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            
            # Add invisible text layer for searchability
            can.setFont("Helvetica", 12)
            can.setFillColorRGB(0, 0, 0, alpha=0)  # Transparent text
            
            # Extract text and positions from OCR data
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                if text and int(ocr_data['conf'][i]) > 30:  # Confidence threshold
                    x = ocr_data['left'][i]
                    y = page_height - ocr_data['top'][i]  # Flip Y coordinate
                    can.drawString(x, y, text)
            
            can.save()
            
            # Convert image to PDF if preserving images
            if params["preserve_images"]:
                # Save original image as background
                img_packet = io.BytesIO()
                can_img = canvas.Canvas(img_packet, pagesize=(page_width, page_height))
                
                # Save image temporarily
                temp_img_path = f"temp_page_{page_num}.png"
                image.save(temp_img_path, "PNG")
                can_img.drawImage(temp_img_path, 0, 0, page_width, page_height)
                can_img.save()
                
                # Clean up temp image
                os.remove(temp_img_path)
                
                # Merge text layer with image
                img_packet.seek(0)
                from PyPDF2 import PdfReader
                img_pdf = PdfReader(img_packet)
                packet.seek(0)
                text_pdf = PdfReader(packet)
                
                if img_pdf.pages and text_pdf.pages:
                    img_pdf.pages[0].merge_page(text_pdf.pages[0])
                    writer.add_page(img_pdf.pages[0])
                else:
                    writer.add_page(text_pdf.pages[0])
            else:
                # Text-only PDF
                packet.seek(0)
                from PyPDF2 import PdfReader
                text_pdf = PdfReader(packet)
                if text_pdf.pages:
                    writer.add_page(text_pdf.pages[0])
            
            pages_processed += 1
        
        # Write OCR'd PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        avg_confidence = total_confidence / pages_processed if pages_processed > 0 else 0
        
        return {
            "output_path": params["output_path"],
            "pages_processed": pages_processed,
            "confidence_score": round(avg_confidence, 2)
        }
        
    except Exception as e:
        raise Exception(f"Error performing OCR on PDF: {str(e)}")