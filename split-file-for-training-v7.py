import argparse
from transformers import LlamaTokenizer
import json
from tqdm import tqdm

def tokenize_and_chunk(text, tokenizer, block_size, min_tokens, pbar, carry_over):
    tokens = tokenizer(text, truncation=False)['input_ids']
    chunks = []
    
    if carry_over:
        current_chunk = tokenizer(carry_over, truncation=False)['input_ids']
    else:
        current_chunk = []
        
    # Remove any <s> tokens from the beginning of the current chunk
    current_chunk = [token for token in current_chunk if tokenizer.decode([token]).strip() != '<s>' or tokenizer.decode([token]).strip() != '</s>' ]
    
    current_token_count = len(current_chunk)
    small_chunks = []
    
    for token in tokens:
        current_chunk.append(token)
        current_token_count += 1
        decoded_token = tokenizer.decode([token]).strip()
        
        if decoded_token == '.' and current_token_count >= min_tokens:
            decoded_text = tokenizer.decode(current_chunk).strip()
            chunks.append(decoded_text)
            current_chunk = []
            current_token_count = 0
            
        elif current_token_count >= block_size:
            for i in range(len(current_chunk) - 1, -1, -1):
                if tokenizer.decode([current_chunk[i]]).strip() == '.':
                    decoded_text = tokenizer.decode(current_chunk[:i+1]).strip()
                    if len(current_chunk[:i+1]) < min_tokens:
                        small_chunks.append(decoded_text)
                    chunks.append(decoded_text)
                    current_chunk = current_chunk[i+1:]
                    current_token_count = len(current_chunk)
                    break
        pbar.update(1)
        
    carry_over = tokenizer.decode(current_chunk).strip()
    return chunks, carry_over, small_chunks

def tokenize_and_save(filename, output_filename, tokenizer, block_size, min_tokens):
    all_chunks = []
    small_chunks = []
    carry_over = ""
    
    total_tokens = 0
    with open(filename, 'r') as f:
        for line in f:
            total_tokens += len(tokenizer(line, truncation=False)['input_ids'])
            
    with tqdm(total=total_tokens) as pbar:
        with open(filename, 'r') as f:
            text_parts = f.readlines()
            
        for i, text in enumerate(text_parts):
            new_chunks, new_carry_over, new_small_chunks = tokenize_and_chunk(text, tokenizer, block_size, min_tokens, pbar, carry_over)
            carry_over = new_carry_over  # Update the carry_over
            all_chunks.extend(new_chunks)
            small_chunks.extend(new_small_chunks)
    
    if small_chunks:
        print(f"Warning: {len(small_chunks)} chunks are smaller than the minimum token limit.")
    
    sorted_text_chunks = [{"text": chunk} for chunk in all_chunks]
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(sorted_text_chunks, f, ensure_ascii=False)

# Argument parsing code remains the same

parser = argparse.ArgumentParser(description='Split file into chunks for training.')
parser.add_argument('--filename', type=str, required=True, help='Input filename')
parser.add_argument('--output_filename', type=str, required=True, help='Output filename')
parser.add_argument('--tokenizer', type=str, default='llama', help='Tokenizer to use (default: llama)')
parser.add_argument('--block_size', type=int, default=1024, help='Maximum number of tokens in each chunk (default: 1024)')
parser.add_argument('--min_tokens', type=int, default=50, help='Minimum number of tokens in each chunk (default: 50)')
parser.add_argument('--num_threads', type=int, default=4, help='Number of threads to use for tokenization (default: 4)')

args = parser.parse_args()

if args.tokenizer == 'llama':
    tokenizer = LlamaTokenizer.from_pretrained('llama-base')
else:
    tokenizer = LlamaTokenizer.from_pretrained(args.tokenizer)
    
tokenize_and_save(args.filename, args.output_filename, tokenizer, args.block_size, args.min_tokens)
