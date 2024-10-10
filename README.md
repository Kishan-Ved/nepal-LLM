# IITGN CS 613: Natural Language Processing - Assignment 1
## Instructor: Prof. Mayank Singh
## Team 3: Nepali NLP
## Members:
- Aditya Mehta - 22110017
- Daksh Jain - 22110066
- Hrriday Ruparel - 22110099
- Kishan Ved - 22110122
- Sumeet Sawale - 22110234

> Huggingface repo for datasets scraped locally for Assignment 1 [HuggingFace Link](https://huggingface.co/Kishan-Ved/nepal-llm/tree/main).

# Web Scraping, Downloading, and Cleaning Pipeline

## Overview

This project involves scraping article data, downloading large datasets, cleaning Nepali text files, and generating hashes for deduplication. The pipeline follows these steps: Scraping, Downloading, Cleaning, Hash Generation, and Deduplication.

## Pipeline

### 1. Scraping

- Scraped a webpage containing only links to various articles.
- Collected all links and stored them in a CSV file.
- Iterated over the CSV file and opened each link (webpage) using `webdriver` / `BeautifulSoup`.
- Scraped each webpage and extracted Nepali data present in `<p>` tags inside specific `<div>` tags.
- Created a `.txt` file for every webpage.

### 2. Downloading

- Downloaded datasets, most of which were in parquet format.
- Used a Python script (`pandas`) to convert parquet files into text files.
- Separated the text files into individual article texts using unique identifiers or line breaks.
- Cleaned the files for bad word removal and non-Devanagari character removal.
- Used pandas `ctext` techniques to convert CSV articles into text files.

### 3. Cleaning

- Collected a list of bad words from various online sources.
- Translated English bad words into Nepali using translation libraries.
- Cross-verified the bad word list with a native Nepali speaker, Sidharth (+91 93457 66974), for accuracy.
- Saved the final list in the `Nepali_Bad_Words.txt` file.
- Iterated over all `.txt` files in the given folder:
  - If bad word(s) were present (as per the `Nepali_Bad_Words.txt` file), the file was moved to the `bad_texts` folder.
  - If no bad words were found, all non-Devanagari characters, except for whitespaces and some punctuation marks, were removed.
  - The cleaned text was written to a new `.txt` file in the `good_texts` folder.

### 4. Hash Generation

- For each `.txt` file scraped or downloaded, two hash values (MinHash and SimHash) were generated to assist with deduplication tasks.
  - **MinHash**: Uses 128 hash functions to generate 128 hash values and compute the Jaccard distance between two documents.
  - **SimHash**: A 128-bit hash for each `.txt` file.
  
- For very large datasets containing only a single document, hash generation was skipped as they couldn't be meaningfully separated into smaller documents.

### 5. Deduplication

- Distance Metrics:
  - **Jaccard distance (MinHash)**: Lower the value, higher the similarity.
  - **Hamming distance (SimHash)**: Lower the value, higher the similarity.
  
- **LSH (Locality-Sensitive Hashing)** was used to compare hash values for deduplication.
