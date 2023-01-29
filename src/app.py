from flask import Flask
from extract import Extract

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


# Extracts text and embeddings from tuple (type of file, raw file data)
@app.route("/extract/<file_type>/<file_data>")
def extract(file_type, file_data):
    data = request.form['input_name']

    extract = Extract()
    if file_type == "pdf":
        pages_text = extract.pdf2text(file_data)


if __name__ == "__main__":
    app.run()
