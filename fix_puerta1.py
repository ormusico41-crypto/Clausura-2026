import os
import base64
from PIL import Image, ImageOps
from io import BytesIO

html_path = "presentacion_consejo_clausura.html"
img_path = "LOGÍSTICA DEL EVENTO/FOTOS TEATRO WILLIAM SHAQUESPEARE/puerta_1.jpg"

# 1. Generate the BAD base64 string (exactly how it was generated before)
img_bad = Image.open(img_path)
img_bad.thumbnail((800, 800))
if img_bad.mode in ("RGBA", "P"):
    img_bad = img_bad.convert("RGB")
buffered_bad = BytesIO()
img_bad.save(buffered_bad, format="JPEG", quality=80)
bad_base64_str = base64.b64encode(buffered_bad.getvalue()).decode("utf-8")
bad_base64_src = f"data:image/jpeg;base64,{bad_base64_str}"

# 2. Generate the GOOD base64 string (with EXIF transpose)
img_good = Image.open(img_path)
img_good = ImageOps.exif_transpose(img_good) # This fixes the EXIF orientation
img_good.thumbnail((800, 800))
if img_good.mode in ("RGBA", "P"):
    img_good = img_good.convert("RGB")
buffered_good = BytesIO()
img_good.save(buffered_good, format="JPEG", quality=80)
good_base64_str = base64.b64encode(buffered_good.getvalue()).decode("utf-8")
good_base64_src = f"data:image/jpeg;base64,{good_base64_str}"

print(f"Bad length: {len(bad_base64_src)}")
print(f"Good length: {len(good_base64_src)}")

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

count = html_content.count(bad_base64_src)
print(f"Found {count} instances of the bad image in the HTML.")

if count > 0:
    html_content = html_content.replace(bad_base64_src, good_base64_src)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Replaced all instances!")
else:
    print("Could not find the bad base64 string in the HTML.")

