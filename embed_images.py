import re
import base64
import os
from PIL import Image
from io import BytesIO
import urllib.parse

html_path = "presentacion_consejo_clausura.html"
base_dir = "/Users/ciedimusica1/Library/CloudStorage/OneDrive-CIEDI/2025 - 2026/DEPARTAMENTO DE ARTES/CEREMONIA DE CLAUSURA"

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Buscamos todos los <img src="...">
img_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"')
matches = img_pattern.findall(html_content)

for src in matches:
    if src.startswith("data:"):
        continue  # Ya es base64
    
    # Resolvamos la ruta. Si tiene espacios o está decodificada, mejor manejamos ambos casos
    unquoted_src = urllib.parse.unquote(src)
    full_path = os.path.join(base_dir, unquoted_src)
    
    if os.path.exists(full_path):
        try:
            img = Image.open(full_path)
            # Resize
            img.thumbnail((800, 800))
            
            # Convertir a JPEG en memoria
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=80)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            base64_src = f"data:image/jpeg;base64,{img_str}"
            
            # Reemplazar exactamente el src original en el html_content
            # Solo la primera coincidencia del string exacto para evitar conflictos
            html_content = html_content.replace(f'src="{src}"', f'src="{base64_src}"')
            print(f"Embedded: {src}")
        except Exception as e:
            print(f"Error processing {src}: {e}")
    else:
        print(f"File not found: {full_path}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Finished embedding images.")
