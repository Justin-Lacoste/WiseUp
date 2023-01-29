
import pdfplumber
from typing import List, Dict
import json

import pytube
import whisper

import openai
import numpy as np

import config

openai.api_key = config.OPENAI_API_KEY


class Extract:
    def __init__(self):
        self.text_pages: List[str] = []

    def pdf2text(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text().replace("\t", " ").replace("\n", " ").replace("\xa0", " ")
                self.text_pages.append(text)
        return self.text_pages

    def mp3_to_text(self, mp3_path):
        model = whisper.load_model(config.WHISPER_MODEL_NAME)
        self.text_pages = model.transcribe(mp3_path, language='english')["text"]
        return self.text_pages

    def mp4_to_text(self, mp4_path):
        model = whisper.load_model(config.WHISPER_MODEL_NAME)
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
        raise NotImplementedError("word_office_to_text")
    
    def reformat_pages(self):
        low_thresh = 150
        high_thresh = 750
        
        reformatted_pages = [""]
        count = 0
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
                count += 2
            
            #condition 3, add the page to a new reformatting page
            else:
                reformatted_pages.append(page)
        self.text_pages = reformatted_pages
            



def get_json(pages_text: List[str]):
    # This program takes a list of strings, and returns a json file in the following format: {pages_text: [page1, page2, ...], pages_embeddings: arr.tolist()}
    
    def get_embedding(page: str):
        result = openai.Embedding.create(model=config.EMBEDDING_MODEL, input=page)
        return result["data"][0]["embedding"]

    arr = np.array([get_embedding(page) for page in pages_text])
    return json.dumps({"pages_text": pages_text, "pages_embeddings": arr.tolist()})


# def vector_similarity(x: list[float], y: list[float]) -> float:
#     """
#     Returns the similarity between two vectors.
    
#     Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
#     """
#     return np.dot(np.array(x), np.array(y))


# def order_document_sections_by_query_similarity(query: str, contexts: List[Dict[str, str]]) -> List[Dict[str, str]]:
#     query_embedding = get_embedding(query)
    
#     document_similarities = []
#     for context in contexts:
#         similarity = vector_similarity(query_embedding, context["embedding"])
#         document_similarities.append({"text": context["text"], "similarity": similarity})
        
#     document_similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
#     return document_similarities


if __name__ == "__main__":
    #testing
    
    # PDF
    pdf_file = r'C:\Users\Henri\Documents\GitHub\WiseUp\src\Test\Floating Point.pdf'
    text_and_embeddings: List[Dict[str, str]] = []

    extract = Extract()

    pages_text = extract.pdf2text(pdf_file)
    extract.reformat_pages()

    json = get_json(extract.text_pages)
    print(json)
    
    # # MP3
    # mp3_file = r'C:\Users\Henri\Documents\GitHub\Project-Lawful-Audiobook - Copy\Audio\what the truth can destroy - episode 22 - excerpt.mp3'
    # text_and_embeddings: List[Dict[str, str]] = []

    # extract = Extract()

    # pages_text = extract.mp3_to_text(mp3_file)
    # extract.reformat_pages()

    # json = get_json(extract.text_pages)
    # print(json)
    
    # # MP4
    # mp4_file = r'C:\Users\Henri\OneDrive - McGill University\VSC\MAIS Hacks\MAIS_Hacks_ScribeAI\videos\Aaron Paul wins an Emmy for Breaking Bad 2014.mp4'
    # text_and_embeddings: List[Dict[str, str]] = []

    # extract = Extract()

    # pages_text = extract.mp4_to_text(mp4_file)
    # extract.reformat_pages()

    # json = get_json(extract.text_pages)
    # print(json)
    
    # # Youtube
    # youtube_link = "https://www.youtube.com/watch?v=_bcfxty39Cw"
    # text_and_embeddings: List[Dict[str, str]] = []
    
    # extract = Extract()
    
    # pages_text = extract.youtube2text(youtube_link)
    # extract.reformat_pages()
    
    # json = get_json(extract.text_pages)
    # print(json)
    
    # # Github
    # github_link = "https://github.com/Justin-Lacoste/WiseUp"
    # text_and_embeddings: List[Dict[str, str]] = []
    
    # extract = Extract()
    
    # pages_text = extract.github2text(github_link)
    # extract.reformat_pages()

    # json = get_json(extract.text_pages)
    # print(json)
    
    # # Word Office
    # word_file = r'C:\Users\Henri\Documents\GitHub\WiseUp\src\Test\test.docx'
    # text_and_embeddings: List[Dict[str, str]] = []
    
    # extract = Extract()
    
    # pages_text = extract.word_office_to_text(word_file)
    # extract.reformat_pages()

    # json = get_json(extract.text_pages)
    # print(json)
    