from utils import DocumentCollection, Query, Document
from framework import VectorFramework


def test1():
    d1 = Document(1, 'd1', ['leon', 'leon', 'leon'])
    d2 = Document(2, 'd2', ['leon', 'leon', 'leon', 'zorro'])
    d3 = Document(3, 'd3', ['leon', 'zorro', 'nutria'])
    d4 = Document(4, 'd4', ['leon', 'zorro', 'leon', 'zorro'])
    d5 = Document(5, 'd5', ['nutria'])

    dc = DocumentCollection([d1, d2, d3, d4, d5])

    vf = VectorFramework(dc, load_document=False)
    q = Query(1, ['iguana', 'nutria'])

    print(vf.find(q))

    print('done')

    # dc = vf.document_collection

    # print(dc)
