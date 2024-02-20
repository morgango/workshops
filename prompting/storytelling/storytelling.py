from workshop_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, get_file_size, tell_story
from icecream import ic
import argparse

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Customize user message and run story response")
    parser.add_argument('--temperature', type=float, default=0, help="Temperature for simple_chat function")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help="Model for simple_chat function")
    parser.add_argument('--max_tokens', type=int, default=2000, help="Max tokens for simple_chat function")

    # Add command-line arguments for file paths
    parser.add_argument('--system_prompt_file', type=str, default='system-prompt.txt', help="File containing system message content")
    parser.add_argument('--subject_file', type=str, default='subject.txt', help="File containing subject content")
    parser.add_argument('--hero_file', type=str, default='hero.txt', help="File containing hero content")
    parser.add_argument('--location_file', type=str, default='location.txt', help="File containing location content")
    parser.add_argument('--user_prompt_file', type=str, default='user-prompt.txt', help="File containing user message content")
    parser.add_argument('--response_file', help="File to write the response to", default='results.txt')
    
    args = parser.parse_args()

    # Set local directory, initialize simple_chat_args
    set_local_directory()
    simple_chat_args = {
        'temperature': args.temperature,
        'model': args.model,
        'max_tokens': args.max_tokens
    }

    # Get system and user messages from files specified in command-line arguments
    system_prompt = get_file_contents(args.system_prompt_file)
    subject = get_file_contents(args.subject_file)
    hero = get_file_contents(args.hero_file)
    location = get_file_contents(args.location_file)
    user_prompt = get_file_contents(args.user_prompt_file)

    # Get the story response
    story_response = tell_story(user_prompt=user_prompt,
                                system_prompt=system_prompt,
                                subject=subject,
                                hero=hero,
                                location=location,
                                chat_args=simple_chat_args)

    # Write response to a file
    write_response_to_file(file_path=args.response_file, response=story_response)

    # Log the output and results
    result_size = get_file_size(args.response_file)

    ic(story_response, subject, hero, location, result_size)