from read_content import read_dataset, read_query, get_cran_dataset
from data_sets.cran.cran import read_cran_rel
from evaluation import evaluate, _graph_similarity_mean, vary_fw_similarity

# from test import test1
from utils import DocumentCollection, Query
from framework import VectorFramework

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
#
# documents, queries = get_cran_dataset()
# document_collection = DocumentCollection(documents)
#
# f = VectorFramework(document_collection)
#
# model_queries_results = []
# for i in range(len(queries)):
#     names, ids, ids_vals = f.find(queries[i])
#     model_queries_results.append(ids_vals)
#
# dataset_queries_results = read_cran_rel()
#
# precision, recall, f1 = evaluate(model_queries_results, dataset_queries_results)
#
# _graph_similarity_mean(precision, "precision", "vector")

vary_fw_similarity()

# test1()
print('Done!')
