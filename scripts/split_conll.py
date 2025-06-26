import sys

# Usage: python split_conll.py input_file output_prefix messages_per_file

def split_conll(input_file, output_prefix, messages_per_file=1000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        message = []
        file_count = 1
        msg_count = 0
        out = open(f"{output_prefix}_{file_count}.conll", 'w', encoding='utf-8')
        for line in infile:
            if line.strip() == '':
                if message:
                    out.write('\n'.join(message) + '\n\n')
                    message = []
                    msg_count += 1
                    if msg_count >= messages_per_file:
                        out.close()
                        file_count += 1
                        out = open(f"{output_prefix}_{file_count}.conll", 'w', encoding='utf-8')
                        msg_count = 0
            else:
                message.append(line.strip())
        # Write any remaining messages
        if message:
            out.write('\n'.join(message) + '\n')
        out.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_conll.py input_file output_prefix [messages_per_file]")
    else:
        input_file = sys.argv[1]
        output_prefix = sys.argv[2]
        messages_per_file = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
        split_conll(input_file, output_prefix, messages_per_file) 