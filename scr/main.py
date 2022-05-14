from read_content import read_dataset, read_query
from utils import DocumentCollection, Query
from framework import VectorFramework

print('PLEASE ENTER PATH TO DATA SET')
doc_path = input()
print('PLEASE ENTER QUERY')
query = input()

filtered_doc_list = read_dataset(doc_path)
filtered_query_list = read_query(query)

# d1 = Document('d1', ['leon', 'leon', 'leon'])
# d2 = Document('d2', ['leon', 'leon', 'leon', 'zorro'])
# d3 = Document('d3', ['leon', 'zorro', 'nutria'])
# d4 = Document('d4', ['leon', 'leon', 'leon', 'zorro', 'zorro', 'zorro'])
# d5 = Document('d5', ['nutria'])


document_collection = DocumentCollection()
document_collection.add_documents(filtered_doc_list)
query = Query()
query.add_terms(filtered_query_list)

f = VectorFramework(document_collection)
retrieve = f.find(query)

print(retrieve)
