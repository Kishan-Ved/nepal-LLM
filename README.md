# IITGN CS 613: Natural Language Processing - Assignment 1
## Instructor: Prof. Mayank Singh
## Team 3: Nepali NLP
## Members:
- Aditya Mehta - 22110017
- Daksh Jain - 22110066
- Hrriday Ruparel - 22110099
- Kishan Ved - 22110122
- Sumeet Sawale - 22110234

## Overview

This project involves scraping article data, downloading large datasets, cleaning Nepali text files, and generating hashes for deduplication. The pipeline follows these steps: Scraping, Downloading, Cleaning, Hash Generation, and Deduplication.

## Dataset information
[Google Sheet](https://docs.google.com/spreadsheets/d/1-co_8irDi8RMbQBpmy0dVurucci2tkUEoINtMe1r544/edit?usp=sharing) containing information about datasets scrapped and downloaded

[HuggingFace](https://huggingface.co/Kishan-Ved/nepal-llm/tree/main) containing scrapped datasets that were collected and cleaned on local machines.

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


## **Individual Contributions**

### **Kishan**
- Scraped:
  - Feature articles from **Ekantipur**.
  - Opinions articles from **Ekantipur**.
  - Books from **Internet Archive**: Bhagavad Gita, Mahabharata, Ramayan, 3 Vedas, and 7 parts of Bhagwat Mahapuran.
  - Articles from **Online Khabar**.
- Developed code for:
  - Scraping **Ekantipur** and **Online Khabar** articles.
  - Generating **SimHash** for all text files.
  - Parallelizing scraping on the server for **Ekantipur** and **Online Khabar**.
  - Cleaning data by removing bad words and non-Nepali (Devanagari) symbols from all text files.
- Created a **Hugging Face repository** and uploaded the scraped files.

### **Hrriday**
- Scraped:
  - Blogs: **Ghumante**, **Mysansar**.
  - Literature articles: **Nai Academy**, **Shabd Sopan**, **Samakalin Sahitya**.
  - News articles: **Annapurna Post**, **Desh Sanchar**, **Dainik Nepal**, **DcNepal**, **Farakdhar**, **Makalu Khabar**, **Sagarmatha TV**, **Sahitya Post**.
- Developed a **BeautifulSoup + Requests** implementation for faster dataset curation compared to **Chromedriver**.
- Added functionality of **ThreadPoolExecutor** to all scripts for enhanced speed.

### **Sumeet**
- Scraped:
  - Articles from **Online Khabar** and **HimalKhabar**.
- Downloaded:
  - **CulturaX** dataset.
  - **English to Nepali translation** dataset.
- Developed code for:
  - Converting **Parquet files to CSV**.
  - Generating **MinHash** for deduplication.
  - Cleaning and generating hashes for the downloaded datasets.

### **Aditya**
- Scraped:
  - Poems from a website.
  - Examiner Data.
- Collected and verified **bad words** for the Nepali language with the help of a native speaker.
- Downloaded and cleaned **4 datasets** (50GB combined) from **Hugging Face**.
- Separated 2 of these datasets and generated **hashes** for them.
- Contact: **Sidharth** (+91 93457 66974).

### **Daksh**
- Scraped:
  - Articles from **News24Nepal**.
  - Data from **Nepal Wiki**.
- Cleaned and hashed both datasets.
- Downloaded:
  - **3 datasets** (AllenAI, Statmt, Oscar).
  - A large-scale Nepali text corpus dataset from **IEEE**, split it into individual files while maintaining semantics, cleaned, and hashed them.
- Developed code for parallelizing scraping using **ThreadPoolExecutor** for the listed tasks.
