#!/Users/animeshtalukdar/Desktop/Github/old/temp/summarize_youtube/env/bin/python

import sys
from youtube_transcript_api import YouTubeTranscriptApi 
import tkinter as tk
# import google api
from google import genai
# env variables
import os
from bs4 import BeautifulSoup
from markdown import markdown
import re



# client = genai.Client(api_key=os.environ["GOOGLE_API"])
client = genai.Client(api_key="YOUR_API_KEY_HERE")



def summarize_text(text):
    response = client.models.generate_content(model="gemini-2.0-flash-thinking-exp", contents="summarize the following you can ignore sponsorship sections it is the captions of a youtube video" + text)
    return response.text


def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text

from urllib.parse import urlparse, parse_qs

def get_url_arguments(url):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)


def get_subs_text(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    text = " ".join([line['text'] for line in transcript])
    return text

def get_text_from_video(url):
    arguments = get_url_arguments(url)
    if 'v' not in arguments:
        print("No video ID found in the URL")
        sys.exit(1)
    video_id = arguments['v'][0]

    return get_subs_text(video_id)

# print(get_text_from_video("https://www.youtube.com/watch?v=zg9-C61MnwA"))

def create_window_with_text(text):
    root = tk.Tk()
    text_widget = tk.Text(root)
    text_widget.insert(tk.END, text)
    text_widget.pack()
    root.mainloop()

url = input()
if "youtube" not in url:
    print("Not a youtube video")
    sys.exit(1)
text = summarize_text(get_text_from_video(url))
print(markdown_to_text(text))
# create_window_with_text(text)
