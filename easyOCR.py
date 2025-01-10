import easyocr
import pandas as pd
import os

def extract_table_easyocr(image_path, output_txt_path):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)
    
    # Read text from the image
    results = reader.readtext(image_path, detail=0)
    
    if not results:
        print("No text detected in the image. Please check the file.")
        return
    
    # Join the extracted text as raw output
    extracted_text = "\n".join(results)
    print("Extracted Text:", extracted_text)
    
    # Save raw extracted text to the text file
    try:
        os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)  # Create directory if not exists
        with open(output_txt_path, 'w') as file:
            file.write(extracted_text)
        print(f"Text successfully saved to {output_txt_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")
        return
    
    # Process data into a structured table
    rows = extracted_text.split("\n")
    
    # Split based on spaces or tabs; refine this according to your image structure
    data = []
    for row in rows:
        if row.strip():  # Skip empty rows
            data.append(row.split())  # Split by whitespace 
    
    # Create a DataFrame and handle any possible uneven columns
    df = pd.DataFrame(data)
    
    # Handle case where the DataFrame has inconsistent column sizes
    max_columns = max(df.apply(lambda x: len(x), axis=1))
    df = df.apply(lambda x: x.tolist() + [''] * (max_columns - len(x)), axis=1, result_type='expand')

    print("Tabular Data:")
    print(df)

    # Format the data into a structured text file format
    try:
        # Create formatted output for the text file
        with open(output_txt_path, 'w') as file:
            # Header with aligned columns
            for index, row in df.iterrows():
                formatted_row = " | ".join([str(cell).ljust(15) for cell in row])  # Adjust column width as necessary
                file.write(formatted_row + "\n")
        print(f"Tabular data successfully saved to {output_txt_path}")
    except Exception as e:
        print(f"Error saving tabular data to file: {e}")
        return

# Example usage
image_path = "easy-extract/images/brsr-pg.png"
output_txt_path = "easy-extract/outputs/extracted_text.txt"   
extract_table_easyocr(image_path, output_txt_path)
