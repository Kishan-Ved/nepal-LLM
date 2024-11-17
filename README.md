# CS 613: NLP - Assignment 2  
**Tokenizer & Model Training**  
**Total Marks: 100 Pts**  
**November 17, 2024**


## [Report Link](https://github.com/Kishan-Ved/nepal-LLM/blob/tokenization_pre_train/Tokenization_and_Pre_Training_report.pdf)

## [Prompts and Generated Text Link](https://github.com/Kishan-Ved/nepal-LLM/blob/tokenization_pre_train/Prompts_and_Generated_Text.pdf)

## Problem Statement

### Task 1: Tokenizer Training

#### 1.1 Tokenizer Training

**Dataset Samples Description:**  
The curated scrapped data by all the team members was used to train the tokenizer. The dataset was called `all_final_dataset`. A random sampling from this dataset (with a fixed seed) was used to make datasets of fixed sizes. Additionally, a dataset containing only news articles was compiled called `all_news_dataset`, along with standalone datasets like Sangrah and Nepali Deva, as they were substantial in size on their own.

- Dataset Sample 1: `all_final_dataset` (200 MB)
- Dataset Sample 2: `all_final_dataset` (350 MB)
- Dataset Sample 3: `all_final_dataset` (500 MB)
- Dataset Sample 4: `all_final_dataset` (750 MB)
- Dataset Sample 5: `all_final_dataset` (1 GB)
- Dataset Sample 6: `all_news_scrapped` (350 MB)
- Dataset Sample 7: `Sangrah` (750 MB)
- Dataset Sample 8: `Nepali_Deva` (1.2 GB)

**Tokenizer Details:**  

| Tokenizer | Algorithm   | Vocab Size | Dataset Information                      |
|-----------|-------------|------------|-------------------------------------------|
| Tokenizer 1 | sentencePiece | 49,152 | `all_final_dataset` (200 MB) |
| Tokenizer 2 | sentencePiece | 49,152 | `all_final_dataset` (350 MB) |
| Tokenizer 3 | sentencePiece | 49,152 | `all_final_dataset` (500 MB) |
| Tokenizer 4 | sentencePiece | 49,152 | `all_final_dataset` (750 MB) |
| Tokenizer 5 | sentencePiece | 49,152 | `all_final_dataset` (1 GB) |
| Tokenizer 6 | sentencePiece | 49,152 | `all_news_scrapped` (350 MB) |
| Tokenizer 7 | sentencePiece | 50,000 | `Sangrah` (750 MB) |

#### 1.2 Fertility Score Calculation

**Methodology:**  
Fertility scores were calculated for the trained tokenizers on both their respective training datasets and a held-out dataset (`all_news_scrapped`).

---

**Results when tested on the same dataset it was trained on:**

| Tokenizer | Fertility Score | Dataset Info (Train) | Dataset Info (Test) |
|-----------|-----------------|----------------------|---------------------|
| Tokenizer 1 | 1.2911565101 | `all_final_dataset` (200 MB) | `all_final_dataset` (200 MB) |
| Tokenizer 2 | 1.2952214366 | `all_final_dataset` (350 MB) | `all_final_dataset` (350 MB) |
| Tokenizer 3 | 1.2952510265 | `all_final_dataset` (500 MB) | `all_final_dataset` (500 MB) |
| Tokenizer 4 | 1.2964268691 | `all_final_dataset` (750 MB) | `all_final_dataset` (750 MB) |
| Tokenizer 5 | 1.2960094995 | `all_final_dataset` (1 GB) | `all_final_dataset` (1 GB) |
| Tokenizer 7 | 1.2469413133 | `Sangrah` (200 MB) | `Sangrah` (200 MB) |

**Results when tested on a fixed held-out dataset (`all_news_scrapped`):**

