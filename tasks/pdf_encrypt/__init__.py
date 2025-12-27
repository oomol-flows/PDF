#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_path: str
    user_password: str
    owner_password: str | None
    allow_printing: bool | None
    allow_copying: bool | None
    allow_modification: bool | None
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
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

        # Apply default values for nullable fields
        allow_printing = params.get("allow_printing") if params.get("allow_printing") is not None else True
        allow_copying = params.get("allow_copying") if params.get("allow_copying") is not None else True
        allow_modification = params.get("allow_modification") if params.get("allow_modification") is not None else False

        # Set permissions
        use_128bit = True

        # Apply encryption with passwords and permissions
        writer.encrypt(
            user_pwd=params["user_password"],
            owner_pwd=params.get("owner_password") or params["user_password"],
            use_128bit=use_128bit,
            permissions_flag=(
                (4 if allow_printing else 0) |
                (16 if allow_copying else 0) |
                (8 if allow_modification else 0)
            )
        )
        
        # Write encrypted PDF
        with open(params["output_path"], 'wb') as output_file:
            writer.write(output_file)
        
        return {"output_path": params["output_path"]}
        
    except Exception as e:
        raise Exception(f"Error encrypting PDF: {str(e)}")