import pdfplumber
from typing import List, Dict

import openai
import numpy as np


pdf_file = 'src\Test\Creating Character Arcs by K.M. Weiland.pdf'
pdf_file = 'Test\Floating Point.pdf'

from settings import EMBEDDING_MODEL

openai.api_key = ""


def extract_pages(pdf_file) -> List[str]:
    pages_text = []
    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages
        for page in pages:
            text = page.extract_text().replace("\t", " ").replace("\n", " ").replace("\xa0", " ")
            pages_text.append(text)
    return pages_text


def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(model=model, input=text)
    return result["data"][0]["embedding"]


def get_embeddings(text_pages: List[str]) -> np.array:
    """
    This function is used to get the embeddings of a list of text pages.

    Args:
        text_pages (List[str]): A list of strings, each string being a page of text.

    Returns:
        np.array: A numpy array of shape (n, 1024), where n is the number of pages.
    """
    result = openai.Embedding.create(model=model, input=texts)
    return [x["embedding"] for x in result["data"]]


def vector_similarity(x: list[float], y: list[float]) -> float:
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    query_embedding = get_embedding(query)
    
    document_similarities = []
    for context in contexts:
        similarity = vector_similarity(query_embedding, context["embedding"])
        document_similarities.append({"text": context["text"], "similarity": similarity})
        
    document_similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
    return document_similarities


text_and_embeddings: List[Dict[str, str]] = []

pages_text = extract_pages(pdf_file)
for page in pages_text:
    embedding = get_embedding(page)
    text_and_embeddings.append({"text": page, "embedding": embedding})


b = order_document_sections_by_query_similarity("What is IEEE 754?", text_and_embeddings)
for k in b[:5]:
    print(k["similarity"])
    print(k["text"])
    print("")