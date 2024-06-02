from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import requests
import pygame


def openai_chat(system_prompt, user_prompt):
    """
    Generates a response by having a chat conversation with the GPT-4o model.

    Args:
        system_prompt (str): The initial prompt for the system.
        user_prompt (str): The user's input prompt.

    Returns:
        str: The generated response from the GPT-4o model.
    """

    load_dotenv()
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    response = completion.choices[0].message.content
    log_to_file('prompts.json', user_prompt, response)
    return response


def log_to_file(filename, user_prompt, system_response):
    """
    Logs the given text output to a file with the specified filename.

    Parameters:
    - text_name (str): The name of the text output.
    - text_output (str): The text output to be logged.
    - filename (str): The name of the file to log the text output to.

    Returns:
    None
    """
    data = {}
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    data[user_prompt] = system_response

    with open(filename, 'w') as f:
        json.dump(data, f)

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def text_to_audio(text):
    load_dotenv()
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text
    )
    response.stream_to_file('./audio.wav')


def dalle_image(user_prompt):
    """
    Generates an image using the DALL-E model based on the given user prompt.

    Args:
        user_prompt (str): The prompt provided by the user.

    Returns:
        str: The URL of the generated image.
    """
    load_dotenv()
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=user_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url


def download_image(url, directory='./images'):
    """
    Downloads an image from the given URL and saves it to the specified directory.

    Args:
        url (str): The URL of the image to download.
        directory (str): The directory to save the downloaded image.

    Returns:
        str: The path of the downloaded image file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(url)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    else:
        raise Exception(f"Failed to download image from {url}")
