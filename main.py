import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import sys

def image_to_ascii_art(image_path, output_path="ascii_output.png", font_size=12, density_scale="complex"):
    RAMPS = {
        "simple": "@%#*+=-:. ",
        "complex": r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    }
    
    chars = RAMPS[density_scale]
    chars = chars[::-1] 
    
    try:
        img = Image.open(image_path)
        char_width_aspect = 0.6
        
        orig_width, orig_height = img.size
        cols = int(orig_width / (font_size * char_width_aspect))
        rows = int(orig_height / font_size)
        
        print(f"Generating ASCII grid: {cols}x{rows}...")

        img_small = img.resize((cols, rows), Image.Resampling.HAMMING)
        
        img_gray = img_small.convert("L")
        pixels = np.array(img_gray)
        
        pixel_indices = (pixels / 255 * (len(chars) - 1)).astype(int)
        
        out_width = int(cols * font_size * char_width_aspect)
        out_height = int(rows * font_size)
        
        output_image = Image.new("RGB", (out_width, out_height), "black")
        draw = ImageDraw.Draw(output_image)
        
        try:
                font = ImageFont.truetype("Courier", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

        print("Rendering pixels to characters... (This might take a moment)")
        
        for r in range(rows):
            line_chars = ""
            for c in range(cols):
                char_idx = pixel_indices[r, c]
                char = chars[char_idx]
                
                draw.text(
                    (int(c * font_size * char_width_aspect), r * font_size), 
                    char, 
                    font=font, 
                    fill=(255, 255, 255)
                )

        output_image.save(output_path)
        print(f"Success! Saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_filename = "Billie-Eilish-Happier-Than-Ever.jpeg" 
    
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        
    image_to_ascii_art(input_filename, density_scale="complex", font_size=10)