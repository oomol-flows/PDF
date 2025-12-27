#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    password: str
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
    was_encrypted: typing.NotRequired[bool]
#endregion

from oocana import Context
from pypdf import PdfReader, PdfWriter

def main(params: Inputs, context: Context) -> dict:
    """
    Remove password protection from encrypted PDF
    
    Args:
        params: Input parameters containing PDF path and password
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path and encryption status
    """
    try:
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        
        # Check if PDF is encrypted
        was_encrypted = reader.is_encrypted
        
        # Decrypt if necessary
        if was_encrypted:
            if not reader.decrypt(params["password"]):
                raise Exception("Invalid password - could not decrypt PDF")
        
        # Create writer and copy all pages
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        
        # Write decrypted PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {
            "output_path": params["output_path"],
            "was_encrypted": was_encrypted
        }
        
    except Exception as e:
        raise Exception(f"Error decrypting PDF: {str(e)}")