import xml.etree.ElementTree as ET
from gensim.models import KeyedVectors
import numpy as np
import os
import sys
import csv

def get_pretrained_model():
    return KeyedVectors.load_word2vec_format(
        "GoogleNews-vectors-negative300.bin", binary=True
    )


def extract_text_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    text_data = []

    for element in root.iter():
        if element.text:
            text_data.append(element.text)

    return " ".join(text_data)


def embed_text(text, word2vec_model):
    return np.array([word2vec_model.get_vector(word) for word in text if word in word2vec_model.key_to_index])

def save_embedding_as_csv(embedded_text, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(embedded_text)

pretrained_model = get_pretrained_model()
for file_path in sys.argv[1:]:
    print(file_path)
    file_as_text = extract_text_from_xml(file_path)
    embedded_text = embed_text(file_as_text, pretrained_model)
    output_directory = "TextEmbedding"

    output_csv_path = os.path.join(
        output_directory, f"{os.path.basename(file_path)}_embedded.csv"
    )
    save_embedding_as_csv(embedded_text, output_csv_path)
