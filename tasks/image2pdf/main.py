from oocana import Context
import img2pdf
from PIL import Image
import os
# "in", "out" is the default node key.
# Redefine the name and type of the node, change it manually below.
# Click on the gear(⚙) to configure the input output UI

def main(inputs: dict, context: Context):
    # 调用函数
    image_files = inputs.get('paths')
    name = inputs.get('name')
    out_folder = inputs.get('out_folder')
    output_pdf = out_folder + name + ".pdf"
    images_to_pdf(image_files, output_pdf, context)

    return { "file_address": output_pdf }
def images_to_pdf(image_files, output_pdf, context):
    
    # 按文件名排序（可选）
    image_files.sort()

    total_images = len(image_files)
    converted_images = []

    # 处理每一张图片，并计算进度
    for index, image_path in enumerate(image_files):
        converted_images.append(image_path)
        progress_percentage = (index + 1) / total_images * 100
        context.report_progress(progress_percentage)
        print(progress_percentage)
        
        # 检查是否所有图片都已经处理完毕
        if len(converted_images) == total_images:
            break

    # 使用img2pdf转换器将图像文件路径列表转为PDF字节流，并写入到文件中
    pdf_bytes = img2pdf.convert(image_files)
    
    with open(output_pdf, "wb") as f:
        f.write(pdf_bytes)
