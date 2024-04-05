from workshop_common import set_local_directory, get_file_contents, get_file_size, write_response_to_file, summarize_text
from icecream import ic
import os

def process_files(directory, system_prompt_file, response_file, temperature, model, max_tokens, cost_per_token):
    total_cost = 0

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            user_prompt_file = os.path.join(directory, filename)
            ic(f"Processing {user_prompt_file}...")

            user_message_content = get_file_contents(user_prompt_file)
            system_message_content = get_file_contents(system_prompt_file)

            chat_args = {
                'temperature': temperature,
                'model': model,
                'max_tokens': max_tokens
            }

            response = summarize_text(user_prompt=user_message_content,
                                      system_prompt=system_message_content,
                                      chat_args=chat_args)
            
            response_filename = os.path.join(response_file, f"response_{filename}")
            write_response_to_file(file_path=response_filename, response=response)

            # Calculate the number of tokens and the cost for this file
            num_tokens = len(response.split())
            cost = num_tokens * cost_per_token
            total_cost += cost

            # Output the number of tokens and cost for this file
            ic(f"Number of tokens: {num_tokens}, Cost: {cost}")

            prompt_size = get_file_size(user_prompt_file)
            result_size = get_file_size(response_filename)

            ic(response, prompt_size, result_size)

    # Output the total cost for all files
    ic(f"Total cost for all files: {total_cost}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Summarization program with command line arguments")
    parser.add_argument('--directory', help="Directory containing user message content files", required=True)
    parser.add_argument('--system_prompt_file', help="File containing system message content", default='system-prompt.txt')
    parser.add_argument('--response_directory', help="Directory to write the responses to", default='responses')
    parser.add_argument('--temperature', type=float, default=0, help="Temperature for summarization function")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="Model for summarization function")
    parser.add_argument('--max_tokens', type=int, default=2000, help="Max tokens for summarization function")
    parser.add_argument('--cost_per_token', type=float, default=0.01, help="Cost per token for processing")
    args = parser.parse_args()

    set_local_directory()

    if not os.path.exists(args.response_directory):
        os.makedirs(args.response_directory)

    process_files(args.directory, args.system_prompt_file, args.response_directory, args.temperature, args.model, args.max_tokens, args.cost_per_token)
