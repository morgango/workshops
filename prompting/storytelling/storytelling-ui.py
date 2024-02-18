
from workshops_common import set_local_directory, simple_chat, get_file_contents, write_response_to_file
import streamlit as st


set_local_directory()

model_options = ['gpt-3.5-turbo', 'gpt-4.0', 'gpt-4.5']

def main():

    st.title("Storytelling Application")

    # break the buttons into three columns so they can be side by side
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperature = st.number_input("Temperature:", value=0.0, step=0.1, max_value=1.0, min_value=0.0)
    
    with col2:
        model_options = ['gpt-3.5-turbo', 'gpt-4.0', 'gpt-4.5']
        model = st.selectbox("Model:", model_options)
    
    with col3:
        max_tokens = st.number_input("Max Tokens:", value=2000, step=100, max_value=2000, min_value=100)
    
    # these are arguments that can be pre-defined and passed to the simple_chat function.
    simple_chat_args = {
        'temperature': temperature,
        'model': model,
        'max_tokens': max_tokens,
    }

    # break the buttons into three columns so they can be side by side
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hero_text = get_file_contents('hero.txt')
        hero = st.text_area("Hero:", value=hero_text, height=50, max_chars=None, key=None)
    
    with col2:
        subject_text = get_file_contents('subject.txt')
        subject = st.text_area("Subject:", value=subject_text, height=50, max_chars=None, key=None)
    
    with col3:
        location_text = get_file_contents('location.txt')
        location = st.text_area("Location:", value=location_text, height=50, max_chars=None, key=None)
    
    # these are arguments that can be pre-defined and passed to the simple_chat function.
    simple_chat_args = {
        'temperature': temperature,
        'model': model,
        'max_tokens': max_tokens,
    }


    # Read in default values from the system-prompt.txt and user-prompt.txt files
    system_prompt = get_file_contents('system-prompt.txt')
    system_message_content = st.text_area("System Prompt:",value=system_prompt, height=100, max_chars=None, key=None)

    user_prompt = get_file_contents('user-prompt.txt')
    user_message_string = st.text_area("User Prompt:", value=user_prompt, height=200, max_chars=None, key=None,)
    
   
    if st.button("Create a Story"):

        user_message_content = user_message_string.format(subject=subject, 
                                                        hero=hero, 
                                                        location=location)
        
        # build our messages to send to openAI.  These should be well formed JSON with a ROLE and CONTENT
        system_message = {"role":"system", 
                        "content": system_message_content}
        user_message = {"role":"user",
                        "content": user_message_content}

        # send the information to the LLM and get back a response
        chat_response = simple_chat(messages=[system_message, 
                                         user_message], 
                               **simple_chat_args)

        # extract the response from the chat response
        response = chat_response.choices[0].message.content

        st.markdown(
            f"""
            <div style="white-space: pre-wrap; word-wrap: break-word;">
                <b>User Prompt:</b> 
                {user_message_content}
            </div>
            """,
            unsafe_allow_html=True
        )

        # st.text(f"<b>True Prompt: {user_message_content}")

        # display the response on the screen
        st.text_area("Here you go:", value=response, height=200, max_chars=None, key=None)
        
        # write the results to a file
        write_response_to_file(file_path='results.txt', 
                           response=chat_response)

if __name__ == "__main__":
    main()