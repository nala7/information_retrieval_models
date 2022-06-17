import os
import spacy
from typing import Any
from utils import Document, Query
from data_sets.cran.cran import read_cran_documents, read_cran_queries
import pickle


def process_content(text):
    nlp = spacy.load('en_core_web_sm')

    nlp.max_length = 5030000  # or higher
    doc = nlp(text)

    # Tokenization and lemmatization are done with the spacy nlp pipeline commands
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)

    # Filter the stopword
    filtered_sentence1: list[Any] = []
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            filtered_sentence1.append(word)

    # Remove punctuation
    punctuations = "?:!.,;|<>*&$%#@!()_-=+ "
    filtered_sentence2 = []
    for word in filtered_sentence1:
        if word in punctuations:
            continue
        if word == '\n':
            continue
        filtered_sentence2.append(word)  
    
    return filtered_sentence2


def read_dataset(path):
    doc_list = []
    for filename in os.listdir(path):
        if filename[0] == '.':  # if file is hidden skip
            continue
        with open(os.path.join(path, filename), 'r', errors='ignore') as f:
            text = f.read()
            filtered_text = process_content(text)
            document = Document(filename, filtered_text)
            doc_list.append(document)
            print(filename, "was read successfully")
    return doc_list

def get_cran_dataset(load_from_memory = True):
    if load_from_memory:
        with open('data_sets\\cran\\cran.pickle', 'rb') as infile:
            documents, queries = pickle.load(infile)
    else:
        documents, queries = _compute_cran_dataset()
        with open('data_sets\\cran\\cran.pickle', 'wb') as outfile:
            pickle.dump((documents,queries), outfile)
    
    return documents, queries

def _compute_cran_dataset():
    documents_data = read_cran_documents()
    documents = []
    i = 1
    for (title, text) in documents_data:
        processed_text = process_content(text)
        documents.append(Document(title, processed_text))
        print('Document: ', i)
        i+= 1

    queries_data = read_cran_queries()
    queries = []
    for text in queries_data:
        processed_text = process_content(text)
        queries.append(Query(processed_text))

    return documents, queries

def read_query(query_text):
    filtered_query = process_content(query_text)
    return filtered_query
