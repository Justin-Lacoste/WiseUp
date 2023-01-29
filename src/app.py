from flask import Flask, request
from extract import Extract
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# Extracts text and embeddings from tuple (type of file, raw file data)
@app.route("/extract/", methods=['GET', 'POST'])
def extract():#file_type, file_data):
    data = request.form["file"]
    print(data, type(data))
    
    # extract = Extract()
    # if file_type == "pdf":
    #     pages_text = extract.pdf2text(file_data)
    
    # print(pages_text)
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
