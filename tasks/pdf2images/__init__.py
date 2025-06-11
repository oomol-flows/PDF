import os
from oocana import Context
from pdf2image import convert_from_path


def main(params: dict, context: Context):
    pdf_path = params.get("pdf_path")
    image_dir = params.get("image_dir")

    if pdf_path is None:
        raise ValueError("pdf_path is required")

    if image_dir is None:
        image_dir = os.path.join(
            context.session_dir,
            context.job_id,
        )
    os.makedirs(image_dir, exist_ok=True)

    pdf_to_images(pdf_path, image_dir, context)

    return {"image_dir": image_dir}


def pdf_to_images(pdf_path, output_folder, context):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    total_pages = len(images)
    percentage = 0
    # Save each image
    for i, image in enumerate(images):
        # Calculate the percentage of the current page
        percentage = (i + 1) / total_pages * 100
        # Print or record percentage
        context.report_progress(percentage)
        image_path = f"{output_folder}/page_{i + 1}.png"
        image.save(image_path, "PNG")