import streamlit as st
from llm_calls import openai_chat, dalle_image, download_image, text_to_audio
from config import write_story_prompt

# Add a title
st.title("La Petite Wonder Week")  # Make this a var?

# Create a text input
user_input = st.text_input("Enter some text")

# Create a dropdown selection
option = st.selectbox(
    'What do you want to do?',
    ('Write a story', 'Make an image'))

# Create a button
if st.button('Create'):

    if option == 'Write a story':
        # Print request & create a placeholder
        placeholder = st.empty()
        placeholder.text('Creating a story based on your input...')
        st.markdown('---')

        # Update the placeholder with a the result
        result = openai_chat(write_story_prompt, user_input)
        placeholder.text('Creating an audio output of your story.')
        st.markdown(result)
        text_to_audio(result)
        # Create a button
      
        if st.button('Play Audio'):
            # Embed the audio file in the app
            st.audio('./audio.wav', format='audio/wav')
        
        placeholder.text('Audio file created, all items completed!')


    else:
        st.markdown('---')
        placeholder = st.empty()
        placeholder.text('Creating a picture based on your input...')
        result = dalle_image(user_input)
        placeholder.text('Downloading picture for display...')
        path = download_image(result)
        st.image(path)