| Tokenizer | Fertility Score | Dataset Info (Train) | Dataset Info (Test) |
|-----------|-----------------|----------------------|---------------------|
| Tokenizer 1 | 1.2529094399 | `all_final_dataset` (200 MB) | `all_news_scrapped` (350 MB) |
| Tokenizer 2 | 1.2515642463 | `all_final_dataset` (350 MB) | `all_news_scrapped` (350 MB) |
| Tokenizer 3 | 1.2509406335 | `all_final_dataset` (500 MB) | `all_news_scrapped` (350 MB) |
| Tokenizer 4 | 1.2504782866 | `all_final_dataset` (750 MB) | `all_news_scrapped` (350 MB) |
| Tokenizer 5 | 1.2515644638 | `all_final_dataset` (1 GB) | `all_news_scrapped` (350 MB) |

## Task 2: Model Training

### 2.1 Model Selection

**Model Architecture Chosen:**  
The architecture chosen is **LLaMAForCausalLM**, which is based on the transformer architecture optimized for causal language modeling tasks. It employs a multi-head self-attention mechanism with rotary embeddings, RMS normalization, and an efficient feed-forward network.

**Adjustments Made:**  
To reduce the total number of parameters to below 100M, the following modifications were made:

- Reduced the `hidden_size` to **512** (compared to higher defaults in larger models).
- Set the number of attention heads to **8** with a head dimension of **64**.
- Kept **16 layers** in the model (`num_hidden_layers`).
- Set `intermediate_size` to **1024**, balancing the computational load in the feed-forward layers.
- Used a vocabulary size of **50,000**, optimized for the dataset size.
- Excluded additional biases in feed-forward layers (`mlp_bias: false`) to reduce parameters.

**Total Parameters:**  
The final model has approximately **86M parameters**, which is within the 100M constraint.

### 2.2 Tokenization of Dataset

**Best Tokenizer Chosen:** The tokenizer 7 (trained on Sangrah (750 MB)) was chosen for the model training.

**Reason for Choice:**  
It had a perplexity of around **1.2469413133**, which was the lowest among all the tokenizers trained on different datasets. Thus, we chose it as the best tokenizer for the model training.

### 2.3 Model Training

**Training Details:**

- Number of Epochs: **10**
- Batch Size: **8**

**Perplexity Results per Epoch:**

The following table shows the training loss, validation loss, and perplexity at various steps during model training. Every 500 steps corresponds to 0.1 epoch.

| **Steps** | **Training Loss** | **Validation Loss** | **Perplexity** |
|-----------|-------------------|---------------------|----------------|
| 500       | 7.918729          | 7.703134            | 2102.312241    |
| 1000      | 7.529400          | 7.505957            | 1818.844430    |
| 1500      | 7.207300          | 7.229811            | 1437.476760    |
| 2000      | 6.884200          | 6.893766            | 986.108044     |
| 2500      | 6.688900          | 6.741419            | 838.426617     |
| 3000      | 6.493600          | 6.508142            | 670.579000     |
| 3500      | 6.371900          | 6.391015            | 591.100484     |
| 4000      | 6.250200          | 6.223870            | 504.652362     |
| 4500      | 6.111200          | 6.113407            | 451.556748     |
| 5000      | 5.971700          | 6.002983            | 404.633863     |
| 5500      | 5.877500          | 5.910859            | 366.748795     |
| 6000      | 5.783300          | 5.816735            | 335.873564     |
| 6500      | 5.687900          | 5.723983            | 310.632056     |
| 7000      | 5.630000          | 5.672997            | 290.905210     |
| 7500      | 5.577500          | 5.599084            | 274.989125     |
| 8000      | 5.524400          | 5.547181            | 256.513335     |
| 8500      | 5.469400          | 5.487976            | 241.756643     |
| 9000      | 5.444300          | 5.444356            | 231.448171     |
| 9500      | 5.385400          | 5.398842            | 222.632577     |
| 10000     | 5.327800          | 5.347515            | 210.085508     |
| 10500     | 5.276100          | 5.306705            | 202.228561     |
| 11000     | 5.227900          | 5.265094            | 193.464456     |
| 11500     | 5.157300          | 5.214261            | 188.233344     |
| 12000     | 5.184900          | 5.194471            | 180.272732     |
| 12500     | 5.113100          | 5.126363            | 173.604526     |
| 13000     | 5.041700          | 5.132655            | 169.466479     |
| 13500     | 5.028200          | 5.092561            | 163.415618     |
| 14000     | 5.021400          | 5.080809            | 160.904193     |
| 14500     | 5.015000          | 5.068379            | 157.665767     |
| 15000     | 5.016100          | 5.031531            | 153.167311     |
| 15500     | 4.993000          | 5.009063            | 149.152026     |
| 16000     | 4.924900          | 4.986255            | 146.387131     |
| 16500     | 4.890000          | 4.967847            | 142.557062     |
| 17000     | 4.855600          | 4.947319            | 140.796985     |
| 17500     | 4.850000          | 4.915397            | 137.633544     |
| 18000     | 4.834600          | 4.908449            | 135.429160     |
| 18500     | 4.832000          | 4.885120            | 133.049802     |
| 19000     | 4.840000          | 4.873579            | 130.788174     |
| 19500     | 4.774500          | 4.853282            | 128.125492     |
| 20000     | **4.688000**      | **4.849658**        | **127.696651**  |


