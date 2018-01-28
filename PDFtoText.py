import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    return document.text

files = ['letterexample']

for file in files:
    a = os.path.join(os.path.dirname(__file__), file)
    text = detect_document(a)
    fh = open(file+"output.txt", "w")
    fh.write(text)
    fh.close()


