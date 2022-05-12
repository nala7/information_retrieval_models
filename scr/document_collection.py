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


class Query:
    def __init__(self):
        # term_name : repetitions
        self.frequencies = {}

        # term_id : weight. Must be set by framework.
        # If documents don't contain some term then it will not be in dict.
        self.weights = {}