## Testing Prompts & Outputs

As Markdown does not support Devanagari characters, all the prompts and generated texts are documented in the Google Doc file linked here: **[Link to Google Doc](https://docs.google.com/document/d/1OlPw7KpUDN4s5xKAvibZpJCs9EnnND2bKnRrVHyNlEQ/edit?usp=sharing)**

### 2.5 Other Trained Models

The best-trained model was chosen for the final submission. Below are the details of the other models that were trained:

- **Nepali LLM Version 1:**
  - **Trained on:** `all_final_dataset` (500 MB)
  - **Model Architecture:** LlamaForCausalLM
  - **Parameters:** 86.000128 Million
  - **Tokenizer Used:** Tokenizer 4 (trained on `all_final_dataset` (750 MB))
  - **Perplexity:** 4000
  - **Epochs:** 10
  - **Training Split:** 80:20

- **Nepali LLM Version 2:**
  - **Trained on:** `all_final_dataset` (200 MB)
  - **Model Architecture:** LlamaForCausalLM
  - **Parameters:** 86.000128 Million
  - **Tokenizer Used:** Tokenizer 4 (trained on `all_final_dataset` (750 MB))
  - **Perplexity:** 171
  - **Epochs:** 10
  - **Training Split:** 90:10

---

## References

- [Thakur, Aamod. NLP Pre-Training. GitHub](https://github.com/AamodThakur/NLP_Pre_Training)

---

## Work Distribution

- **Aditya Mehta (Roll Number: 22110017)**
  - Tokenized the `all_news_scrapped` dataset and identified duplicates with other datasets.
  - Worked on the tokenization process of the `Nepali_Deva` text corpus.
  - Prepared the entire report.

- **Daksh Jain (Roll Number: 22110066)**
  - Tokenized a Nepali Wikipedia-scraped dataset and evaluated fertility scores to determine the best tokenization strategy.
  - Tested scalability by tokenizing datasets of various sizes.
  - Ran prompt tests on the final model to validate its performance.

- **Hrriday Ruparel (Roll Number: 22110099)**
  - Wrote scripts for dataset merging, tokenization, and model training.
  - Trained tokenizers on the scraped dataset.
  - Trained an 80M model on the scraped dataset.

- **Kishan Ved (Roll Number: 22110122)**
  - Trained five different tokenizers and identified the one with the best fertility score.
  - Trained an 86M parameter model on the scraped dataset.
  - Trained a tokenizer on the Sangrah dataset and tokenized it.
  - Trained an 86M parameter model on the Sangrah dataset.

- **Summet Sawale (Roll Number: 22110234)**
  - Assisted in writing code for tokenizing text into tensors of context length.
  - Tested models using prompts.
  - Documented testing results.
  - Downloaded the scraped data from the server.
