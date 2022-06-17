from typing import List


class Document:
    def __init__(self, title, filtered_text):
        self.title = title
        self.filtered_text = filtered_text


class DocumentCollection:
    def __init__(self):
        # (id_document, id_term) : repetitions
        self.frequencies = {}

        # term_name : term_id
        self.t_name2id = {}
        # term_id : term_name
        self.t_id2name = {}
        # document_name : document_id
        self.d_name2id = {}
        # document_id : document_name
        self.d_id2name = {}

        # (id_document, term_id) : weight. Must be set by framework
        self.weights_doc = {}
        # term_id : idf_of_ti. Must be set by framework
        self.idf = {}

        self._doc_id = 1
        self._term_id = 1

    def add_documents(self, documents: List[Document]):
        for doc in documents:
            doc_id = self._doc_id
            self.d_name2id[doc.title] = doc_id
            self.d_id2name[doc_id] = doc.title
            self._doc_id += 1

            for term in doc.filtered_text:
                try:
                    term_id = self.t_name2id[term]
                    try:
                        self.frequencies[doc_id, term_id] += 1
                    except KeyError:
                        self.frequencies[doc_id, term_id] = 1
                except KeyError:
                    term_id = self._term_id
                    self.t_name2id[term] = term_id
                    self.t_id2name[term_id] = term
                    self.frequencies[doc_id, term_id] = 1
                    self._term_id += 1


class Query:
    def __init__(self, terms: List[str]):
        # term_name : repetitions
        self.frequencies = {}

        # term_id : weight. Must be set by framework.
        # If documents don't contain some term then it will not be in dict.
        self.weights = {}

        self.add_terms(terms)

    def add_terms(self, terms: List[str]):
        for term in terms:
            try:
                self.frequencies[term] += 1
            except KeyError:
                self.frequencies[term] = 1
