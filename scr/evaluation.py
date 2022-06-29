import numpy as np

from typing import List
from read_content import get_cran_dataset
from data_sets.cran.cran import read_cran_rel
from utils import DocumentCollection
from framework import VectorFramework


def evaluate(model_queries: List, dataset_queries: List):
    precision_per_query = []
    recall_per_query = []
    f1_per_query = []
    for query_id in range(len(model_queries)):
        model_doc_rel_list = model_queries[query_id]
        model_doc_rel_list.sort()
        dataset_doc_rel_list = dataset_queries[query_id]
        dataset_doc_rel_list.sort()

        rr = 0
        ri = 0
        nr = 0
        i = 0
        j = 0
        while True:
            if i == len(model_doc_rel_list):
                # All recalled docs were analyzed
                break
            if j == len(dataset_doc_rel_list):
                # The rest of recalled documents are irrelevant
                ri += len(model_doc_rel_list) - i
                break

            model_doc = model_doc_rel_list[i][0]
            print(model_doc)
            ds_doc = dataset_doc_rel_list[j][0]
            print(ds_doc)

            if model_doc == ds_doc:  # It's a match
                rr += 1
                i += 1
                j += 1
            if model_doc > ds_doc:  # A doc wasn't retrieved
                nr += 1
                j += 1
            if model_doc < ds_doc:  # A relevant doc wasn't retrieved
                ri += 1
                i += 1

        if rr == 0 and ri == 0:
            p = 0
        else:
            p = round(rr/(rr + ri), 2)
        print(p)
        precision_per_query.append(p)

        if rr == 0 and nr == 0:
            r = 0
        else:
            r = round(rr/(rr+nr), 2)
        print(r)
        recall_per_query.append(r)

        if p == 0 and r == 0:
            f1 = 0
        else:
            f1 = round(2*p*r/(p+r), 2)
        f1_per_query.append(f1)

    return precision_per_query, recall_per_query, f1_per_query


def vary_fw_similarity():
    documents, queries = get_cran_dataset()
    document_collection = DocumentCollection(documents)
    dataset_queries_results = read_cran_rel()

    # from 0 - 0.9 similarity
    mean_precision = []
    mean_recall = []
    mean_f1 = []

    f = VectorFramework(document_collection)
    for umbral in np.arange(0, 1, 0.1):
        f.similarity_umbral = umbral
        model_queries_results = []
        for i in range(len(queries)):
            names, ids, ids_vals = f.find(queries[i])
            model_queries_results.append(ids_vals)
        precision, recall, f1 = evaluate(model_queries_results, dataset_queries_results)

        mean_precision.append(sum(precision)/len(precision))
        mean_recall.append((sum(recall)/len(recall)))
        mean_f1.append(sum(f1)/len(f1))

    _graph_similarity_mean(mean_precision, "Precision", "Vector")
    _graph_similarity_mean(mean_recall, "Recall", "Vector")
    _graph_similarity_mean(mean_f1, "F1", "Vector")


def _graph_similarity_mean(mean_list, evaluation_name, model):
    import matplotlib.pyplot as plt

    similarity = np.arange(0, 1, 0.1)

    plt.xlabel("similarity")
    plt.ylabel(f'mean {evaluation_name}')
    plt.title(f'{model} framework')
    plt.plot(similarity, mean_list)
    plt.legend()
    plt.show()

    pass
