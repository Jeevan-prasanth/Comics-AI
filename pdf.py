from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def images_to_pdf(input_folder, output_pdf):
    # Get all image files from input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png') or f.endswith('.jpg')]

    # Sort image files by name (assuming filenames are numbered)
    image_files.sort()

    # Create a PDF file
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Calculate page size and orientation based on image dimensions
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        width, height = img.size

        # Determine orientation based on image dimensions
        if width > height:
            c.setPageSize((height, width))
            c.rotate(90)
        else:
            c.setPageSize((width, height))

        # Draw the image on the page
        c.drawImage(image_path, 0, 0, width, height)
        c.showPage()

    c.save()

    print(f"PDF created: {output_pdf}")
'''
def main():
    input_folder = 'output1'  # Change this to your input folder containing images
    output_pdf = 'output.pdf'  # Output PDF file name

    images_to_pdf(input_folder, output_pdf)

if __name__ == "__main__":
    main()
'''