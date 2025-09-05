#region generated meta
import typing
class Inputs(typing.TypedDict):
    input_source: str
    html_file: typing.Optional[str]
    html_string: typing.Optional[str]
    url: typing.Optional[str]
    output_path: str
    page_size: str
    orientation: str
    margin_top: float
    margin_bottom: float
    margin_left: float
    margin_right: float
#endregion

from oocana import Context
from weasyprint import HTML, CSS
from weasyprint.css import get_all_computed_styles
from weasyprint.css.targets import get_all_computed_styles
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
        page_sizes = {\n            \"A4\": \"210mm 297mm\",\n            \"A3\": \"297mm 420mm\",\n            \"A5\": \"148mm 210mm\",\n            \"Letter\": \"8.5in 11in\",\n            \"Legal\": \"8.5in 14in\"\n        }\n        \n        page_size_value = page_sizes.get(params[\"page_size\"], \"210mm 297mm\")\n        \n        if params[\"orientation\"] == \"landscape\":\n            # Swap width and height for landscape\n            dimensions = page_size_value.split()\n            page_size_value = f\"{dimensions[1]} {dimensions[0]}\"\n        \n        css_style = f\"\"\"\n        @page {{\n            size: {page_size_value};\n            margin-top: {params['margin_top']}mm;\n            margin-bottom: {params['margin_bottom']}mm;\n            margin-left: {params['margin_left']}mm;\n            margin-right: {params['margin_right']}mm;\n        }}\n        \"\"\"\n        \n        # Generate PDF\n        html_doc.write_pdf(\n            params[\"output_path\"],\n            stylesheets=[CSS(string=css_style)]\n        )\n        \n        return {\"output_path\": params[\"output_path\"]}\n        \n    except Exception as e:\n        raise Exception(f\"Error converting HTML to PDF: {str(e)}\")