from flask import Flask, request
from extract import Extract, construct_prompt, answer_question
import requests
import cohere

import whisper
import random
import string
import os
from typing import List, Dict
import tiktoken
import openai

import config
from settings import WHISPER_MODEL_NAME, COMPLETIONS_MODEL


app = Flask(__name__)


co = cohere.Client(config.COHERE_API_KEY)
model = whisper.load_model(WHISPER_MODEL_NAME)

MAX_SECTION_LEN = 500
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))


def construct_prompt(question: str, most_relevant_document_sections: List[str]) -> str:
    """
    Fetch relevant 
    """
    chosen_sections = []
    chosen_sections_len = 0
     
    for section in most_relevant_document_sections:
        chosen_sections_len += section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break
            
        chosen_sections.append(SEPARATOR + section.content.replace("\n", " "))
            
    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""
    
    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"


@app.route("/extract/", methods=['GET', 'POST'])
def extract():
    title = request.args.get('title')
    directory = request.args.get('directory')
    UUID = request.args.get('UUID')
    file = request.files['file']
    file_type = request.args.get('file_type')
    rand_file_name = f"{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))}.{file_type}"
    
    with open(rand_file_name, "wb") as f:
        f.write(file.read())
    
    extract = Extract()
    text_pages = extract.extract_pages(rand_file_name, file_type)
    os.remove(rand_file_name)
    text_pages, embedding_pages = extract.get_dict()
    
    dict_info = {
        "title": title,
        "directory": directory,
        "UUID": UUID,
        "data": {"text_pages": text_pages, "embeddings": embedding_pages}
    }
    res = requests.post('http://107.22.146.14:3000/json_to_s3', json=dict_info, headers={'Content-Type': 'application/json'})

    return {"status": "200"}


@app.route("/summarize/", methods=['GET', 'POST'])
def summarize_page():
    text_to_summarize = request.args.get('text_to_summarize')
    

    prediction = co.generate(
        model='xlarge',
        prompt=f"{text_to_summarize}\nTLDR:",
        return_likelihoods='GENERATION',
        #stop_sequences=['.'],
        max_tokens=300,
        temperature=0.2,
    )
    return prediction.generations[0].text


@app.route("/answer/", methods=['GET', 'POST'])
def answer_question():
    question = request.args.get('question')
    most_relevant_document_sections = request.args.get('most_relevant_document_sections')
    show_prompt = request.args.get('show_prompt')
    
    prompt = construct_prompt(question, most_relevant_document_sections)
    if show_prompt:
        print(prompt)
    COMPLETIONS_API_PARAMS = {
        "temperature": 0.0,
        "max_tokens": 300,
        "model": COMPLETIONS_MODEL,
    }

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )
    return response["choices"][0]["text"].strip(" \n")

    # prediction = co.generate(
    #     model='xlarge',
    #     prompt=f"{'\n'.join(top_k_strings)[:6000]}\nQ: {question}\nA: ",
    #     return_likelihoods='GENERATION',
    #     stop_sequences=['.'],
    #     max_tokens=200,
    #     temperature=0.2,
    # )
    # return prediction.generations[0].text


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
