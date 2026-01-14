import pdfplumber
import os
import json
import re

pdf_dir = "curiculum PDFS"
output_dir = "vocab_json"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def normalize_text(text):
    if text:
        return text.replace('\n', ' ').strip()
    return ""

def get_subject_from_filename(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Common subjects to looking for
    subjects = [
        "Art", "Computing", "Drama", "Design Technology", "Design & Technology", "Design and Technology", "DT",
        "English", "French", "Geography", "History", "Maths", "Mathematics", "Music",
        "PE", "Physical Education", "Personal Development", "RE", "Religious Education", 
        "Science", "Spanish"
    ]
    
    # Normalize filename for search
    norm_name = name.replace("-", " ").replace("_", " ").title()
    
    for subject in subjects:
        # distinct word match to avoid partials like 'Art' in 'Department' (unlikely but safe)
        if re.search(r'\b' + re.escape(subject) + r'\b', norm_name, re.IGNORECASE):
            # Normalize output name
            if subject in ["Design & Technology", "Design and Technology", "DT"]:
                return "Design Technology"
            if subject in ["Mathematics"]:
                return "Maths"
            if subject in ["Physical Education"]:
                return "PE"
            if subject in ["Religious Education"]:
                return "RE"
            return subject


            
    # Fallback: key parts of filename
    parts = norm_name.split()
    if parts:
        return parts[0]
    return "Unknown_Subject"

def extract_vocab_from_pdf(pdf_path, default_year=None):
    extracted_data = {7: [], 8: [], 9: []}
    current_year = default_year
    
    print(f"Processing: {os.path.basename(pdf_path)}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables:
                    continue
                
                for table in tables:
                    if not table:
                        continue
                        

                    # 1. Identify Headers
                    header_row_idx = -1
                    headers = []
                    
                    for idx, row in enumerate(table):
                        # clean row for checking
                        row_text = [normalize_text(cell).lower() for cell in row]
                        
                        # Check if this row *is* the header
                        if any("topic" in cell for cell in row_text) and any("vocab" in cell for cell in row_text):
                            header_row_idx = idx
                            headers = row_text
                            
                            # Check if the header itself contains the year (e.g. "Year 8" or just "8" in first col)
                            # Only if explicit default_year wasn't strict (i.e. KS3 file)
                            if not default_year: 
                                first_cell = row_text[0]
                                if "7" in first_cell or "year 7" in first_cell: current_year = 7
                                elif "8" in first_cell or "year 8" in first_cell: current_year = 8
                                elif "9" in first_cell or "year 9" in first_cell: current_year = 9
                            break
                    
                    if header_row_idx == -1:
                        # Maybe explicit headers aren't clear, skip table
                        continue
                        
                    # Identify column indices
                    topic_idx = -1
                    vocab_idx = -1
                    
                    for idx, h in enumerate(headers):
                        if "topic" in h:
                            topic_idx = idx
                        elif "vocab" in h:
                            vocab_idx = idx
                            
                    if topic_idx == -1 or vocab_idx == -1:
                        continue

                    # 2. Extract Data
                    for i in range(header_row_idx + 1, len(table)):
                        row = table[i]
                        if len(row) <= max(topic_idx, vocab_idx):
                            continue
                            
                        # Check Year indicator in first column
                        # Text might be "Year 7", "7", "Y7"
                        first_col_val = normalize_text(row[0]).lower()
                        
                        if "year 7" in first_col_val or (first_col_val.isdigit() and int(first_col_val) == 7):
                            current_year = 7
                        elif "year 8" in first_col_val or (first_col_val.isdigit() and int(first_col_val) == 8):
                            current_year = 8
                        elif "year 9" in first_col_val or (first_col_val.isdigit() and int(first_col_val) == 9):
                            current_year = 9
                        
                        # If we don't know the year yet and can't find it, skip
                        target_year = current_year
                        if not target_year:
                            continue
                            
                        if target_year not in extracted_data:
                            continue

                        term_val = "" 
                        topic_val = normalize_text(row[topic_idx])
                        
                        # Get raw vocab to preserve newlines which are crucial separators
                        vocab_raw = row[vocab_idx]
                        
                        # Clean vocab list
                        if not vocab_raw or vocab_raw.lower() == "none":
                            continue
                            
                        # 1. Pre-clean: Remove content in brackets (explanations)
                        vocab_raw = re.sub(r'\(.*?\)', '', vocab_raw)

                        # 2. Split keys by comma, newline, slash, ampersand, or ' and ' / ' or '
                        tokens = re.split(r'[,\n/\\&+]|\s+and\s+|\s+or\s+', vocab_raw)
                        
                        vocab_list = []
                        for t in tokens:
                            # 3. Clean individual token
                            t = t.strip().strip('.,:;-"\'')
                            
                            # Skip if empty or too short
                            if len(t) < 2: 
                                continue
                                
                            # Skip if explicit header trash
                            if "tier 3 words" in t.lower():
                                continue
                                
                            # 4. Capitalize first letter
                            t = t[0].upper() + t[1:]
                            
                            vocab_list.append(t)
                        
                        # Avoid duplicates
                        vocab_list = list(dict.fromkeys(vocab_list))

                        if (topic_val and len(topic_val) > 2 and "key topics" not in topic_val.lower()) or vocab_list:
                            extracted_data[target_year].append({
                                "Term": term_val, 
                                "Topic": topic_val,
                                "KeyVocab": vocab_list
                            })
                            
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
        
    return extracted_data


def main():
    files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    
    # Organize by subject to merge results (e.g. KS3 file might have year 7, 8, 9 for history)
    subject_db = {} 
    
    for filename in files:
        subject = get_subject_from_filename(filename)
        path = os.path.join(pdf_dir, filename)
        
        # Determine default year from filename if possible
        default_year = None
        if "year-7" in filename.lower() or "year 7" in filename.lower():
            default_year = 7
        elif "year-8" in filename.lower() or "year 8" in filename.lower():
            default_year = 8
        elif "year-9" in filename.lower() or "year 9" in filename.lower():
            default_year = 9
            
        # extract
        data = extract_vocab_from_pdf(path, default_year)
        
        if subject not in subject_db:
            subject_db[subject] = {7: [], 8: [], 9: []}
            
        # Merge
        for year in [7, 8, 9]:
            if data[year]:
                subject_db[subject][year].extend(data[year])

    # Write JSON files
    for subject, years_data in subject_db.items():
        # Construct user requested format
        # { "Subject": ... "Years": [ { "Year": 7, "Topics": [...] } ] }
        
        final_struct = {
            "Subject": subject,
            "Years": []
        }
        
        curr_has_data = False
        for year in [7, 8, 9]:
            if years_data[year]:
                curr_has_data = True
                final_struct["Years"].append({
                    "Year": year,
                    "Topics": years_data[year]
                })
        
        if curr_has_data:
            out_file = os.path.join(output_dir, f"{subject}.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(final_struct, f, indent=2, ensure_ascii=False)
            print(f"Created {out_file}")

if __name__ == "__main__":
    main()
