from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, get_file_size, execute_prompt
from icecream import ic
import argparse

if __name__ == "__main__":
    
    design_type="complete"

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Customize user message and run story response")
    parser.add_argument('--temperature', type=float, default=0, help="Temperature for simple_chat function")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="Model for simple_chat function")
    parser.add_argument('--max_tokens', type=int, default=2000, help="Max tokens for simple_chat function")

    # Add command-line arguments for file paths
    parser.add_argument('--system_prompt_file', type=str, default='system-prompt.txt', help="File containing system message content")
    parser.add_argument('--user_prompt_file', type=str, default=f'user-prompt-{design_type}.txt', help="File containing user message content")
    parser.add_argument('--response_file', help="File to write the response to", default=f'results-{design_type}.txt')
    parser.add_argument('--location_file', type=str, default='location.txt', help="File containing location content")
    parser.add_argument('--format_file', type=str, default='format.txt', help="File containing format content")
    parser.add_argument('--length_file', type=str, default='length.txt', help="File containing length content")
    parser.add_argument('--mentions_file', type=str, default='mentions.txt', help="File containing mentions content")
    parser.add_argument('--instructions_file', type=str, default='instructions.txt', help="File containing instructions content")
    parser.add_argument('--shots_file', type=str, default='shots.txt', help="File containing shots content")
    parser.add_argument('--start_file', type=str, default='start.txt', help="File containing start content")
    parser.add_argument('--nickname_file', type=str, default='nickname.txt', help="File containing nickname content")

    args = parser.parse_args()

    # Set local directory, initialize simple_chat_args
    set_local_directory()
    chat_args = {
        'temperature': args.temperature,
        'model': args.model,
        'max_tokens': args.max_tokens
    }

    # Get system and user messages from files specified in command-line arguments
    location = get_file_contents(args.location_file)

    prompt_args={'location': location,
                 'format': get_file_contents(args.format_file),
                 'length': get_file_contents(args.length_file),
                 'mentions': get_file_contents(args.mentions_file),
                 'instructions': get_file_contents(args.instructions_file),
                 'shots': get_file_contents(args.shots_file),
                 'start': get_file_contents(args.start_file),
                 'nickname': get_file_contents(args.nickname_file),
                 } 

    # # use the information from our files to customize the user message
    user_message = get_file_contents(args.user_prompt_file)
    system_message = get_file_contents(args.system_prompt_file)

    prompt_response = execute_prompt(user_prompt=user_message, 
                                    system_prompt=system_message, 
                                    prompt_vars=prompt_args, 
                                    chat_args=chat_args)

    # Write response to a file
    write_response_to_file(file_path=args.response_file, response=prompt_response)

    # Log the output and results
    result_size = get_file_size(args.response_file)
    ic(prompt_response, result_size)

# from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file
# from icecream import ic

# # make sure python is looking in the right spot for the files we need.
# set_local_directory()

# # these are arguments that can be pre-defined and passed to the simple_chat function.
# # they can be changed as needed. 
# simple_chat_args = {
#     'temperature': 0,
#     'model': 'gpt-3.5-turbo',
#     'max_tokens': 2000,
# }

# # get the system and user messages from the files
# system_message_content = get_file_contents('system-prompt.txt')

# # define some parameters for this story
# location = get_file_contents('location.txt')
# nickname = get_file_contents('nickname.txt')
# format = get_file_contents('format.txt')
# length = get_file_contents('length.txt')
# instructions = get_file_contents('instructions.txt')
# mentions = get_file_contents('mentions.txt')
# shots = get_file_contents('shots.txt')
# start = get_file_contents('start.txt')

# # use the information from our files to customize the user message
# user_message_string = get_file_contents('user-prompt-complete.txt')
# user_message_content = user_message_string.format(location=location,
#                                                  nickname=nickname,
#                                                  format=format,
#                                                  length=length,
#                                                  instructions=instructions,
#                                                  mentions=mentions,
#                                                  shots=shots,
#                                                  start=start)

# # create the messages we are going to use to create the story.
# system_message = {"role":"system", "content": system_message_content}
# user_message = {"role":"user", "content": user_message_content}

# # send the information to OpenAI and get back a response
# story_response = simple_chat(messages=[system_message, 
#                                        user_message], 
#                              **simple_chat_args)

# # write the response to a file
# write_response_to_file(file_path='results-complete.txt', 
#                        response=story_response)

# import re
# response = get_file_contents('results-complete.txt', return_as_list=True)

# for paragraph in response:
#     print(f"paragraph: {paragraph}")

# # log output the results
# ic(location, nickname, format, length, instructions, mentions, shots, start)
# ic(story_response.choices[0].message.content)