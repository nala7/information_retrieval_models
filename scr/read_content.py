import spacy
import os
import ir_datasets

from typing import Any
from utils import Document, Query
from data_sets.cran.cran import read_cran_documents, read_cran_queries, read_cran_rel
import pickle

nlp = spacy.load('en_core_web_sm')

def process_content(text):

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
    punctuations = "?:!.,;|<>*&$%#@!()_-=+"
    filtered_sentence2 = []
    for word in filtered_sentence1:
        if (word in punctuations) or word.isspace():
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


def get_cran_dataset(load_from_memory=True):
    if load_from_memory:
        with open('data_sets/cran/cran.pickle', 'rb') as infile:
            documents, queries, relevancy = pickle.load(infile)
    else:
        documents, queries, relevancy = _compute_cran_dataset()
        with open('data_sets/cran/cran.pickle', 'wb') as outfile:
            pickle.dump((documents, queries, relevancy), outfile)
    
    return documents, queries, relevancy


def get_ir_dataset(dataset_name, load_from_memory=True):
    if load_from_memory:
        with open(f'data_sets/{dataset_name}/{dataset_name}.pickle', 'rb') as infile:
            documents, queries, relevancy = pickle.load(infile)
    else:
        documents, queries, relevancy = _compute_ir_dataset(dataset_name)
        a = os.getcwd()
        with open(f'data_sets/{dataset_name}/{dataset_name}.pickle', 'wb') as outfile:
            pickle.dump((documents, queries, relevancy), outfile)
    
    return documents, queries, relevancy


def _compute_cran_dataset():
    documents_data = read_cran_documents()
    documents = []
    i = 1
    for (id, title, text) in documents_data:
        processed_text = process_content(text)
        documents.append(Document(id, title, processed_text))
        print('Document: ', i)
        i += 1

    queries_data = read_cran_queries()
    queries = []
    i = 1
    for id, text in queries_data:
        processed_text = process_content(text)
        queries.append(Query(id, processed_text))
        print('Query: ', i)
        i += 1

    relevancy = read_cran_rel()

    return documents, queries, relevancy


def _compute_ir_dataset(dataset_name):
    dataset = ir_datasets.load(dataset_name)

    i = 1
    documents = []
    for doc in dataset.docs_iter():
        print(f'Document: {i}')
        i += 1
        processed_text = process_content(doc.text)
        documents.append(Document(int(doc.doc_id), str(doc.doc_id), processed_text))
    
    queries = []
    i = 1
    for q in dataset.queries_iter():
        print(f'Query: {i}')
        i += 1
        processed_text = process_content(q.text)
        queries.append(Query(int(q.query_id), processed_text))
    
    query_rel = [[] for _ in range(dataset.queries_count())]
    i = 1
    for r in dataset.qrels_iter():
        print(f'Relevancy: {i}')
        i += 1
        query_rel[int(r.query_id) - 1].append((int(r.doc_id), 0))

    return documents, queries, query_rel


def read_query(query_text):
    filtered_query = process_content(query_text)
    return filtered_query
