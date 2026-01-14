import pdfplumber
import os

pdf_dir = "curiculum PDFS"
files_to_inspect = [
    "Year-7-Computing.pdf",
    "KS3 History.pdf",
    "English-Year-7-Curriculum-Sequence-2024.pdf"
]


with open("inspection_results.txt", "w", encoding="utf-8") as f:
    for filename in files_to_inspect:
        path = os.path.join(pdf_dir, filename)
        f.write(f"--- Inspecting {filename} ---\n")
        
        if not os.path.exists(path):
            f.write(f"File not found: {path}\n")
            continue

        try:
            with pdfplumber.open(path) as pdf:
                # Check the first few pages for tables
                for i, page in enumerate(pdf.pages[:3]): 
                    tables = page.extract_tables()
                    if tables:
                        f.write(f"Page {i+1}: Found {len(tables)} table(s)\n")
                        for j, table in enumerate(tables):
                            # Print the first non-empty row (likely headers)
                            for row in table:
                                # Filter out None or empty strings to see actual text
                                cleaned_row = [cell.replace('\n', ' ') if cell else 'None' for cell in row]
                                if any(cell != 'None' for cell in cleaned_row):
                                    f.write(f"  Table {j+1} Header Candidate: {cleaned_row}\n")
                                    break # Just show the first significant row
                    else:
                        f.write(f"Page {i+1}: No tables found\n")
        except Exception as e:
            f.write(f"Error reading {filename}: {e}\n")
        f.write("\n")
print("Done. Check inspection_results.txt")

