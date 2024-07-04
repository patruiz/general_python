import os  # Import the os module to handle directory operations
import PyPDF2  # Import the PyPDF2 library to work with PDF files

def combine_pdfs(directory, output_file):
    """
    Combine all PDF files in a specified directory into a single PDF file.

    :param directory: Path to the directory containing PDF files.
    :param output_file: Name of the output file where combined PDF will be saved.
    """
    # Create a PdfWriter object to write the combined PDF
    pdf_writer = PyPDF2.PdfWriter()
    
    # Loop through all the files in the specified directory
    for filename in sorted(os.listdir(directory)):
        # Check if the current file is a PDF by looking at its extension
        if filename.endswith('.pdf'):
            # Construct the full path to the current PDF file
            pdf_path = os.path.join(directory, filename)
            
            # Create a PdfReader object to read the current PDF file
            pdf_reader = PyPDF2.PdfReader(pdf_path)
            
            # Loop through all the pages in the current PDF file
            for page_num in range(len(pdf_reader.pages)):
                # Add each page of the current PDF to the PdfWriter object
                pdf_writer.add_page(pdf_reader.pages[page_num])
    
    # Open the output file in write-binary mode to save the combined PDF
    with open(output_file, 'wb') as output_pdf:
        # Write the combined PDF content to the output file
        pdf_writer.write(output_pdf)

# Example usage of the combine_pdfs function
directory = r'C:\Users\pr19556\OneDrive - Applied Medical\Documents\Golden Jaw Force Fixture\AFG Evaluation\5mm AFG Electrical Schematic (EN8548)'  # Specify the directory containing your PDF files
output_file = 'combined.pdf'  # Specify the name of the output file
combine_pdfs(directory, output_file)  # Call the function to combine the PDFs
