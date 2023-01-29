
import pdfplumber
from typing import List, Dict

import openai
import numpy as np

import config

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
openai.api_key = config.OPENAI_API_KEY

class Extract:
    def __init__(self):
        self.text_pages: List[str] = []

    def pdf2text(self, pdf_path):
        def format_text(pages_text: str) -> str:
            return pages_text.replace("\t", " ").replace("\n", " ").replace("\xa0", " ")
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                text = format_text(text)
                self.text_pages.append(text)
        return self.text_pages
    
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
                reformatted_pages[-1] += f" {page}"
            
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
            


# extra : if page less than 

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(model=model, input=text)
    return result["data"][0]["embedding"]


def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    query_embedding = get_embedding(query)
    
    document_similarities = []
    for context in contexts:
        similarity = vector_similarity(query_embedding, context["embedding"])
        document_similarities.append({"text": context["text"], "similarity": similarity})
        
    document_similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
    return document_similarities


if __name__ == "__main__":
    #testing
    pdf_file = 'Test/Creating Character Arcs by K.M. Weiland.pdf'
    text_and_embeddings: List[Dict[str, str]] = []

    extract = Extract()

    pages_text = extract.pdf2text(pdf_file)
    for page in pages_text:
        embedding = get_embedding(page)
        text_and_embeddings.append({"text": page, "embedding": embedding})


    a = order_document_sections_by_query_similarity("What is a \"Flat\" arc?", text_and_embeddings)
    for k in a[:5]:
        print(k["similarity"])
        print(k["text"])
        print("")