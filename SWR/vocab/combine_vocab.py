import json
import os

input_dir = "vocab_json"
output_file = "all_curriculum.json"

combined_data = {}

print("Combining JSON files...")

if os.path.exists(input_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".json") and filename != output_file:
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # specific check for the structure we created
                    subject_name = data.get("Subject")
                    if subject_name:
                        combined_data[subject_name] = data
                    else:
                        # Fallback to filename if Subject key missing (shouldn't happen with our script)
                        name = os.path.splitext(filename)[0]
                        combined_data[name] = data
                        
                    print(f"Added {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Write combined file
    # Structure: { "Art": { "Subject": "Art", "Years": [...] }, ... }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created {output_file} with {len(combined_data)} subjects.")
else:
    print(f"Directory {input_dir} not found.")
