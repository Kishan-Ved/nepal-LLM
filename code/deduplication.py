import os
import csv
from datasketch import MinHash, MinHashLSH
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast

# Function to convert a list of hash values back into a MinHash object
def create_minhash_from_values(minhash_values, num_perm=128):
    m = MinHash(num_perm=num_perm)
    m.digest(minhash_values)
    return m

# Function to compute Jaccard similarity between two MinHash objects
def compute_jaccard_similarity(m1, m2):
    return m1.jaccard(m2)

# Function to process a single file for LSH query and duplication detection
def process_file(file_key, minhash_values, lsh, file_paths, duplicates_info):
    minhash = create_minhash_from_values(minhash_values)
    
    # Query LSH for similar files
    similar_files = lsh.query(minhash)
    
    # If duplicates are found (more than one similar file), calculate similarity
    if len(similar_files) > 1:
        for other_file in similar_files[1:]:  # Compare with other similar files
            other_minhash_values = file_paths[other_file]
            other_minhash = create_minhash_from_values(other_minhash_values)
            
            # Compute Jaccard similarity
            similarity = compute_jaccard_similarity(minhash, other_minhash)
            
            # Log duplicate info
            duplicates_info.append((file_key, other_file, similarity))

# Folder path where CSV files are stored (the base folder containing doc1, doc2, ...)
base_folder_path = "mnt/HDFS1/language_nlp/nepali_nlp_team_3/hashes"

# Initialize LSH for duplicate detection
lsh = MinHashLSH(threshold=0.5, num_perm=128)  # Set your desired threshold

# Store file paths for checking duplicates
file_paths = {}

# Loop over each folder to load the CSV and insert MinHashes into LSH
for csv_file_path in os.listdir(base_folder_path):

    if csv_file_path.ends_with('.csv') :
        dataset = str(csv_file_path).split('_')[0]

        # Read the CSV and insert MinHashes into LSH
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                filename = row['filename']
                minhash_values = ast.literal_eval(row['minhash_values'])  # Safely convert string back to list of integers
                
                # Create MinHash object from values
                minhash = create_minhash_from_values(minhash_values)
                
                # Insert MinHash into LSH with file path as the key
                file_key = os.path.join(dataset, filename)
                lsh.insert(file_key, minhash)
                file_paths[file_key] = minhash_values

# Shared list to store duplicates information across threads
duplicates_info = []

# Use ThreadPoolExecutor to parallelize the duplicate detection
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    
    # Schedule tasks for each file to check for duplicates
    for file_key, minhash_values in file_paths.items():
        futures.append(executor.submit(process_file, file_key, minhash_values, lsh, file_paths, duplicates_info))
    
    # Wait for all threads to complete
    for future in as_completed(futures):
        try:
            future.result()  # Retrieve the result (if needed)
        except Exception as exc:
            print(f"Error during processing: {exc}")

# Write the duplicates information to a CSV file
duplicates_csv_path = os.path.join(base_folder_path, "duplicates.csv")
with open(duplicates_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["file1", "file2", "similarity_value"])
    
    # Write each pair of duplicates and their similarity
    for file1, file2, similarity in duplicates_info:
        writer.writerow([file1, file2, similarity])

print("Duplicate information stored in duplicates.csv.")