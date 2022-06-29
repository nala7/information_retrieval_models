from io import TextIOWrapper


def read_cran_documents():
    with open('data_sets/cran/cran.all.1400', 'r') as file:
        documents = []
        try:
            id = _read_i(file)
            not_finished = True
            while not_finished:
                title = _read_t(file)
                _read_a(file)
                _read_b(file)
                text, not_finished, new_id = _read_w(file)
                documents.append((id, title, text))
                id = new_id
            return documents
        except ReadingError as error:
            print('Error: ', error)
            return []


def read_cran_queries():
    with open('data_sets/cran/cran.qry', 'r') as file:
        queries = []
        try:
            id = _read_i(file)
            not_finished = True
            while not_finished:
                file.readline()  # Skip .W line
                text, not_finished, new_id = _read_w(file)
                queries.append((id, text))
                id = new_id
            return queries
        except ReadingError as error:
            print('Error: ', error)
            return []


def read_cran_rel():
    with open('data_sets/cran/cranqrel', 'r') as file:
        # each position in the list represents the id of a query
        # it's a list of list. For each query theres a list of tuples <doc, rel>
        queries = [[] for _ in range(225)]
        while True:
            line = file.readline().split()
            if not line:
                break
            query_id, doc_id, rel = line
            query_id = int(query_id)
            queries[query_id - 1].append((int(doc_id), int(rel)))
    return queries


def _read_i(file: TextIOWrapper):
    line = file.readline()
    if not line.startswith('.I'):
        raise ReadingError('Expected .I')
    id_literal = line.split()[1]
    return int(id_literal)


def _read_t(file: TextIOWrapper) -> str:
    line = file.readline()
    if not line.startswith('.T'):
        raise ReadingError('Expected .T')
    title = ''
    while True:
        line = file.readline().removesuffix('\n')
        if line.startswith('.A'):
            return title
        title += line


def _read_a(file: TextIOWrapper):
    while True:
        line = file.readline()
        if line.startswith('.B'):
            break


def _read_b(file: TextIOWrapper):
    while True:
        line = file.readline()
        if line.startswith('.W'):
            break


def _read_w(file: TextIOWrapper):
    text = ''
    while True:
        line = file.readline().removesuffix('\n')
        if line.startswith('.I'):
            return text, True, int(line.split()[1])
        if line == '':
            return text, False, -1
        text += ' ' + line


class ReadingError(LookupError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


read_cran_rel()
