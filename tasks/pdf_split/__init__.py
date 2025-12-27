#region generated meta
import typing
class Inputs(typing.TypedDict):
    pdf_path: str
    output_dir: str
    split_mode: typing.Literal["single_pages", "page_ranges", "bookmarks", "equal_parts"]
    page_ranges: str | None
    pages_per_part: float | None
    filename_prefix: str | None
class Outputs(typing.TypedDict):
    output_files: typing.NotRequired[list[str]]
    files_created: typing.NotRequired[float]
#endregion

from oocana import Context
from pypdf import PdfReader, PdfWriter
import os
import re

def main(params: Inputs, context: Context) -> dict:
    """
    Split PDF into separate files
    
    Args:
        params: Input parameters containing PDF path and split settings
        context: OOMOL context object
        
    Returns:
        Dictionary with output files list and statistics
    """
    try:
        # Read input PDF
        reader = PdfReader(params["pdf_path"])
        total_pages = len(reader.pages)

        if total_pages == 0:
            raise ValueError("PDF has no pages")

        # Create output directory if it doesn't exist
        os.makedirs(params["output_dir"], exist_ok=True)

        # Apply default values for nullable fields
        pages_per_part = int(params.get("pages_per_part") or 10)
        filename_prefix = params.get("filename_prefix") or "page"

        output_files = []

        if params["split_mode"] == "single_pages":
            # Split into individual pages
            for page_num in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])

                filename = f"{filename_prefix}_{page_num + 1:03d}.pdf"
                output_path = os.path.join(params["output_dir"], filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                output_files.append(output_path)

        elif params["split_mode"] == "page_ranges":
            # Split by specified page ranges
            if not params["page_ranges"]:
                raise ValueError("Page ranges must be specified for page_ranges mode")

            ranges = parse_page_ranges(params["page_ranges"], total_pages)

            for range_index, (start, end) in enumerate(ranges):
                writer = PdfWriter()

                for page_num in range(start - 1, end):
                    if 0 <= page_num < total_pages:
                        writer.add_page(reader.pages[page_num])

                filename = f"{filename_prefix}_range_{range_index + 1}_{start}-{end}.pdf"
                output_path = os.path.join(params["output_dir"], filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                output_files.append(output_path)

        elif params["split_mode"] == "bookmarks":
            # Split by bookmarks
            if not reader.outline:
                raise ValueError("PDF has no bookmarks to split by")

            bookmark_pages = extract_bookmark_pages(reader.outline)
            bookmark_pages.append(total_pages)  # Add final page

            for i in range(len(bookmark_pages) - 1):
                start_page = bookmark_pages[i]
                end_page = bookmark_pages[i + 1]

                writer = PdfWriter()
                for page_num in range(start_page, end_page):
                    if 0 <= page_num < total_pages:
                        writer.add_page(reader.pages[page_num])

                filename = f"{filename_prefix}_bookmark_{i + 1}.pdf"
                output_path = os.path.join(params["output_dir"], filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                output_files.append(output_path)

        elif params["split_mode"] == "equal_parts":
            # Split into equal parts
            part_num = 1

            for start_page in range(0, total_pages, pages_per_part):
                writer = PdfWriter()
                end_page = min(start_page + pages_per_part, total_pages)

                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])

                filename = f"{filename_prefix}_part_{part_num:02d}.pdf"
                output_path = os.path.join(params["output_dir"], filename)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                output_files.append(output_path)
                part_num += 1
        
        return {
            "output_files": output_files,
            "files_created": len(output_files)
        }
        
    except Exception as e:
        raise Exception(f"Error splitting PDF: {str(e)}")

def parse_page_ranges(ranges_str, total_pages):
    """Parse page ranges string like "1-3,5-7,10" into list of (start, end) tuples"""
    ranges = []
    
    for range_part in ranges_str.split(','):
        range_part = range_part.strip()
        
        if '-' in range_part:
            # Range like "1-3"
            start, end = range_part.split('-', 1)
            start = int(start.strip())
            end = int(end.strip())
        else:
            # Single page like "10"
            start = end = int(range_part)
        
        # Validate range
        start = max(1, min(start, total_pages))
        end = max(start, min(end, total_pages))
        
        ranges.append((start, end))
    
    return ranges

def extract_bookmark_pages(outline, pages=None):
    """Extract page numbers from PDF bookmarks"""
    if pages is None:
        pages = []
    
    for item in outline:
        if isinstance(item, list):
            # Nested bookmarks
            extract_bookmark_pages(item, pages)
        else:
            try:
                page_num = item.page.idnum
                if page_num not in pages:
                    pages.append(page_num)
            except:
                pass
    
    return sorted(pages)