import os
import pandas as pd
from docx import Document
import json

base_dir = "/Users/ciedimusica1/Library/CloudStorage/OneDrive-CIEDI/2025 - 2026/DEPARTAMENTO DE ARTES/CEREMONIA DE CLAUSURA/CEREMONIA DE CLAUSURA BACHILLERATO"

excel_files = [
    "DANZA GRADO 6°.xlsx",
    "DANZA GRADO 7°.xlsx",
    "DANZA GRADO 8°.xlsx",
    "DANZA GRADO 9°.xlsx",
    "MÚSICA GRADO 6°.xlsx",
    "MÚSICA GRADO 7°.xlsx",
    "MÚSICA GRADO 8°.xlsx",
    "MÚSICA GRADO 9°.xlsx",
    "MÚSICA GRADOS 10° Y 11°.xlsx"
]

data = {}

for file in excel_files:
    file_path = os.path.join(base_dir, file)
    try:
        df = pd.read_excel(file_path, header=None)
        
        # Iterar sobre las filas y si tienen valor en la columna 0 y 1 concatenarlas
        names = []
        for index, row in df.iterrows():
            nombre = str(row[0]).strip() if pd.notna(row[0]) else ""
            apellido = str(row[1]).strip() if pd.notna(row[1]) else ""
            
            # Omitir filas vacías o con encabezados
            if nombre == "" or nombre.lower() == "nombre" or nombre.startswith("GRADO"):
                continue
                
            full_name = f"{nombre} {apellido}".strip()
            if full_name:
                names.append(full_name)
        data[file.replace('.xlsx', '')] = names
    except Exception as e:
        print(f"Error reading {file}: {e}")

# The Staff is fine as is
staff_file = os.path.join(base_dir, "LISTADOS STAFF DE ARTES VISUALES.docx")
try:
    doc = Document(staff_file)
    staff_names = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            staff_names.append(text)
    data["STAFF DE ARTES V."] = staff_names
except Exception as e:
    print(f"Error reading {staff_file}: {e}")

with open('extracted_names_full.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

