from elasticsearch import Elasticsearch
from flask import current_app

def single_get(index, name):
	results = es.search(index="address_book", body={"query": {"match": {'name': name}}})

def paged_get(index, address):
	if not current_app.elasticsearch:
        return


def insert_doc(index, address, id):
	if not current_app.elasticsearch:
        return
	result = es.index(index='address_book', doc_type='address', id=es_data.i, body=body)
