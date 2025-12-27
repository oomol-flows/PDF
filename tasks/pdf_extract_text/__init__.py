#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_format: typing.Literal["plain_text", "json", "csv"]
    output_file: str | None
    page_range: str | None
    preserve_formatting: bool | None
class Outputs(typing.TypedDict):
    extracted_text: typing.NotRequired[str]
    output_file: typing.NotRequired[str | None]
    pages_processed: typing.NotRequired[float]
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
        # Apply default values for nullable parameters
        page_range = params.get("page_range") or "all"
        preserve_formatting = params.get("preserve_formatting") if params.get("preserve_formatting") is not None else True

        extracted_data = []
        pages_processed = 0

        with pdfplumber.open(params["pdf_path"]) as pdf:
            total_pages = len(pdf.pages)

            # Parse page range
            if page_range.strip().lower() == "all":
                page_indices = range(total_pages)
            else:
                page_indices = parse_page_range(page_range, total_pages)

            # Extract text from specified pages
            for page_index in page_indices:
                if 0 <= page_index < total_pages:
                    page = pdf.pages[page_index]

                    if preserve_formatting:
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
            writer = csv.DictWriter(output, fieldnames=["page", "text"])
            writer.writeheader()
            writer.writerows(extracted_data)
            output_text = output.getvalue()
        else:  # plain_text
            output_text = "\n\n".join([item["text"] for item in extracted_data])
        
        # Save to file if specified
        output_file_path = None
        if params.get("output_file"):
            with open(params["output_file"], 'w', encoding='utf-8') as f:
                f.write(output_text)
            output_file_path = params["output_file"]
        
        return {
            "extracted_text": output_text,
            "output_file": output_file_path,
            "pages_processed": pages_processed
        }
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def parse_page_range(range_str, total_pages):
    """Parse page range string like "1-3,5" into list of page indices (0-based)"""
    pages = []
    
    for part in range_str.split(','):
        part = part.strip()
        
        if '-' in part:
            # Range like "1-3"
            start, end = part.split('-', 1)
            start = max(1, int(start.strip()))
            end = min(total_pages, int(end.strip()))
            
            for page_num in range(start, end + 1):
                pages.append(page_num - 1)  # Convert to 0-based index
        else:
            # Single page like "5"
            page_num = int(part.strip())
            if 1 <= page_num <= total_pages:
                pages.append(page_num - 1)  # Convert to 0-based index
    
    return pages