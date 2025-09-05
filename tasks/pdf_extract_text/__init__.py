#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_format: typing.Literal["plain_text", "json", "csv"]
    page_range: str
    preserve_formatting: bool
    output_file: str | None
class Outputs(typing.TypedDict):
    extracted_text: str
    output_file: str | None
    pages_processed: float
#endregion

from oocana import Context
import pdfplumber
import json
import csv
import io

def main(params: Inputs, context: Context) -> dict:
    """
    Extract text from PDF file
    
    Args:
        params: Input parameters containing PDF path and extraction settings
        context: OOMOL context object
        
    Returns:
        Dictionary with extracted text and processing statistics
    """
    try:
        extracted_data = []
        pages_processed = 0
        
        with pdfplumber.open(params["pdf_path"]) as pdf:
            total_pages = len(pdf.pages)
            
            # Parse page range
            if params["page_range"].strip().lower() == "all":
                page_indices = range(total_pages)
            else:
                page_indices = parse_page_range(params["page_range"], total_pages)
            
            # Extract text from specified pages
            for page_index in page_indices:
                if 0 <= page_index < total_pages:
                    page = pdf.pages[page_index]
                    
                    if params["preserve_formatting"]:
                        # Extract with layout preservation
                        text = page.extract_text(layout=True)
                    else:
                        # Simple text extraction
                        text = page.extract_text()
                    
                    if text:
                        extracted_data.append({
                            "page": page_index + 1,
                            "text": text.strip()
                        })
                    
                    pages_processed += 1
        
        # Format output based on requested format
        if params["output_format"] == "json":
            output_text = json.dumps(extracted_data, indent=2, ensure_ascii=False)
        elif params["output_format"] == "csv":
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["page", "text"])\n            writer.writeheader()\n            writer.writerows(extracted_data)\n            output_text = output.getvalue()\n        else:  # plain_text\n            output_text = \"\\n\\n\".join([item[\"text\"] for item in extracted_data])\n        \n        # Save to file if specified\n        output_file_path = None\n        if params.get(\"output_file\"):\n            with open(params[\"output_file\"], 'w', encoding='utf-8') as f:\n                f.write(output_text)\n            output_file_path = params[\"output_file\"]\n        \n        return {\n            \"extracted_text\": output_text,\n            \"output_file\": output_file_path,\n            \"pages_processed\": pages_processed\n        }\n        \n    except Exception as e:\n        raise Exception(f\"Error extracting text from PDF: {str(e)}\")\n\ndef parse_page_range(range_str, total_pages):\n    \"\"\"Parse page range string like \"1-3,5\" into list of page indices (0-based)\"\"\"\n    pages = []\n    \n    for part in range_str.split(','):\n        part = part.strip()\n        \n        if '-' in part:\n            # Range like \"1-3\"\n            start, end = part.split('-', 1)\n            start = max(1, int(start.strip()))\n            end = min(total_pages, int(end.strip()))\n            \n            for page_num in range(start, end + 1):\n                pages.append(page_num - 1)  # Convert to 0-based index\n        else:\n            # Single page like \"5\"\n            page_num = int(part.strip())\n            if 1 <= page_num <= total_pages:\n                pages.append(page_num - 1)  # Convert to 0-based index\n    \n    return pages