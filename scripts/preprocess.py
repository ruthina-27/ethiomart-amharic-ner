import pandas as pd
import re
from pathlib import Path

df = pd.read_csv("data/raw_data/messages.csv")

def clean_amharic_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"[^\u1200-\u137F0-9፡።፣፤፥፦፧]+", " ", text)  # keep Amharic + numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_amharic_text)
df = df[["channel", "clean_text", "views", "date", "sender_id"]]
df = df.dropna(subset=["clean_text"])

Path("data").mkdir(parents=True, exist_ok=True)
df.to_csv("data/cleaned_data.csv", index=False)
