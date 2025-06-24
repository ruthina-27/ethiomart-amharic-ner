def convert_to_conll(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            line = line.strip()
            if not line:
                outfile.write("\n")
                continue
            
            if "\t" in line:
                token, label = line.split("\t")
            elif " " in line:
                token, label = line.split(" ")
            else:
                continue
            
            outfile.write(f"{token} {label}\n")

if __name__ == "__main__":
    convert_to_conll("labeled_telegram_product_price_location.txt", "labeled_data/ner_labels.conll")
    print("Converted to CoNLL format.")
