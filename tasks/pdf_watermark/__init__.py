#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    watermark_text: str | None
    watermark_image: str | None
    output_path: str | None
    position_x: float | None
    position_y: float | None
    layer: typing.Literal["background", "foreground"] | None
    opacity: float | None
    font_size: float | None
    rotation: float | None
    color: str | None
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
#endregion

from oocana import Context
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
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
        # Apply default values for nullable parameters
        position_x = params.get("position_x") if params.get("position_x") is not None else 0.5
        position_y = params.get("position_y") if params.get("position_y") is not None else 0.5
        layer = params.get("layer") or "background"
        opacity = params.get("opacity") if params.get("opacity") is not None else 0.05
        font_size = params.get("font_size") if params.get("font_size") is not None else 36
        rotation = params.get("rotation") if params.get("rotation") is not None else 45
        color = params.get("color") or "#B8B8B8"

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
            x_pos = position_x * page_width
            y_pos = position_y * page_height

            if params.get("watermark_text") and params["watermark_text"].strip():
                # Text watermark
                can.setFillAlpha(opacity)
                can.setStrokeAlpha(opacity)
                can.setFillColor(HexColor(color))

                # Register and use font that supports Unicode/CJK
                try:
                    # Try to register fonts that support Chinese, Japanese, Korean
                    # Format: (path, subfontIndex) - subfontIndex is for TTC files
                    font_configs = [
                        ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 0),  # WenQuanYi Micro Hei (Linux)
                        ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 0),    # WenQuanYi Zen Hei (Linux)
                        ('/System/Library/Fonts/PingFang.ttc', 0),               # macOS
                        ('C:\\Windows\\Fonts\\msyh.ttc', 0),                     # Windows - Microsoft YaHei
                        ('C:\\Windows\\Fonts\\simsun.ttc', 0),                   # Windows - SimSun
                    ]

                    font_registered = False
                    for font_path, subfont_idx in font_configs:
                        if os.path.exists(font_path):
                            try:
                                pdfmetrics.registerFont(TTFont('CJKFont', font_path, subfontIndex=subfont_idx))
                                can.setFont("CJKFont", font_size)
                                font_registered = True
                                break
                            except:
                                continue

                    if not font_registered:
                        # Fallback to Helvetica if no CJK font found
                        can.setFont("Helvetica", font_size)
                except:
                    can.setFont("Helvetica", font_size)

                # Rotate and draw text
                can.translate(x_pos, y_pos)
                can.rotate(rotation)
                can.drawCentredString(0, 0, params["watermark_text"])

            elif params.get("watermark_image") and os.path.exists(params["watermark_image"]):
                # Image watermark with transparency support
                img = Image.open(params["watermark_image"])

                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Apply opacity to image
                if opacity < 1.0:
                    alpha = img.split()[3] if img.mode == 'RGBA' else Image.new('L', img.size, 255)
                    alpha = alpha.point(lambda p: int(p * opacity))
                    img.putalpha(alpha)

                img_width, img_height = img.size

                # Scale image to reasonable size
                max_size = min(page_width, page_height) * 0.3
                if img_width > max_size or img_height > max_size:
                    ratio = min(max_size / img_width, max_size / img_height)
                    new_width = int(img_width * ratio)
                    new_height = int(img_height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    new_width, new_height = img_width, img_height

                # Save processed image to BytesIO
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                # Draw image with rotation and transparency
                can.saveState()
                can.translate(x_pos, y_pos)
                can.rotate(rotation)
                can.drawImage(
                    ImageReader(img_buffer),
                    -new_width/2, -new_height/2,
                    new_width, new_height,
                    mask='auto'
                )
                can.restoreState()

            can.save()

            # Move to the beginning of the BytesIO buffer
            packet.seek(0)
            watermark_pdf = PdfReader(packet)

            # Merge watermark with original page
            if watermark_pdf.pages:
                watermark_page = watermark_pdf.pages[0]
                if layer == "background":
                    # Place watermark underneath content
                    watermark_page.merge_page(page)
                    writer.add_page(watermark_page)
                else:
                    # Place watermark on top of content (foreground)
                    page.merge_page(watermark_page)
                    writer.add_page(page)
            else:
                writer.add_page(page)
        
        # Determine output path
        output_path = params.get("output_path")
        if not output_path:
            # Generate default output path in session directory
            base_name = os.path.splitext(os.path.basename(params["pdf_path"]))[0]
            output_path = os.path.join(
                context.session_dir,
                f"{base_name}_watermarked_{context.job_id}.pdf"
            )

        # Write output PDF - ensure directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {"output_path": output_path}
        
    except Exception as e:
        raise Exception(f"Error adding watermark to PDF: {str(e)}")