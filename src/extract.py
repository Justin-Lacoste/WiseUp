
import pdfplumber
from typing import List, Dict
import json

import pytube
import whisper

import openai
import numpy as np

import config
openai.api_key = config.OPENAI_API_KEY

from settings import WHISPER_MODEL_NAME, EMBEDDING_MODEL

class Extract:
    def __init__(self):
        self.transcript = ""
        self.transcript_blocks = []
        
    def extract_pages(self, file_or_link_or_str: str, str_type: str) -> List[str]:
        if str_type == "text":
            self.text2text_pages(file_or_link_or_str)
        elif str_type == "pdf":
            self.pdf2text(file_or_link_or_str)
        elif str_type == "mp3":
            self.mp3_to_text(file_or_link_or_str)
        elif str_type == "mp4":
            self.mp4_to_text(file_or_link_or_str)
        elif str_type == "youtube":
            self.youtube2text(file_or_link_or_str)
        elif str_type == "github":
            self.github2text(file_or_link_or_str)
        #elif str_type == "docx":
        #    self.docx2text(file_or_link_or_str)
        
        self.transcript_to_transcript_blocks()
        return self.transcript_blocks
            
    def text2text_pages(self, text: str):
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
        """document = Document(word_file_path)
        for para in document.paragraphs:
            self.text_pages.append(para.text)
        return self.text_pages"""
        raise NotImplementedError("word_office_to_text")
    
    def transcript_to_transcript_blocks(self):
        block_size = 500
        transcript_sentences = self.transcript.split(". ")
        for i, sentence in enumerate(transcript_sentences):
            # if the sentence is huge, add it to its own block
            
            if len(sentence) > block_size:
                self.transcript_blocks.append(sentence)
            # 3/4 time, add sentence to block
            elif i % 15 == 0:
                self.transcript_blocks.append(sentence + ". ")
            else:
                self.transcript_blocks[-1] += f"{sentence}. "
        return self.transcript_blocks
            
    def get_dict(self):
        # This program takes a list of strings, and returns a dictionary in the following format: {"pages_text": ["page1", "page2", ...], "pages_embeddings": arr.tolist()}
        
        def get_embedding(block: str):
            result = openai.Embedding.create(model=EMBEDDING_MODEL, input=block)
            return result["data"][0]["embedding"]

        arr = np.array([get_embedding(block) for block in self.transcript_blocks])
        return self.transcript_blocks, arr.tolist()




