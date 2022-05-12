import os
import spacy
from typing import List, Any
from document_type import Documents


def process_document(text):
    nlp = spacy.load('en_core_web_sm')

    nlp.max_length = 5030000  # or higher
    doc = nlp(text)

    # Tokenization and lemmatization are done with the spacy nlp pipeline commands
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)
    print("Tokenize+Lemmatize:")
    # print(lemma_list)

    # Filter the stopword
    filtered_sentence: list[Any] = []
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            filtered_sentence.append(word)

    # Remove punctuation
    punctuations = "?:!.,;|<>*&$%#@!()_-=+"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)
        if word == '\n':
            filtered_sentence.remove(word)
    print(" ")
    print("Remove stopword & punctuation: ")
    print(filtered_sentence)
    return filtered_sentence


def read_dataset(path):
    doc_list = []
    doc_id = 1
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', errors='ignore') as f:
            text = f.read()
            filtered_text = process_document(text)
            document = Documents(doc_id, filename, filtered_text)
            doc_list.append(document)
            doc_id += 1
            print(filename, "was read successfully")