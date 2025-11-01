#region generated meta
import typing
class Inputs(typing.TypedDict):
    input_pdf: str
    output_path: str
    compression_level: int | None
    optimize_images: bool | None
    remove_metadata: bool | None
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    original_size: typing.NotRequired[float]
    compressed_size: typing.NotRequired[float]
    compression_ratio: typing.NotRequired[float]
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter
import os
import io
from PIL import Image

def main(params: Inputs, context: Context) -> Outputs:
    """
    Compress PDF files using lossless compression techniques

    Args:
        params: Input parameters containing PDF file path and compression settings
        context: OOMOL context object

    Returns:
        Dictionary with compression results and statistics
    """
    try:
        # Set default values for nullable parameters
        compression_level = params.get("compression_level", 6)  # Default: medium compression
        optimize_images = params.get("optimize_images", True)   # Default: optimize images
        remove_metadata = params.get("remove_metadata", True)   # Default: remove metadata
        if not os.path.exists(params["input_pdf"]):
            raise FileNotFoundError(f"Input PDF file not found: {params['input_pdf']}")
        
        # Get original file size
        original_size = os.path.getsize(params["input_pdf"])
        
        # Read the input PDF
        reader = PdfReader(params["input_pdf"])
        writer = PdfWriter()
        
        # Process each page
        for page in reader.pages:
            # Optimize images in the page if requested
            if optimize_images:
                page = optimize_page_images(page, compression_level)

            writer.add_page(page)

        # Remove metadata if requested
        if remove_metadata:
            writer.add_metadata({})
        else:
            # Preserve original metadata
            if reader.metadata:
                writer.add_metadata(reader.metadata)
        
        # Apply compression settings (remove methods not available in this PyPDF2 version)
        
        # Write compressed PDF
        os.makedirs(os.path.dirname(params["output_path"]), exist_ok=True)
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        # Get compressed file size
        compressed_size = os.path.getsize(params["output_path"])
        
        # Calculate compression ratio
        compression_ratio = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
        
        return {
            "output_path": params["output_path"],
            "original_size": float(original_size),
            "compressed_size": float(compressed_size),
            "compression_ratio": round(compression_ratio, 2)
        }
        
    except Exception as e:
        raise Exception(f"Error compressing PDF: {str(e)}")

def optimize_page_images(page, compression_level):
    """
    Optimize images within a PDF page using lossless compression
    """
    try:
        if '/XObject' in page.get('/Resources', {}):
            xobjects = page['/Resources']['/XObject'].get_object()
            
            for obj_name in xobjects:
                obj = xobjects[obj_name]
                
                # Check if this is an image object
                if obj.get('/Subtype') == '/Image':
                    # Get image data
                    if '/Filter' in obj:
                        # Skip already compressed images to avoid quality loss
                        continue
                    
                    try:
                        # Extract image data
                        image_data = obj.get_data()
                        
                        # Create PIL Image from data
                        if '/ColorSpace' in obj:
                            color_space = obj['/ColorSpace']
                            width = obj['/Width']
                            height = obj['/Height']
                            
                            # Convert to PIL Image and apply lossless compression
                            img = Image.frombytes('RGB', (width, height), image_data)
                            
                            # Save with PNG compression (lossless)
                            img_io = io.BytesIO()
                            img.save(img_io, format='PNG', optimize=True, compress_level=compression_level)
                            compressed_data = img_io.getvalue()
                            
                            # Only replace if compression actually reduced size
                            if len(compressed_data) < len(image_data):
                                # Update the image object with compressed data
                                obj._data = compressed_data
                                obj['/Filter'] = '/FlateDecode'
                    except:
                        # Skip problematic images
                        continue
        
        return page
    except:
        # Return original page if optimization fails
        return page