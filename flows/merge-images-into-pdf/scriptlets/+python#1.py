def main(params: dict):
  image_paths: list[str] = params["image_paths"]
  image_paths.sort()
  return { "image_paths": image_paths }
