
from workshop_common import set_local_directory, get_file_contents, get_file_lines, get_file_size, write_response_to_file, generate_csv
from icecream import ic


# Only run the function if the script is executed directly
if __name__ == "__main__":

    import argparse

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Simple chat program with command line arguments")
    
    # Add command line arguments for filenames and simple_chat_args with default values
    parser.add_argument('--user_prompt_file', help="File containing user message content", default='user-prompt.txt')
    parser.add_argument('--system_prompt_file', help="File containing system message content", default='system-prompt.txt')
    parser.add_argument('--response_file', help="File to write the response to", default='results.csv')
    
    parser.add_argument('--temperature', type=float, default=0.5, help="Temperature for simple_chat function")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="Model for simple_chat function")
    parser.add_argument('--max_tokens', type=int, default=2000, help="Max tokens for simple_chat function")
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # make sure python is looking at this local directory
    set_local_directory()

    # Get a really long file to summarize
    user_message_content = get_file_contents(args.user_prompt_file)
    
    # Tell the AI how to deal with the file
    system_message_content = get_file_contents(args.system_prompt_file)


    # Build simple_chat_args dictionary based on the command-line arguments
    chat_args = {
        'temperature': args.temperature,
        'model': args.model,
        'max_tokens': args.max_tokens
    }

    # send the information to OpenAI and get back a response
    csv_response = generate_csv(system_prompt=system_message_content, 
                                user_prompt=user_message_content, 
                                 chat_args=chat_args)

    # write the response to a file
    write_response_to_file(file_path=args.response_file, 
                           response=csv_response)

    # get the size of the prompt and the result
    result_size = get_file_lines(args.response_file)
    

    # get the sizes of the results
    prompt_size = get_file_size(args.user_prompt_file)
    result_size = get_file_size(args.response_file)

    ic(csv_response, prompt_size, result_size)