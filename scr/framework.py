import math
import pickle

from scr.utils import DocumentCollection, Query


class VectorFramework:
    def __init__(self, document_collection: DocumentCollection, load_document=True):
        self.alpha = 0.4
        self.similarity_umbral = 0.8
        if load_document:
            try:
                with open('document_collection.pickle', 'rb') as infile:
                    document_collection = pickle.load(infile)
            except FileNotFoundError:
                self._process_and_save_dc(document_collection)
        else:
            self._process_and_save_dc(document_collection)

        self.document_collection = document_collection

    def _process_and_save_dc(self, document_collection):
        self.document_collection = document_collection
        self.compute_documents_weights()
        with open('document_collection.pickle', 'wb') as outfile:
            pickle.dump(document_collection, outfile)

    def _get_max_freq_in_document(self, document_id):
        dc = self.document_collection
        maximum = 0
        for doc_id, term_id in dc.frequencies.keys():
            if doc_id == document_id:
                maximum = max(maximum, dc.frequencies[doc_id, term_id])
        return maximum

    def _compute_tf(self, document_id, term_id):
        dc = self.document_collection
        max_freq = self._get_max_freq_in_document(document_id)
        try:
            freq = dc.frequencies[(document_id, term_id)]
        except KeyError:
            freq = 0
        return freq/max_freq

    def _get_amount_of_doc_that_have_term(self, term_id):
        dc = self.document_collection
        amount = 0
        for doc_id in dc.d_id2name.keys():
            try:
                _ = dc.frequencies[doc_id, term_id]
                amount = amount + 1
            except KeyError:
                pass
        return amount

    def _compute_idf(self, term_id):
        doc_amount = len(self.document_collection.d_id2name)
        docs_in_which_appear = self._get_amount_of_doc_that_have_term(term_id)
        return math.log(doc_amount/docs_in_which_appear, 10)

    def _compute_document_weight(self, document_id, term_id):
        dc = self.document_collection
        tf = self._compute_tf(document_id, term_id)
        idf = dc.idf[term_id]
        return tf * idf

    def compute_documents_weights(self):
        dc = self.document_collection

        for term_id in dc.t_id2name.keys():
            dc.idf[term_id] = self._compute_idf(term_id)
        for doc_id in dc.d_id2name.keys():
            for term_id in dc.t_id2name.keys():
                weight = self._compute_document_weight(doc_id, term_id)
                dc.weights_doc[doc_id, term_id] = weight

    def compute_query_weights(self, query: Query):
        dc = self.document_collection
        max_freq = max(query.frequencies.values())
        for term_name in dc.t_name2id.keys():
            term_id = dc.t_name2id[term_name]
            try:
                q_term_freq = query.frequencies[term_name]
            except KeyError:  # Term it's not in query
                q_term_freq = 0
            a = self.alpha + (1-self.alpha) * q_term_freq / max_freq
            b = dc.idf[term_id]
            query.weights[term_id] = a * b
        return query

    def _sim_of_document(self, document_id, query: Query):
        dc = self.document_collection

        a = 0  # refers to numerator in similarity equation
        b = 0
        c = 0
        for term_id in dc.t_id2name.keys():
            q_weight = query.weights[term_id]
            d_weight = dc.weights_doc[(document_id, term_id)]
            a = a + q_weight * d_weight
            b = b + d_weight * d_weight
            c = c + q_weight * q_weight
        b = math.sqrt(b)
        c = math.sqrt(c)

        return a / (b * c)

    def find(self, query: Query):
        self.compute_query_weights(query)
        documents_similarity = {}  # sim : document_id
        for doc_id in self.document_collection.d_id2name.keys():
            similarity = self._sim_of_document(doc_id, query)
            if similarity > self.similarity_umbral:
                try:
                    doc_list = documents_similarity[str(similarity)]
                    doc_list.append(doc_id)
                except KeyError:
                    documents_similarity[str(similarity)] = [doc_id]

        similarities_selected = list(documents_similarity.keys())
        similarities_selected.sort()
        return_list_id = []
        for val in similarities_selected:
            return_list_id.extend(documents_similarity[val])

        return_list_name = []
        for doc_id in return_list_id:
            return_list_name.append(self.document_collection.d_id2name[doc_id])
        return return_list_name
