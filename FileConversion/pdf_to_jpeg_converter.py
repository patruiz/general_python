import os
from pdf2image import convert_from_path

def pdf_to_image(pdf_directory):
    """
    Convert all PDF files in a specified directory to JPEG images.

    This function scans a given directory for PDF files, converts each one into
    images (one image per page), and saves the images in the same directory
    with the JPEG format. It assumes that the 'pdf2image' library is installed
    and functional.

    Args:
    pdf_directory (str): The path to the directory containing PDF files.

    Returns:
    None: Images are saved directly to the filesystem.

    Raises:
    FileNotFoundError: If the specified directory does not exist.
    """

    # Check if the specified directory exists
    if not os.path.exists(pdf_directory):
        raise FileNotFoundError(f"The directory {pdf_directory} does not exist.")

    # List all PDF files in the directory
    file_list = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    # Loop through each file in the list
    for pdf_file in file_list:
        # Full path to the PDF file
        full_pdf_path = os.path.join(pdf_directory, pdf_file)

        # Convert the PDF file to images (one per page)
        images = convert_from_path(full_pdf_path)

        # Save each page as a separate JPEG image
        for page_number, image in enumerate(images, start=1):
            img_name = f"{pdf_file[:-4]}_page_{page_number}.jpeg"  # Name images to include page number
            image.save(os.path.join(pdf_directory, img_name), 'JPEG')
