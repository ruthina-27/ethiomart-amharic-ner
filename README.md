# EthioMart Amharic E-commerce Data Extractor

## Overview
This project extracts and analyzes e-commerce data from Ethiopian Telegram channels, focusing on Amharic Named Entity Recognition (NER) for products, prices, and locations. The goal is to help EthioMart centralize and analyze vendor data for FinTech applications, such as loan candidate identification.

## Features
- Scrapes messages and media from multiple Telegram channels
- Preprocesses and cleans Amharic text
- Labels data in CoNLL format for NER
- Fine-tunes transformer models (XLM-Roberta, mBERT) for Amharic NER
- Compares models and interprets predictions with SHAP/LIME
- Generates a vendor scorecard for micro-lending analysis

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
3. (Optional) Set up your `.env` file with Telegram API credentials for scraping:
   ```env
   TG_API_ID=your_api_id
   TG_API_HASH=your_api_hash
   PHONE_NUMBER=your_phone_number
   ```

## Running the End-to-End Pipeline
All steps can be run from the notebook:
```
notebooks/end_to_end_pipeline.ipynb
```
This notebook covers:
- Data preprocessing
- NER dataset preparation
- Model fine-tuning (XLM-R, mBERT)
- Model evaluation and comparison
- Model interpretability (SHAP, LIME)
- Vendor scorecard generation and analysis

### To run the full pipeline:
1. Open `notebooks/end_to_end_pipeline.ipynb` in Jupyter or Colab.
2. Run each cell in order. All scripts and outputs are integrated.
3. For new data, rerun the preprocessing and vendor scorecard cells.

## Troubleshooting
- If you encounter missing dependencies, ensure you have run:
  ```bash
  pip install -r requirements.txt
  ```
- For best performance, use a machine with a GPU and the latest version of PyTorch.
- If you have issues with file paths, ensure you are running the notebook from the project root or adjust paths as needed.

## Contribution
Pull requests and issues are welcome! Please ensure your code is well-documented and tested.

## License
MIT License
