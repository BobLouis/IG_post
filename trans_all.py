import os
from PIL import Image, ImageDraw
import subprocess
def add_rounded_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    
    w, h = im.size
    mask = Image.new('L', (w, h), 255)
    mask.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    mask.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    mask.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    mask.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    
    im.putalpha(mask)
    return im.convert("RGBA")

def transform_img(input_file, output_file):
    img = Image.open(input_file)
    width, height = img.size
    new_dimension = min(width, height)
    left = (width - new_dimension) / 2
    top = (height - new_dimension) / 2
    right = (width + new_dimension) / 2
    bottom = (height + new_dimension) / 2
    img = img.crop((left, top, right, bottom))

    img_rgba = img.convert("RGBA")
    rounded_img = add_rounded_corners(img_rgba, int(0.08 * new_dimension))

    background_img = Image.open("templete.png")
    bg_width, bg_height = background_img.size
    new_width = int(bg_width * 0.9)
    new_height = int(bg_height * 0.9)
    resized_bordered_img = rounded_img.resize((new_width, new_height), Image.ANTIALIAS)

    paste_x = (bg_width - new_width) // 2 - 5
    paste_y = (bg_height - new_height) // 2 - 5

    background_img.paste(resized_bordered_img, (paste_x, paste_y), mask=resized_bordered_img.split()[3])
    background_img.save(output_file)

def process_directory(input_dir, output_count=1):
    source_file = "封面.ai"
    for file_name in os.listdir(input_dir):
        full_path = os.path.join(input_dir, file_name)
        
        # Skip the folder named "已發出貼文"
        if file_name == "已發出貼文":
            continue

        # If it's a directory, process it recursively
        if os.path.isdir(full_path):
            process_directory(full_path, output_count)
        else:
            # Transform .jpg, .webp, and .heic files
            if file_name.endswith(('.jpg', '.webp', '.heic')):
                output_file = f"{output_count}.png"
                transform_img(full_path, os.path.join(input_dir, output_file))
                output_count += 1

        if os.path.isdir(file_name):
            subprocess.run(["cp", source_file, file_name])


if __name__ == "__main__":
    input_dir = '.'  # Start with the current directory
    process_directory(input_dir)




