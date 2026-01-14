import os
import urllib.request
import urllib.error
import time

base_url = "https://swr.gloucs.sch.uk/wp-content/uploads/2024/03/"
output_dir = "found_pdfs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

years = [7, 8, 9, 10, 11]
subjects = [
    "Art", "Computing", "Drama", "Design Technology", "English",
    "French", "Geography", "History", "Maths", "PE",
    "Personal Development", "RE", "Science", "Spanish"
]

files_to_check = []

# 1. Generate Year-based filenames
for year in years:
    for subject in subjects:
        safe_subject = subject.replace(" ", "-")
        files_to_check.append(f"Year-{year}-{safe_subject}.pdf")

# 2. Generate KS3 filenames
for subject in subjects:
    safe_subject = subject.replace(" ", "-")
    files_to_check.append(f"KS3-{safe_subject}.pdf")
    files_to_check.append(f"Key-Stage-3-{safe_subject}.pdf") 

print(f"Checking {len(files_to_check)} potential file URLs...")

found_count = 0
new_download_count = 0

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for filename in files_to_check:
    dest_path = os.path.join(output_dir, filename)
    
    # Skip if we already have it (optional, but good for speed)
    if os.path.exists(dest_path):
        print(f"[EXISTS] {filename}")
        found_count += 1
        continue

    url = base_url + filename
    try:
        req = urllib.request.Request(url, method='GET', headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f"[FOUND & DOWNLOADING] {filename}")
                with open(dest_path, 'wb') as f:
                    f.write(response.read())
                found_count += 1
                new_download_count += 1
    except urllib.error.HTTPError:
        # file not found on server
        pass
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")

    time.sleep(0.1)

print("-" * 20)
print(f"Total Files in '{output_dir}': {found_count}")
print(f"Newly Downloaded: {new_download_count}")
