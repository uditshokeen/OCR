import io
from PIL import Image
import pytesseract
import re

# Set the Tesseract executable path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def parse_table(table_text):
    """
    Parse the extracted table text into headers and rows.
    """
    try:
        # Split the table text into lines
        lines = table_text.strip().split('\n')

        # Extract headers from the first line
        headers = lines[0].split()

        # Extract data rows
        data = []
        for line in lines[1:]:
            row = line.split()
            # Ensure row has the same number of elements as headers
            if len(row) >= len(headers):
                data.append(row)

        return headers, data
    except Exception as e:
        print(f"Error while parsing table: {e}")
        return [], []


def extract_paragraph_or_table(text, heading):
    """
    Extract a paragraph or table based on a heading.
    """
    try:
        # Find the heading's position
        heading_pattern = rf"{heading}"
        match = re.search(heading_pattern, text, re.IGNORECASE)
        if match:
            start_idx = match.end()  # Start extracting after the heading
            # Extract until the next blank line or end of text
            remaining_text = text[start_idx:].strip()
            # Paragraph ends where there's a double newline
            end_idx = remaining_text.find("\n\n")
            paragraph = remaining_text[:end_idx] if end_idx != -1 else remaining_text
            return paragraph.strip()
        return "Heading not found."
    except Exception as e:
        print(f"Error while extracting paragraph or table: {e}")
        return "An error occurred."


def save_to_file(file_path, content):
    """
    Save content to a text file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(content)
    except Exception as e:
        print(f"Error saving to file: {e}")


# Main Execution
try:
    # Open the image for OCR
    img_path = r"C:/og/ocr/extraction/easy-extract/images/Bank-Statement-img.jpg"
    img = Image.open(img_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(img)

    # Save the full extracted text to a files
    output_txt_file = "C:/og/ocr/extraction/easy-extract/outputs/Bank-Statement.txt"
    save_to_file(output_txt_file, "Extracted Text from Image:\n" + text)

    print("Extracted Text has been saved to the file.")

    # Extract the table using a regular expression
    table_pattern = r'Parameter\s+Unit\s+FY\s*2023-24.*?(?=\n\n)'  # Adjust regex as per the table format
    table_match = re.search(table_pattern, text, re.DOTALL)
    if table_match:
        table_text = table_match.group(0)
        headers, data = parse_table(table_text)

        # Print the parsed table
        print("\nExtracted Table:")
        print(" | ".join(headers))  # Print headers
        for row in data:
            print(" | ".join(row))  # Print rows

    else:
        print("No table found matching the pattern.")

    # Allow the user to specify a heading to extract paragraphs or sections
    while True:
        heading = input("\nEnter the table/paragraph heading to extract (or type 'exit' to quit): ")
        if heading.lower() == 'exit':
            break

        # Extract and print the content
        content = extract_paragraph_or_table(text, heading)
        if content and content != "Heading not found.":
            print(f"\n--- Content for Heading '{heading}' ---\n")
            print(content)
        else:
            print(f"No content found for heading '{heading}'.")

except FileNotFoundError:
    print(f"Error: The file '{img_path}' was not found. Please check the file path.")
except pytesseract.TesseractNotFoundError:
    print("Error: Tesseract is not installed or the path is not set.")
except Exception as e:
    print(f"An error occurred: {e}")
