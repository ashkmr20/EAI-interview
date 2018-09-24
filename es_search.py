from flask import current_app

def single_get(es, index, name):
	results = es.search(index= index, body={"query": {"match": {'name': name}}})
	return ((results['hits']['hits']))

def paged_get(es, index, page, page_size, querystr):
	results = es.search(index=index, from_=(page-1)*10, size=page_size, body={'query' :{ 'match_all':{}}})
	return results['hits']['hits']

def insert_doc(es, index, name, phone_no, address, ids):
	body = {
		'name': name,
		'phone_no': phone_no,
		'address': address
	}
	results = es.index(index=index, doc_type='contact', body=body, id=ids)
	return results
def update_doc(es, index, name, phone_no, address):
	results=-1

	# 2 separate updates so that we dont have to overwrite a field if it doesn't need to be updated
	if phone_no:
		body = {
				'script':
					{
						"source": "ctx._source.phone_no ='%s'"% phone_no,
					},
				'query': 
					{
						'match': 
							{'name': name}
					}
			}
		results = es.update_by_query(index='address_book',doc_type='contact', body=body)

	if address:
		body = {
				'script':
					{
						"source": "ctx._source.address ='%s'"% address,
					},
				'query': 
					{
						'match': 
							{'name': name}
					}
			}		
		results = es.update_by_query(index='address_book',doc_type='contact', body=body)
	if results['updated']==0:
		return -1
	return results

def delete_doc(es, index, name):
	results = es.delete_by_query(index=index,doc_type='contact', body={"query": {"match": {'name': name}}})
	if results['deleted']==0:
		return -1
	return results
