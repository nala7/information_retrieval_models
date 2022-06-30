from read_content import read_dataset, read_query, get_cran_dataset, get_ir_dataset
from data_sets.cran.cran import read_cran_rel
from evaluation import evaluate, _graph_similarity_mean, vary_fw_similarity

# from test import test1
from utils import DocumentCollection, Query
from framework import VectorFramework
import os


# print('····································································')
# print('················SISTEMA DE EXTRACCIÓN DE INFORMACIÓN················')
# print('····································································')
# print('··············· Nadia Glez  &  Alejandro Labourdette ···············')
# print('····································································')
# while True:
#     print('Por favor ingrese alguna de las siguientes instrucciones:')
#     print('~ test <framework> <dataset>')
#     print('<framework>: framework a probar ("vector","boolean")')
#     print('<dataset>: dataset que será utilizado ("cran","vaswani")')

#     instruction = input('   ~ ')
#     if len(instruction.split()) == 2:
#         command, dataset = instruction.split()
#         if command == 'compare':
#             if dataset == 'cran':
#                 # Compare both models using cran dataset
#                 pass
#             else:
#                 # Compare both models using any other dataset
#                 pass
#     if len(instruction.split()) == 3:
#         command, framework, dataset = instruction.split()
#         if command == 'test':
#             if framework == 'vector':
#                 if dataset == 'cran':
#                     # Run test vector cran
#                     pass
#                 else:
#                     # Run test vector <other_dataset>
#                     pass
#             if framework == 'boolean':
#                 if dataset == 'cran':
#                     # Run test vector cran
#                     pass
#                 else:
#                     # Run test vector <other_dataset>
#                     pass

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



os.chdir('scr')
a = os.getcwd()
dataset_queries_results = get_ir_dataset('vaswani', load_from_memory=False)
#
# precision, recall, f1 = evaluate(model_queries_results, dataset_queries_results)
#
# _graph_similarity_mean(precision, "precision", "vector")

# vary_fw_similarity()

# test1()

print('Done!')
