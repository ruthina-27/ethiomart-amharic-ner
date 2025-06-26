# EthioMart Amharic E-commerce Data Extractor

## Overview
This project extracts and analyzes e-commerce data from Ethiopian Telegram channels, focusing on Amharic Named Entity Recognition (NER) for products, prices, and locations. The goal is to help EthioMart centralize and analyze vendor data for FinTech applications, such as loan candidate identification.

## Features
- Scrapes messages and media from multiple Telegram channels
- Preprocesses and cleans Amharic text
- Labels data in CoNLL format for NER
- Fine-tunes transformer models (XLM-Roberta, mBERT) for Amharic NER
- Compares models and interprets predictions with SHAP/LIME

## Project Structure
- `scripts/`: Data scraping, preprocessing, and conversion scripts
- `labeled_data/`: Labeled data in CoNLL format
- `notebooks/`: Model training and evaluation notebooks
- `models/`: Saved models
- `data/`, `raw_data/`, `photos/`: Data storage

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with Telegram API credentials:
   ```env
   TG_API_ID=your_api_id
   TG_API_HASH=your_api_hash
   PHONE_NUMBER=your_phone_number
   ```
4. Run the scraper:
   ```bash
   python scripts/telegram_scraper.py
   ```
5. Preprocess data:
   ```bash
   python scripts/preprocess.py
   ```
6. Convert labeled data to CoNLL:
   ```bash
   python scripts/convert_to_conll.py
   ```
7. Open and run the notebook for model training:
   ```
   notebooks/fine_tune_ner.ipynb
   ```

## Usage
- Update `channels_to_crawl.xlsx` with your target Telegram channels.
- Use the provided scripts to collect and preprocess data.
- Label a subset of messages in the required format.
- Fine-tune and evaluate NER models using the notebook.

## Contribution
Pull requests and issues are welcome! Please ensure your code is well-documented and tested.

## License
MIT License
