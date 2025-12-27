import os
import typing
import pypdf


class Inputs(typing.TypedDict):
  pdf: str

class Outputs(typing.TypedDict):
  name: str
  meta: dict

def main(params: Inputs) -> Outputs:
  pdf_path = params["pdf"]
  pdf_reader = pypdf.PdfReader(pdf_path)
  metadata = pdf_reader.metadata
  metadata_dict: dict[str, str] = {}
  if metadata is not None:
    for key, value in metadata.items():
      clean_key = key.lstrip("/") if key.startswith("/") else key
      metadata_dict[clean_key] = f"{value}"

  return {
    "name": os.path.splitext(os.path.basename(pdf_path))[0],
    "meta": metadata_dict,
  }
