from read_content import read_dataset, read_query, get_cran_dataset
# from test import test1
from utils import DocumentCollection, Query
from framework import VectorFramework
import os

# print('PLEASE ENTER PATH TO DATA SET')
# doc_path = input()
# print('PLEASE ENTER QUERY')
# query = input()

# filtered_doc_list = read_dataset(doc_path)
# filtered_query_list = read_query(query)

# # d1 = Document('d1', ['leon', 'leon', 'leon'])
# # d2 = Document('d2', ['leon', 'leon', 'leon', 'zorro'])
# # d3 = Document('d3', ['leon', 'zorro', 'nutria'])
# # d4 = Document('d4', ['leon', 'leon', 'leon', 'zorro', 'zorro', 'zorro'])
# # d5 = Document('d5', ['nutria'])


# document_collection = DocumentCollection()
# document_collection.add_documents(filtered_doc_list)
# query = Query()
# query.add_terms(filtered_query_list)

# f = VectorFramework(document_collection)
# retrieve = f.find(query)
os.chdir('scr')
a = os.getcwd()
documents, queries = get_cran_dataset()
document_collection = DocumentCollection(documents)

f = VectorFramework(document_collection)
print(f)
names, ids = f.find(queries[0])

# test1()
print('Done!')
