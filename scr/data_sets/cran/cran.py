from io import TextIOWrapper


def read_cran_documents():
    import os
    cur_dir = os.getcwd()
    print(cur_dir)
    with open(cur_dir+'/data_sets/cran/cran.all.1400', 'r') as file:
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
    import os
    cur_dir = os.getcwd()
    print(cur_dir)
    with open(cur_dir+'/data_sets/cran/cran.qry', 'r') as file:
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
