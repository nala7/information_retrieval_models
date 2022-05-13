from scr.utils import DocumentCollection
from scr.framework import VectorFramework


def test1():
    dc = DocumentCollection()

    dc.frequencies[1, 1] = 3
    dc.frequencies[2, 1] = 3
    dc.frequencies[2, 2] = 1
    dc.frequencies[3, 1] = 1
    dc.frequencies[3, 2] = 1
    dc.frequencies[3, 3] = 1
    dc.frequencies[4, 1] = 3
    dc.frequencies[4, 2] = 3
    dc.frequencies[5, 3] = 1

    dc.t_name2id = {'leon': 1, 'zorro': 2, 'nutria': 3}
    dc.t_id2name = {1: 'leon', 2: 'zorro', 3: 'nutria'}

    dc.d_name2id = {'d1': 1, 'd2': 2, 'd3': 3, 'd4': 4, 'd5': 5}
    dc.d_id2name = {1: 'd1', 2: 'd2', 3: 'd3', 4: 'd4', 5: 'd5'}

    vf = VectorFramework(dc)
    dc = vf.document_collection

    print(dc)
