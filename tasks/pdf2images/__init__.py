from oocana import Context
from pdf2image import convert_from_path

def main(params: dict, context: Context):

  pdf_path = params.get("pdf_path")
  image_dir = params.get("image_dir")

  if pdf_path is None:
    raise ValueError("pdf_path is required")

  if image_dir is None:
    image_dir = context.session_dir


  pdf_to_images(pdf_path, image_dir, context)

  return { "image_dir": image_dir }

def pdf_to_images(pdf_path, output_folder, context):
    # 将 PDF 转换为图片
    images = convert_from_path(pdf_path)
    total_pages = len(images)
    percentage = 0
    # 保存每张图片
    for i, image in enumerate(images):
      # 计算当前页码的百分比
        percentage = (i + 1) / total_pages * 100
        # 打印或记录百分比
        context.report_progress(percentage)
        image_path = f"{output_folder}/page_{i + 1}.png"
        image.save(image_path, "PNG")