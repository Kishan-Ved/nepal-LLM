import os
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define directories
content_folder = './news/content/'
input_folder = os.path.join(content_folder, 'desh_sanchar')  # Folder containing text files to scan
bad_folder = os.path.join(content_folder, 'desh_sanchar_bad')
good_folder = os.path.join(content_folder, 'desh_sanchar_good')

# Create directories if they don't exist
os.makedirs(bad_folder, exist_ok=True)
os.makedirs(good_folder, exist_ok=True)

# Load bad words from file
with open('./Nepali_Bad_Words.txt', 'r', encoding='utf-8') as f:
    bad_words = set(line.strip().lower() for line in f)

# Function to check if a file contains any bad words
def contains_bad_words(content):
    content = content.lower()  # Case-insensitive matching
    for word in bad_words:
        if word in content:
            return True
    return False

# Function to remove all non-Devanagari characters from content
def remove_non_devanagari(content):
    devanagari_pattern = re.compile(r'[ऀ-ॿ\s।॥,.?!\n:;()]+')
    cleaned_content = ' '.join(devanagari_pattern.findall(content))
    return cleaned_content

# Function to process a single file
def process_file(filename):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for bad words and move the file accordingly
        if contains_bad_words(content):
            shutil.copy(file_path, os.path.join(bad_folder, filename))
        else:
            # Remove non-Devanagari characters and save to the good folder
            cleaned_content = remove_non_devanagari(content)
            new_file_path = os.path.join(good_folder, filename)
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

# Use ThreadPoolExecutor to process files concurrently
def process_files_concurrently():
    filenames = sorted(os.listdir(input_folder), key=lambda x: int(x.split('.')[0]))
    total = len(filenames)
    processed_count = 0
    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = []
        for i in range(len(filenames)):
            futures.append(executor.submit(process_file, filenames[i]))
        for future in as_completed(futures):
            try:
                success = future.result()
                processed_count += 1
                if processed_count % 1000 == 0:
                    print(f"Processed: {processed_count}/{total} files")
            except Exception as e:
                print(f"An error occurred while processing file: {e}")

if __name__ == "__main__":
    process_files_concurrently()
    print("Cleaning done.")                