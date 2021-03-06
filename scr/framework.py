import math
import pickle

from utils import DocumentCollection, Query


class VectorFramework:
    def __init__(self, dc_name, document_collection = None):
        self.alpha = 0.4
        self.similarity_umbral = 0.5
        if document_collection is None:
            with open(f'document_collection/{dc_name}_vector.pickle', 'rb') as infile:
                document_collection = pickle.load(infile)
        else:
            self._process_and_save_dc(document_collection, dc_name)
        self.document_collection = document_collection

    def _process_and_save_dc(self, document_collection, dc_name):
        self.document_collection = document_collection
        self.compute_documents_weights()
        with open(f'document_collection/{dc_name}_vector.pickle', 'wb') as outfile:
            pickle.dump(document_collection, outfile)

    def _compute_tf(self, document_id, term_id):
        dc = self.document_collection
        max_freq = dc.max_frequency
        freq = dc.frequencies[(document_id, term_id)]
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

        i = 1
        total = len(dc.t_id2name.keys())
        for term_id in dc.t_id2name.keys():
            print('IDF: ', i, '/', total)
            i += 1
            dc.idf[term_id] = self._compute_idf(term_id)

        i = 1
        total = len(dc.frequencies.keys())
        for doc_id, term_id in dc.frequencies.keys():
            print('Document Weight: ', i, '/', total)
            i += 1
            weight = self._compute_document_weight(doc_id, term_id)
            dc.weights_doc[doc_id, term_id] = weight

    def compute_query_weights(self, query: Query):
        dc = self.document_collection
        max_freq = max(query.frequencies.values())
        for term_name in query.frequencies.keys():
            try:
                term_id = dc.t_name2id[term_name]
                q_term_freq = query.frequencies[term_name]
                a = self.alpha + (1 - self.alpha) * q_term_freq / max_freq
                b = dc.idf[term_id]
                query.weights[term_id] = a * b
            except KeyError:  # term is not in vocabulary
                continue
        return query

    def _sim_of_document(self, document_id, query: Query):
        dc = self.document_collection

        a = 0  # refers to numerator in similarity equation
        b = 0
        c = 0
        for term_id in list(query.weights.keys()) + dc.terms_id_of_document_id[document_id]:
            try:
                q_weight = query.weights[term_id]
            except KeyError:
                q_weight = 0
            try:
                d_weight = dc.weights_doc[(document_id, term_id)]
            except KeyError:
                d_weight = 0
            a = a + q_weight * d_weight
            b = b + d_weight * d_weight
            c = c + q_weight * q_weight
        b = math.sqrt(b)
        c = math.sqrt(c)

        if b == 0 or c == 0:  # document is empty, or query have no term of vocabulary
            return 0
        return a / (b * c)

    def find(self, query: Query):
        self.compute_query_weights(query)
        documents_similarity = {}  # sim : document_id
        for doc_id in self.document_collection.d_id2name.keys():
            similarity = self._sim_of_document(doc_id, query)
            if similarity >= self.similarity_umbral:
                try:
                    doc_list = documents_similarity[str(similarity)]
                    doc_list.append(doc_id)
                except KeyError:
                    documents_similarity[str(similarity)] = [doc_id]

        similarities_selected = list(documents_similarity.keys())
        similarities_selected.sort(reverse=True)
        return_list_id = []
        return_doc_id_val = []
        for val in similarities_selected:
            return_list_id.extend(documents_similarity[val])
            for doc_id in documents_similarity[val]:
                return_doc_id_val.append((int(doc_id), float(val)))

        return_list_name = []
        for doc_id in return_list_id:
            return_list_name.append(self.document_collection.d_id2name[doc_id])

        return return_list_name, return_list_id, return_doc_id_val
