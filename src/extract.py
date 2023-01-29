
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

