#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    user_password: str
    owner_password: str | None
    allow_printing: bool
    allow_copying: bool
    allow_modification: bool
class Outputs(typing.TypedDict):
    output_path: str
#endregion

from oocana import Context
from PyPDF2 import PdfReader, PdfWriter

def main(params: Inputs, context: Context) -> dict:
    """
    Encrypt PDF file with password protection
    
    Args:
        params: Input parameters containing PDF path and encryption settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path
    """
    try:
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Set permissions
        use_128bit = True
        
        # Apply encryption with passwords and permissions
        writer.encrypt(
            user_pwd=params["user_password"],
            owner_pwd=params.get("owner_password") or params["user_password"],
            use_128bit=use_128bit,
            permissions_flag=(
                (4 if params["allow_printing"] else 0) |
                (16 if params["allow_copying"] else 0) |
                (8 if params["allow_modification"] else 0)
            )
        )
        
        # Write encrypted PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {"output_path": params["output_path"]}
        
    except Exception as e:
        raise Exception(f"Error encrypting PDF: {str(e)}")