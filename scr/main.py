from os import getcwd

# from read_content import read_dataset, read_query
from utils import DocumentCollection, Query, Document
from framework import VectorFramework

print('PLEASE ENTER PATH TO DATA SET')
# doc_path = input()
# doc_path = getcwd() + "\\test"
# print('PLEASE ENTER QUERY')
# query = input()
# query = "jesus god church good pray"

# filtered_doc_list = read_dataset(doc_path)
# filtered_query_list = read_query(query)

# d1 = Document('d1', ['leon', 'leon', 'leon'])
# d2 = Document('d2', ['leon', 'leon', 'leon', 'zorro'])
# d3 = Document('d3', ['leon', 'zorro', 'nutria'])
# d4 = Document('d4', ['leon', 'leon', 'leon', 'zorro', 'zorro', 'zorro'])
# d5 = Document('d5', ['nutria'])


document_collection = DocumentCollection()
document_collection.add_documents('LIST OF DOCUMENT')
query = Query()
query.add_terms('LIST OF STR (TERMS)')

f = VectorFramework(document_collection)
retrieve = f.find(query)

print(retrieve)
