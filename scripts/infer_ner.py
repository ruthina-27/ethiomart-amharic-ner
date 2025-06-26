import sys
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import numpy as np

# Load model and tokenizer
MODEL_PATH = "./models/xlmr"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)

# Label mapping (update if needed)
label_list = list(model.config.id2label.values())


def predict_entities(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**tokens)
    predictions = torch.argmax(outputs.logits, dim=2)[0].numpy()
    input_ids = tokens["input_ids"][0].numpy()
    words = tokenizer.convert_ids_to_tokens(input_ids)
    entities = []
    for word, pred in zip(words, predictions):
        label = label_list[pred]
        if word not in ["[CLS]", "[SEP]", "<s>", "</s>", "[PAD]"]:
            entities.append((word, label))
    return entities


def main():
    if len(sys.argv) < 2:
        print("Usage: python infer_ner.py 'Your Amharic text here'")
        return
    text = sys.argv[1]
    entities = predict_entities(text)
    print("Predicted entities:")
    for word, label in entities:
        print(f"{word}: {label}")

if __name__ == "__main__":
    main() 