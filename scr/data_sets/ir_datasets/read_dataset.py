import ir_datasets


dataset = ir_datasets.load('msmarco-passage/train')
# Documents
for doc in dataset.docs_iter():
    print(doc)