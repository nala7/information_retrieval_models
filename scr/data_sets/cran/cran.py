from io import TextIOWrapper
from typing import Tuple

from numpy import true_divide

def read_cran_documents():
    with open('scr\\data_sets\\cran\\cran.all.1400', 'r') as file:
        documents = []
        try:
            _read_i(file)
            not_finished = True
            while not_finished:
                title = _read_t(file)
                _read_a(file)
                _read_b(file)
                text, not_finished = _read_w(file)
                documents.append((title,text))
            return documents
        except ReadingError as error:
            print('Error: ', error)
            return []
            
def read_cran_queries():
    with open('scr\\data_sets\\cran\\cran.qry', 'r') as file:
        queries = []
        try:
            _read_i(file)
            not_finished = True
            while not_finished:
                text, not_finished = _read_w(file)
                queries.append(text)
            return queries
        except ReadingError as error:
            print('Error: ', error)
            return []

def _read_i(file: TextIOWrapper):
    line = file.readline()
    if not line.startswith('.I'):
        raise ReadingError('Expected .I')

def _read_t(file: TextIOWrapper) -> str:
    line = file.readline()
    if not line.startswith('.T'):
        raise ReadingError('Expected .T')
    title = ''
    while True:
        line = file.readline().removesuffix('\n')
        if line.startswith('.A'):
            return title
        title += line

def _read_a(file: TextIOWrapper):
    while True:
        line = file.readline()
        if line.startswith('.B'):
            break

def _read_b(file: TextIOWrapper):
    while True:
        line = file.readline()
        if line.startswith('.W'):
            break

def _read_w(file: TextIOWrapper):
    text = ''
    while True:
        line = file.readline().removesuffix('\n')
        if line.startswith('.I'):
            return text, True
        if line == '':
            return text, False
        text += line

class ReadingError(LookupError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)