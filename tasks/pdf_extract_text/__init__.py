#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_file: str | None
    page_range: str | None
    preserve_formatting: bool | None
class Outputs(typing.TypedDict):
    markdown_file: typing.NotRequired[str]
    pages_processed: typing.NotRequired[float]
#endregion

from oocana import Context
import pdfplumber
import os
import tempfile

def main(params: Inputs, context: Context) -> dict:
    """
    Extract text from PDF file and save as markdown

    Args:
        params: Input parameters containing PDF path and extraction settings
        context: OOMOL context object

    Returns:
        Dictionary with markdown file path and processing statistics
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

        # Generate markdown content
        markdown_lines = []
        for item in extracted_data:
            markdown_lines.append(f"## Page {item['page']}\n")
            markdown_lines.append(f"{item['text']}\n")

        markdown_content = "\n".join(markdown_lines)

        # Determine output file path
        if params.get("output_file"):
            output_path = params["output_file"]
        else:
            # Generate temp file with .md extension
            pdf_basename = os.path.splitext(os.path.basename(params["pdf_path"]))[0]
            output_path = os.path.join(tempfile.gettempdir(), f"{pdf_basename}_extracted.md")

        # Save to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return {
            "markdown_file": output_path,
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