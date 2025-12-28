import os
from oocana import Context
from typing import Any
from tempfile import TemporaryDirectory
from pypdf import PdfWriter
from PIL import Image, UnidentifiedImageError


def main(params: dict, context: Context):
    title: str | None = params.get("title")
    author: str | None = params.get("author")
    image_paths: list[str] = params.get("image_paths", [])
    pdf_file_path: str | None = params.get("pdf_file_path")

    if pdf_file_path is not None:
        if not pdf_file_path.lower().endswith(".pdf"):
            pdf_file_path = f"{pdf_file_path}/{context.job_id}.pdf" if not os.path.isdir(pdf_file_path) else os.path.join(pdf_file_path, f"{context.job_id}.pdf")
    else:
        pdf_file_path = os.path.join(
            context.session_dir,
            f"{context.job_id}.pdf",
        )

    metadata: dict[str, Any] = {}
    if title is not None:
        metadata["/Title"] = title
    if author is not None:
        metadata["/Author"] = author

    # Validate images first without closing them
    valid_images = []
    for image_path in image_paths:
        try:
            # Open and verify without closing the file
            img = Image.open(image_path)
            img.verify()
            # Need to re-open after verify as it closes the file
            img = Image.open(image_path)
            img.close()
            valid_images.append(image_path)
        except (UnidentifiedImageError, IOError):
            print(f"Skipping non-image file: {image_path}")
            continue

    if not valid_images:
        raise ValueError("No valid images found in the input list")

    # Create PDF writer and temporary directory
    writer = PdfWriter()

    with TemporaryDirectory() as temp_dir:
        # Convert each image to a temporary PDF page
        for i, image_path in enumerate(valid_images):
            with Image.open(image_path) as image:
                rgb_image = image.convert("RGB")
                page_path = os.path.join(temp_dir, f"page_{i}.pdf")
                rgb_image.save(page_path, "PDF", resolution=100.0)
                writer.append(page_path)
                context.report_progress((i + 1) / len(valid_images) * 90.0)

        # Add metadata if provided
        if metadata:
            writer.add_metadata(metadata)

        # Write the final PDF file
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
        with open(pdf_file_path, "wb") as output_file:
            writer.write(output_file)
        writer.close()

    context.report_progress(100.0)

    return {"pdf_file_path": pdf_file_path}
