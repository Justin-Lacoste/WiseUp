
import pdfplumber
from typing import List

import pytube
import whisper

import openai
import numpy as np
from docx import Document

import config
openai.api_key = config.OPENAI_API_KEY

from settings import WHISPER_MODEL_NAME, EMBEDDING_MODEL


class Extract:
    def __init__(self):
        self.text_pages: List[str] = []
        
    def extract_pages(self, file_or_link_or_str: str, str_type: str) -> List[str]:
        if str_type == "text":
            self.text_pages = self.text2text_pages(file_or_link_or_str)
        elif str_type == "pdf":
            self.text_pages = self.pdf2text(file_or_link_or_str)
        elif str_type == "mp3":
            self.text_pages = self.mp3_to_text(file_or_link_or_str)
        elif str_type == "mp4":
            self.text_pages = self.mp4_to_text(file_or_link_or_str)
        elif str_type == "youtube":
            self.text_pages = self.youtube2text(file_or_link_or_str)
        elif str_type == "github":
            self.text_pages = self.github2text(file_or_link_or_str)
        elif str_type == "docx":
            self.text_pages = self.docx2text(file_or_link_or_str)
        
        self.reformat_pages()
        return self.text_pages
            
    def text2text_pages(self, text: str, threshold: int=700):
        for chunk in text.split('. '):
            if self.text_pages and len(chunk)+len(self.text_pages[-1]) < threshold:
                self.text_pages[-1] += ' '+chunk+'.'
            else:
                self.text_pages.append(chunk+'.')
        return self.text_pages

    def pdf2text(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text().replace("\t", " ").replace("\n", " ").replace("\xa0", " ")
                self.text_pages.append(text)
        return self.text_pages

    def mp3_to_text(self, mp3_path):
        model = whisper.load_model(WHISPER_MODEL_NAME)
        self.text_pages = model.transcribe(mp3_path, language='english')["text"]
        return self.text_pages

    def mp4_to_text(self, mp4_path):
        model = whisper.load_model(WHISPER_MODEL_NAME)
        self.text_pages = model.transcribe(mp4_path, language='english')["text"]
        return self.text_pages

    def youtube2text(self, youtube_link):
        data = pytube.YouTube(youtube_link)
        video = data.streams.get_highest_resolution()
        video_path = video.download()
        return self.mp4_to_text(video_path)

    def github2text(self, github_repo_link):
        raise NotImplementedError("github2text")

    def word_office_to_text(self, word_file_path):
        document = Document(word_file_path)
        for para in document.paragraphs:
            self.text_pages.append(para.text)
        return self.text_pages
    
    def reformat_pages(self):
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
        self.text_pages = reformatted_pages
            
    def get_dict(self):
        # This program takes a list of strings, and returns a dictionary in the following format: {"pages_text": ["page1", "page2", ...], "pages_embeddings": arr.tolist()}
        
        def get_embedding(page: str):
            result = openai.Embedding.create(model=EMBEDDING_MODEL, input=page)
            return result["data"][0]["embedding"]

        arr = np.array([get_embedding(page) for page in self.text_pages])
        return self.text_pages, arr.tolist()