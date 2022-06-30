import pickle
from utils import DocumentCollection, Query


class BooleanFramework:
    def __init__(self, dc_name, document_collection: DocumentCollection = None):
        if document_collection is None:
           with open(f'document_collection/{dc_name}_boolean.pickle', 'rb') as infile:
                document_collection = pickle.load(infile)
        else:
            self._process_and_save_dc(document_collection, dc_name)
        self.document_collection = document_collection

    def _process_and_save_dc(self, document_collection, dc_name):
        self.document_collection = document_collection
        self.compute_documents_weights()
        with open(f'document_collection/{dc_name}_boolean.pickle', 'wb') as outfile:
            pickle.dump(document_collection, outfile)

    def compute_documents_weights(self):
        dc: DocumentCollection = self.document_collection

        i = 1
        total = len(dc.frequencies.keys())
        for doc_id, term_id in dc.frequencies.keys():
            print('Document Weight: ', i, '/', total)
            i += 1
            dc.weights_doc[doc_id, term_id] = 1

    def compute_query_weights(self, query: Query):
        dc = self.document_collection
        for term_name in query.frequencies.keys():
            try:
                term_id = dc.t_name2id[term_name]
                query.weights[term_id] = 1
            except KeyError:  # term is not in vocabulary
                continue
        return query

    def _sim_of_document(self, document_id, query: Query):
        dc = self.document_collection

        for term_id in list(query.weights.keys()):
            try:
                query.weights[term_id] == dc.weights_doc[document_id, term_id]
                # If not exception then they are equal because are 1
                return True
            except KeyError:
                return False

    def find(self, query: Query):
        self.compute_query_weights(query)
        response_ids = []
        response_titles = []
        response_ids_val = []
        for doc_id in self.document_collection.d_id2name.keys():
            similarity = self._sim_of_document(doc_id, query)
            if similarity: 
                response_ids.append(doc_id)
                response_ids_val.append((doc_id, 1))
                response_titles.append(self.document_collection.d_id2name[doc_id])

        return response_titles, response_ids, response_ids_val
