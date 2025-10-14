#region generated meta
import typing
class Inputs(typing.TypedDict):
    input_source: typing.Literal["html_file", "html_string", "url"]
    html_file: str | None
    html_string: str | None
    url: str | None
    output_path: str
    page_size: typing.Literal["A4", "A3", "A5", "Letter", "Legal"]
    orientation: typing.Literal["portrait", "landscape"]
    margin_top: float
    margin_bottom: float
    margin_left: float
    margin_right: float
class Outputs(typing.TypedDict):
    output_path: typing.NotRequired[str]
#endregion

from oocana import Context
from weasyprint import HTML, CSS
import os
import requests

def main(params: Inputs, context: Context) -> dict:
    """
    Convert HTML to PDF
    
    Args:
        params: Input parameters containing HTML source and PDF settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output file path
    """
    try:
        # Get HTML content based on input source
        if params["input_source"] == "html_file":
            if not params.get("html_file") or not os.path.exists(params["html_file"]):
                raise ValueError("HTML file not specified or does not exist")
            
            with open(params["html_file"], 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            html_doc = HTML(string=html_content, base_url=os.path.dirname(params["html_file"]))
            
        elif params["input_source"] == "html_string":
            if not params.get("html_string"):
                raise ValueError("HTML string not provided")
            
            html_doc = HTML(string=params["html_string"])
            
        elif params["input_source"] == "url":
            if not params.get("url"):
                raise ValueError("URL not provided")
            
            html_doc = HTML(url=params["url"])
            
        else:
            raise ValueError("Invalid input source type")
        
        # Create CSS for page settings
        page_sizes = {
            "A4": "210mm 297mm",
            "A3": "297mm 420mm",
            "A5": "148mm 210mm",
            "Letter": "8.5in 11in",
            "Legal": "8.5in 14in"
        }
        
        page_size_value = page_sizes.get(params["page_size"], "210mm 297mm")
        
        if params["orientation"] == "landscape":
            # Swap width and height for landscape
            dimensions = page_size_value.split()
            page_size_value = f"{dimensions[1]} {dimensions[0]}"
        
        css_style = f"""
        @page {{
            size: {page_size_value};
            margin-top: {params['margin_top']}mm;
            margin-bottom: {params['margin_bottom']}mm;
            margin-left: {params['margin_left']}mm;
            margin-right: {params['margin_right']}mm;
        }}
        """
        
        # Generate PDF
        html_doc.write_pdf(
            params["output_path"],
            stylesheets=[CSS(string=css_style)]
        )
        
        return {"output_path": params["output_path"]}
        
    except Exception as e:
        raise Exception(f"Error converting HTML to PDF: {str(e)}")