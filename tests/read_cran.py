import re


def extract_info(path_docs: str, path_qry: str, path_rel: str):
    with open(path_docs) as doc_file:
        docs = doc_file.read()
        print(type(docs))
        parse_docs(docs)

    with open(path_qry) as qry_file:
        queries = qry_file.read()
        print(type(queries))
        parse_queries(queries)


# returns a list of queries in order
def parse_queries(text: str):
    queries = re.split('.I \d+\n.W', text)[1:]


def parse_docs(text: str):
    docs = re.split('.I \d+\n.T\n.+?(?=.A)\n.B.+?(?=.W)')
    # docs = re.split('.I\d+\n.T\w+\n.A\w+\n.B\w+\n.W', text)
    # docs = re.findall('?=\.T', text)
    print(docs)


path_docs = "cran/cran.all.1400"
path_qry = "cran/cran.qry"
extract_info(path_docs, path_qry, "")
