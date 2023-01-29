
import pdfplumber
from typing import List, Dict
import json

import pytube
import whisper

import openai
import numpy as np

import config
openai.api_key = config.OPENAI_API_KEY

from settings import WHISPER_MODEL_NAME


class Extract:
    def __init__(self):
        self.transcript = ""

    def text2text_pages(self, text:str):
        self.transcript = text
        return self.transcript

    def pdf2text(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text().replace("\t", " ").replace("\n", " ").replace("\xa0", " ")
                self.transcript += text
        return self.transcript

    def mp3_to_text(self, mp3_path):
        model = whisper.load_model(WHISPER_MODEL_NAME)
        self.transcript = model.transcribe(mp3_path, language='english')["text"]
        return self.transcript

    def mp4_to_text(self, mp4_path):
        model = whisper.load_model(WHISPER_MODEL_NAME)
        self.transcript = model.transcribe(mp4_path, language='english')["text"]
        return self.transcript

    def youtube2text(self, youtube_link):
        data = pytube.YouTube(youtube_link)
        video = data.streams.get_highest_resolution()
        video_path = video.download()
        return self.mp4_to_text(video_path)

    def github2text(self, github_repo_link):
        raise NotImplementedError("github2text")

    def word_office_to_text(self, word_file_path):
        raise NotImplementedError("word_office_to_text")

    def transcript_to_blocks(self):
        block_size = 200 #
        transcript_sentences = self.transcript.split(". ")
        transcript_blocks = []
        for i, sentence in enumerate(transcript_sentences):
            # if the sentence is huge, add it to its own block
            if len(sentence) > block_size:
                transcript_blocks.append(sentence)
            # 3/4 time, add sentence to block
            elif i % 4 != 3:
                transcript_blocks[-1] += f"{sentence}. "
            else:
                transcript_blocks.append(sentence)
        return transcript_blocks
    
    """def reformat_pages(self):
        low_thresh = 150
        high_thresh = 750
        
        reformatted_pages = [""]
        for page in self.text_pages:
            words_in_last_page = len(reformatted_pages[-1].split())
            words_in_cur_page = len(page.split())

            #condition 1, add page to last page
            if (words_in_last_page < low_thresh) and (words_in_last_page + 1 + words_in_cur_page < high_thresh):
                reformatted_pages[-1] += f"\n{page}"
            
            #condition 2, page too big, split in two
            elif (words_in_cur_page > high_thresh):
                half_page_i = len(page)//2
                reformatted_pages.append(page[:half_page_i])
                reformatted_pages.append(page[half_page_i:])
            
            #condition 3, add the page to a new reformatting page
            else:
                reformatted_pages.append(page)
        self.text_pages = reformatted_pages"""

            



def get_json(pages_text: List[str]):
    # This program takes a list of strings, and returns a json file in the following format: {pages_text: [page1, page2, ...], pages_embeddings: arr.tolist()}
    
    def get_embedding(page: str):
        result = openai.Embedding.create(model=config.EMBEDDING_MODEL, input=page)
        return result["data"][0]["embedding"]

    arr = np.array([get_embedding(page) for page in pages_text])
    return json.dumps({"pages_text": pages_text, "pages_embeddings": arr.tolist()})


if __name__ == "__main__":
    #testing
    
    # PDF
    pdf_file = r'src\Test\Floating Point.pdf'
    text_and_embeddings: List[Dict[str, str]] = []

    e = Extract()

    pages_text = e.pdf2text(pdf_file)
    e.reformat_pages()

    json = get_json(e.text_pages)
    print(json)

