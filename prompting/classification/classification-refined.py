from workshops_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file, append_line_to_file

# make sure python is looking in the right spot for the files we need.
set_local_directory()

# these are arguments that can be pre-defined and passed to the simple_chat function.
# they can be changed as needed. 
simple_chat_args = {
    'temperature': 0,
    'model': 'gpt-3.5-turbo',
    'max_tokens': 2000,
}

 
system_message_content = get_file_contents('system-prompt.txt')
flowers = get_file_contents('flowers-list.txt', return_as_list=True)
people = get_file_contents('people-list.txt', return_as_list=True)
food = get_file_contents('food-list.txt', return_as_list=True)

# Combine all the individual lists (flowers, people) into one comprehensive list
everything = flowers + people + food

# Set up an instruction for the system to classify the items in the 'everything' list
system_message = {"role": "system", 
                  "content": system_message_content}

append_line_to_file('results-refined.txt', "-------")

# Iterate over each item in the 'everything' list
for item in everything:
    
    # Construct a user message for each item, prompting its classification
    user_message_string = get_file_contents('user-prompt.txt')
    user_message_content = user_message_string.format(item=item)

    user_message = {"role": "user", 
                    "content": user_message_content}
    
    # Send the system and user messages to and get back a classification response
    classification_response = simple_chat(messages=[system_message, 
                                                    user_message], 
                                          **simple_chat_args)
    
    # Extract the content of the response which contains the classification
    classification = classification_response.choices[0].message.content
    
    results = f"item: {item}, classification: {classification}"
    append_line_to_file('results-refined.txt', results)
