from read_content import read_dataset, read_query

print('PLEASE ENTER PATH TO DATA SET')
doc_path = input()
print('PLEASE ENTER QUERY')
query = input()

filtered_doc_list = read_dataset(doc_path)
filtered_query = read_query(query)
