import pandas as pd
import re
from pathlib import Path

# Use telegram_data.csv as input
input_file = "telegram_data.csv"
output_file = "data/cleaned_data.csv"

# Read the CSV, skip rows with missing Message
try:
    df = pd.read_csv(input_file)
except Exception as e:
    print(f"Error reading {input_file}: {e}")
    exit(1)

# Improved Amharic tokenization: split on whitespace and Amharic punctuation
def amharic_tokenize(text):
    if pd.isna(text):
        return ""
    # Keep Amharic, numbers, and common Amharic punctuation
    text = re.sub(r"[^\u1200-\u137F0-9፡።፣፤፥፦፧]+", " ", str(text))
    # Split on whitespace and Amharic punctuation
    tokens = re.split(r"[\s፡።፣፤፥፦፧]+", text)
    tokens = [t for t in tokens if t]
    return " ".join(tokens)

# Apply cleaning and tokenization
df["clean_text"] = df["Message"].apply(amharic_tokenize)

# Select relevant columns if they exist
cols = [c for c in ["Channel Title", "Channel Username", "clean_text", "Date", "Message ID", "Media Path"] if c in df.columns]
df = df[cols]
df = df.dropna(subset=["clean_text"])

Path("data").mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)
print(f"Preprocessed data saved to {output_file}")
