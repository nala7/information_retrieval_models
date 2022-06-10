import re


def extract_info(path_docs: str, path_qry: str, path_rel: str):
    with open(path_docs) as doc_file:
        docs = doc_file.read()
        parse_docs(docs)

    with open(path_qry) as qry_file:
        queries = qry_file.read()
        parse_queries(queries)


def parse_docs(text: str):
    tokens = text.split()
    docs = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '.W':
            j = i + 1
            current_doc = ""
            while j < len(tokens) and not tokens[j] == '.I':
                current_doc += tokens[j]
                j += 1
            docs.append(current_doc)
            i = j + 1
        i += 1
    print(f'Docs read: {len(docs)}')


# returns a list of queries in order
def parse_queries(text: str):
    queries = re.split('.I \d+\n.W', text)[1:]
    print(f'Queries read: {len(queries)}')
    print(queries[0])


path_docs = "cran/cran.all.1400"
path_qry = "cran/cran.qry"
extract_info(path_docs, path_qry, "")
