#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    language: str
    dpi: int
    preserve_images: bool
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
            can.setFont(\"Helvetica\", 12)\n            can.setFillColorRGB(0, 0, 0, alpha=0)  # Transparent text\n            \n            # Extract text and positions from OCR data\n            for i in range(len(ocr_data['text'])):\n                text = ocr_data['text'][i].strip()\n                if text and int(ocr_data['conf'][i]) > 30:  # Confidence threshold\n                    x = ocr_data['left'][i]\n                    y = page_height - ocr_data['top'][i]  # Flip Y coordinate\n                    can.drawString(x, y, text)\n            \n            can.save()\n            \n            # Convert image to PDF if preserving images\n            if params[\"preserve_images\"]:\n                # Save original image as background\n                img_packet = io.BytesIO()\n                can_img = canvas.Canvas(img_packet, pagesize=(page_width, page_height))\n                \n                # Save image temporarily\n                temp_img_path = f\"temp_page_{page_num}.png\"\n                image.save(temp_img_path, \"PNG\")\n                can_img.drawImage(temp_img_path, 0, 0, page_width, page_height)\n                can_img.save()\n                \n                # Clean up temp image\n                os.remove(temp_img_path)\n                \n                # Merge text layer with image\n                img_packet.seek(0)\n                from PyPDF2 import PdfReader\n                img_pdf = PdfReader(img_packet)\n                packet.seek(0)\n                text_pdf = PdfReader(packet)\n                \n                if img_pdf.pages and text_pdf.pages:\n                    img_pdf.pages[0].merge_page(text_pdf.pages[0])\n                    writer.add_page(img_pdf.pages[0])\n                else:\n                    writer.add_page(text_pdf.pages[0])\n            else:\n                # Text-only PDF\n                packet.seek(0)\n                from PyPDF2 import PdfReader\n                text_pdf = PdfReader(packet)\n                if text_pdf.pages:\n                    writer.add_page(text_pdf.pages[0])\n            \n            pages_processed += 1\n        \n        # Write OCR'd PDF\n        with open(params[\"output_path\"], 'wb') as output_file:\n            writer.write(output_file)\n        \n        avg_confidence = total_confidence / pages_processed if pages_processed > 0 else 0\n        \n        return {\n            \"output_path\": params[\"output_path\"],\n            \"pages_processed\": pages_processed,\n            \"confidence_score\": round(avg_confidence, 2)\n        }\n        \n    except Exception as e:\n        raise Exception(f\"Error performing OCR on PDF: {str(e)}\")