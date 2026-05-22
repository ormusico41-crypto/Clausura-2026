import PyPDF2

pdf_path = "RIDER DE SONIDO - STAGE PLOT.pdf"
output_path = "scratch/pdf_text.txt"

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    print(f"Number of pages: {len(reader.pages)}")
    
    with open(output_path, "w", encoding="utf-8") as out:
        for idx, page in enumerate(reader.pages):
            out.write(f"\n--- PAGE {idx+1} ---\n")
            text = page.extract_text()
            out.write(text)

print("Done extracting PDF.")
