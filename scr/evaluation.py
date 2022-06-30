import numpy as np
import matplotlib.pyplot as plt

from typing import List
from read_content import get_dataset
from utils import DocumentCollection
from framework import VectorFramework
from boolean_framework import BooleanFramework


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
            ds_doc = dataset_doc_rel_list[j][0]

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
        precision_per_query.append(p)

        if rr == 0 and nr == 0:
            r = 0
        else:
            r = round(rr/(rr+nr), 2)
        recall_per_query.append(r)

        if p == 0 and r == 0:
            f1 = 0
        else:
            f1 = round(2*p*r/(p+r), 2)
        f1_per_query.append(f1)

    return precision_per_query, recall_per_query, f1_per_query


def vary_fw_similarity(dataset_name):
    documents, queries, dataset_queries_results = get_dataset(dataset_name)

    # from 0 - 0.9 similarity
    mean_precision = []
    mean_recall = []
    mean_f1 = []

    f = VectorFramework(f'dc_{dataset_name}')
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

    _graph_similarity_mean(mean_precision, "Precision", "Vector", dataset_name)
    _graph_similarity_mean(mean_recall, "Recall", "Vector", dataset_name)
    _graph_similarity_mean(mean_f1, "F1", "Vector", dataset_name)


def _graph_similarity_mean(mean_list, evaluation_name, model, dataset_name):
    similarity = np.arange(0, 1, 0.1)

    plt.xlabel("similarity")
    plt.ylabel(f'mean {evaluation_name}')
    plt.title(f'{model} framework, {dataset_name}')
    plt.plot(similarity, mean_list)
    plt.legend(loc="lower left")
    plt.show()

    pass


def compare_models(dataset_name):
    _, queries, dataset_queries_results = get_dataset(dataset_name)

    vf = VectorFramework(f'dc_{dataset_name}')
    bf = BooleanFramework(f'dc_{dataset_name}')

    vectorf_qrel_list = []
    booleanf_qrel_list = []
    for i in range(len(queries)):
        _, _, vf_qrel = vf.find(queries[i])
        _, _, bf_qrel = bf.find(queries[i])
        vectorf_qrel_list.append(vf_qrel)
        booleanf_qrel_list.append(bf_qrel)

    vf_precision, vf_recall, vf_f1 = evaluate(vectorf_qrel_list, dataset_queries_results)
    bf_precision, bf_recall, bf_f1 = evaluate(booleanf_qrel_list, dataset_queries_results)

    _graph_models_evaluation(vf_precision, bf_precision, "Precision", dataset_name)
    _graph_models_evaluation(vf_recall, bf_recall, "Recall", dataset_name)
    _graph_models_evaluation(vf_f1, bf_f1, "F1", dataset_name)


def _graph_models_evaluation(vector_queries, boolean_queries, evaluation_name, dataset_name):
    plt.xlabel("query_id")
    plt.ylabel(f'mean {evaluation_name}')
    plt.title(f'{dataset_name} dataset, {evaluation_name} comparison')
    plt.plot(np.arange(len(vector_queries)), vector_queries, label="Vector")
    plt.plot(np.arange(len(boolean_queries)), boolean_queries, label="Boolean")
    plt.legend(loc="upper left")
    plt.show()


def show_boolean_means(dataset_name: str):
    _, queries, dataset_queries_results = get_dataset(dataset_name)

    bf = BooleanFramework(f'dc_{dataset_name}')

    booleanf_qrel_list = []
    for i in range(len(queries)):
        _, _, bf_qrel = bf.find(queries[i])
        booleanf_qrel_list.append(bf_qrel)

    bf_precision, bf_recall, bf_f1 = evaluate(booleanf_qrel_list, dataset_queries_results)


def _graph_boolean_means(bf_precision, bf_recall, bf_f1):
    plt.xlabel("metric")
    plt.ylabel(f'mean')
    plt.title(f'{dataset_name} dataset, metric comparison')
    plt.plot(1, bf_precision, label="Precision")
    plt.plot(2, bf_recall, label="Recall")
    plt.plot(3, bf_f1, label="F1")
    plt.legend(loc="upper left")
    plt.show()