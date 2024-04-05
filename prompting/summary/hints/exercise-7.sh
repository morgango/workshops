#!/bin/bash

# Set the directory containing the text files
directory="path/to/your/directory"

# Set the other arguments for summary.py
system_prompt_file="system-prompt.txt"
response_file="results.txt"
temperature=0.7
model="gpt-3.5-turbo"
max_tokens=2000

# Iterate over all .txt files in the directory
for user_prompt_file in "$directory"/*.txt; do
    echo "Processing $user_prompt_file..."
    python summary.py \
        --user_prompt_file "$user_prompt_file" \
        --system_prompt_file "$system_prompt_file" \
        --response_file "$response_file" \
        --temperature "$temperature" \
        --model "$model" \
        --max_tokens "$max_tokens"
done