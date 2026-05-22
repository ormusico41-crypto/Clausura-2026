import PyPDF2
import os

pdf_path = "RIDER DE SONIDO - STAGE PLOT.pdf"
output_dir = "scratch"

reader = PyPDF2.PdfReader(pdf_path)
page = reader.pages[0]

count = 0
for image_file_object in page.images:
    name = f"image_{count}_{image_file_object.name}"
    full_path = os.path.join(output_dir, name)
    with open(full_path, "wb") as fp:
        fp.write(image_file_object.data)
    print(f"Saved: {full_path}")
    count += 1

print(f"Extracted {count} images.")
