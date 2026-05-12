from PIL import Image
from pillow_heif import register_heif_opener
import os

register_heif_opener()

input_path = "LOGÍSTICA DEL EVENTO/FOTOS TEATRO WILLIAM SHAQUESPEARE/Pasillo principal camerinos.HEIC"
output_path = "LOGÍSTICA DEL EVENTO/FOTOS TEATRO WILLIAM SHAQUESPEARE/pasillo_principal.jpg"

try:
    img = Image.open(input_path)
    # Resize to optimize
    img.thumbnail((800, 800))
    img.save(output_path, "JPEG", quality=85)
    print(f"Successfully converted {input_path} to {output_path}")
except Exception as e:
    print(f"Error: {e}")
