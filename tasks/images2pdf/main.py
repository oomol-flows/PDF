import os

from oocana import Context
from typing import Any
from tempfile import TemporaryDirectory
from PyPDF2 import PdfMerger
from PIL import Image

def main(params: dict, context: Context):
  title: str | None = params["title"]
  author: str | None = params["author"]
  image_paths: str = params["image_paths"]
  pdf_file_path: str | None = params["pdf_file_path"]

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

  with TemporaryDirectory() as temp_dir:
    with PdfMerger() as merger:
      for i, image_path in enumerate(image_paths):
        image = Image.open(image_path).convert()
        page_path = os.path.join(temp_dir, f"{i}.pdf")
        page_width, page_height = image.size
        image.save(
          fp=page_path, 
          save_all=True,
        )
        merger.append(page_path)
        context.report_progress(i/len(image_paths) * 90.0)

      if len(metadata) > 0:
        merger.add_metadata(metadata)
      merger.write(pdf_file_path)
    
  return { "pdf_file_path": pdf_file_path }