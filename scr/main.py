from read_content import read_dataset, read_query
from utils import DocumentCollection, Query

print('PLEASE ENTER PATH TO DATA SET')
doc_path = input()
print('PLEASE ENTER QUERY')
query = input()

filtered_doc_list = read_dataset(doc_path)
filtered_query_list = read_query(query)

document_collection = DocumentCollection().add_documents(filtered_doc_list)
query = Query().add_terms(filtered_query_list)
