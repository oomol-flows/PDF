import os
from oocana import Context
from typing import Any
from tempfile import TemporaryDirectory
from PyPDF2 import PdfMerger
from PIL import Image, UnidentifiedImageError

def main(params: dict, context: Context):
  title: str | None = params.get("title")
  author: str | None = params.get("author")
  image_paths: list[str] = params.get("image_paths", [])
  pdf_file_path: str | None = params.get("pdf_file_path")

  if pdf_file_path is None:
    pdf_file_path = os.path.join(
      context.session_dir,
      f"{context.job_id}.pdf",
    )

  metadata: dict[str, Any] = {}
  if title is not None:
    metadata["/Title"] = title
  if author is not None:
    metadata["/Author"] = author

  valid_images = []
  with TemporaryDirectory() as temp_dir:
    with PdfMerger() as merger:
      for i, image_path in enumerate(image_paths):
        try:
          with Image.open(image_path) as img:
            img.verify()
          valid_images.append(image_path)
        except (UnidentifiedImageError, IOError):
          print(f"Skipping non-image file: {image_path}")
          continue

      for i, image_path in enumerate(valid_images):
        image = Image.open(image_path).convert("RGB")
        page_path = os.path.join(temp_dir, f"{i}.pdf")
        image.save(page_path, "PDF", resolution=100.0)
        merger.append(page_path)
        context.report_progress((i + 1) / len(valid_images) * 90.0)

      if metadata:
        merger.add_metadata(metadata)
      merger.write(pdf_file_path)

    context.report_progress(100.0)

  return { "pdf_file_path": pdf_file_path }
