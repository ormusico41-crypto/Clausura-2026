import re
import os
from PIL import Image, ImageOps
from io import BytesIO
import base64

html_path = "presentacion_consejo_clausura.html"
img_path = "LOGÍSTICA DEL EVENTO/FOTOS TEATRO WILLIAM SHAQUESPEARE/puerta_1.jpg"

try:
    # 1. Open the image and apply EXIF transposition to fix rotation
    img = Image.open(img_path)
    img = ImageOps.exif_transpose(img)
    
    # 2. If it's still sideways, we can manually rotate it.
    # Let's see its size to determine if it's sideways.
    print(f"Original size after EXIF transpose: {img.size}")
    
    # Let's just resize and convert to base64
    img.thumbnail((800, 800))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=80)
    new_base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    new_base64_src = f"data:image/jpeg;base64,{new_base64_str}"

    print(f"Generated new base64 string, length {len(new_base64_src)}")
except Exception as e:
    print(f"Error processing image: {e}")
