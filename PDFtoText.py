import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import categorise

import sys

# To use the credentials
# export GOOGLE_APPLICATION_CREDENTIALS=credentials2.json

def detect_document(path):
  """Detects document features in an image."""
  client = vision.ImageAnnotatorClient()
  
  with io.open(path, 'rb') as image_file:
    content = image_file.read()
  
  image = types.Image(content=content)
  
  response = client.document_text_detection(image=image)
  document = response.full_text_annotation
  return document.text

if __name__ == '__main__':
  files = ['letterexample.JPG']
  
  for file in sys.argv[1:]:
    path = os.path.join(os.path.dirname(__file__), file)
    text_contents = detect_document(path)
    
    print(categorise.categorise_letter(text_contents, path, debug=False))
