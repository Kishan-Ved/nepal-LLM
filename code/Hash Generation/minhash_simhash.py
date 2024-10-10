import os
import csv
from datasketch import MinHash
from simhash import Simhash
import re
import pandas as pd

generate_minhash = True
generate_simhash = False
block = 1 # Number of files after which hashes are written to CSV

def tokenize(text):
    return set(text.split())

def create_minhash(tokens, num_perm=128):
    m = MinHash(num_perm=num_perm)
    for token in tokens:
        m.update(token.encode('utf8'))
    return m

def create_simhash(text, num_perm=128):
    m = Simhash(text, f=num_perm)
    return m

# dataset_folder = "./kishan_data/good_data/good_texts_opinions3"
folder_path = "/Users/dj/NLP_Scraping/combined/misc/split_articles"

csv_file_path_minhash = "/Users/dj/NLP_Scraping/combined/misc/split_articles_minhash.csv"
csv_file_path_simhash = "/Users/dj/NLP_Scraping/combined/misc/split_articles_simhash.csv"


if generate_minhash:
	# Open CSV file to write the MinHash values
	with open(csv_file_path_minhash, mode='w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["filename", "minhash_values"])
	
if generate_simhash:
	# Open CSV file to write the simHash values
	with open(csv_file_path_simhash, mode='w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["filename", "simhash_values"])

min_hashes = []
sim_hashes = []

counter = 0

for filename in os.listdir(folder_path):
	if filename.endswith(".txt"):
		file_path = os.path.join(folder_path, filename)

		with open(file_path, 'r', encoding='utf-8') as file:
			text = file.read()
			tokens = tokenize(text)
			if generate_minhash:
				minhash = create_minhash(tokens)
				minhash_values = minhash.digest()
				min_hashes.append((filename, minhash_values))

			
			if generate_simhash:			
				simhash = create_simhash(text)
				sim_hashes.append((filename, simhash.value)) 
			
	if counter % block == 0 :
		if generate_minhash:
			df_minhash = pd.DataFrame(min_hashes)
			df_minhash.to_csv(csv_file_path_minhash,  mode='a', index=False, header=False)
			min_hashes = []
		
		if generate_simhash:
			df_simhash = pd.DataFrame(sim_hashes)
			df_simhash.to_csv(csv_file_path_simhash,  mode='a', index=False, header=False)
			sim_hashes = []
		
		counter = 0
		# print("added 10k files")

	counter += 1

