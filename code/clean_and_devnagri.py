import os
import shutil
import re

# Define directories
input_folder = '/Users/dj/NLP_Scraping/combined/misc/split_articles'  # Folder containing text files to scan
bad_folder = '/Users/dj/NLP_Scraping/combined/misc/split_articles/bad'
good_folder = '/Users/dj/NLP_Scraping/combined/misc/split_articles/good'

# Create directories if they don't exist
os.makedirs(bad_folder, exist_ok=True)
os.makedirs(good_folder, exist_ok=True)

# Load bad words from file
with open('/Users/dj/NLP_Scraping/Nepali_Bad_Words.txt', 'r', encoding='utf-8') as f:
    bad_words = set(line.strip().lower() for line in f)

# Function to check if a file contains any bad words
def contains_bad_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()  # Read and convert to lowercase for case-insensitive matching
        for word in bad_words:
            if word in content:
                print(file_path, word)
                return True
    return False

# Function to remove all non-Devanagari characters from content
def remove_non_devanagari(content):
    # Keep only characters in Devanagari Unicode range (U+0900 to U+097F)
    devanagari_pattern = re.compile(r'[ऀ-ॿ\s।॥,.?!\n:;()]+')
    cleaned_content = ''.join(devanagari_pattern.findall(content))
    return cleaned_content

# Process each file in the input folder
for filename in os.listdir(input_folder): 
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)
        
        # Check for bad words and copy the file accordingly
        if contains_bad_words(file_path):
            # Copy file to bad_texts_features folder
            shutil.copy(file_path, os.path.join(bad_folder, filename))
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove non-Nepali Devanagari characters
            cleaned_content = remove_non_devanagari(content)
            
            # Save the cleaned content to the good_texts_features folder
            new_file_path = os.path.join(good_folder, filename)
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

print("Processing and cleaning done.")
