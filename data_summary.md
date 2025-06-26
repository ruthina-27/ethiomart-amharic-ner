# EthioMart Amharic E-commerce Data Project: Data Preparation & Labeling Summary

## 1. Data Collection

- **Source:**  
  Data was collected from multiple Ethiopian-based e-commerce Telegram channels, as listed in `channels_to_crawl.xlsx`.
- **Method:**  
  A custom Python scraper (`scripts/telegram_scraper.py`) was developed using the Telethon library. The scraper connects to Telegram using API credentials and downloads messages, images, and metadata (channel, sender, timestamp) from each channel.
- **Output:**  
  - Text and metadata are stored in `telegram_data.csv`.
  - Images are saved in the `photos/` directory.

---

## 2. Data Preprocessing

- **Cleaning:**  
  The raw messages are cleaned using `scripts/preprocess.py`. This script:
  - Removes non-Amharic characters and extraneous symbols.
  - Normalizes whitespace and Unicode.
  - Drops empty or irrelevant messages.
- **Structuring:**  
  The cleaned data is saved in `data/cleaned_data.csv` with columns for channel, clean text, views, date, and sender ID.
- **Rationale:**  
  Preprocessing ensures that only relevant Amharic text is used for downstream NER tasks, improving model performance.

---

## 3. Data Labeling

- **Labeling Format:**  
  A subset of messages is manually labeled in the CoNLL format, which is standard for NER tasks. Each token is assigned an entity label:
  - `B-Product`, `I-Product` for product names/types
  - `B-LOC`, `I-LOC` for locations
  - `B-PRICE`, `I-PRICE` for prices
  - `O` for tokens outside any entity
- **Process:**  
  - Labeled data is stored in `labeled_telegram_product_price_location.txt`.
  - The script `scripts/convert_to_conll.py` converts this to `labeled_data/ner_labels.conll` for model training.
- **Coverage:**  
  At least 30-50 messages are labeled, covering a variety of products, prices, and locations.

---

## 4. Data Quality & Challenges

- **Quality Control:**  
  - Manual review ensures correct entity boundaries and label consistency.
  - Ambiguous cases (e.g., mixed English/Amharic, abbreviations) are resolved by consensus or skipped.
- **Challenges:**  
  - Amharic tokenization is non-trivial due to script and morphology.
  - Some messages contain images or mixed content, which are currently labeled as `O` or skipped.

---

## 5. Next Steps

- Expand the labeled dataset for better model generalization.
- Incorporate more channels and message types.
- Begin model fine-tuning and evaluation (in progress).

---

**Instructions:**  
- Review and edit this summary as needed.  
- Export as PDF (using Word, Google Docs, or a Markdown-to-PDF tool).  
- Submit the PDF as part of your interim deliverables. 