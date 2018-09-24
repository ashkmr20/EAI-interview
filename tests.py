import requests
import unittest
from elasticsearch import Elasticsearch
import es_search as es_search

host= input("Elasticsearch Host: ")
port= input("Elasticsearch Port: ")

try:
	es = Elasticsearch([{'host': host, 'port': port}])
except:
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

test_name=['a' for i in range(10)]
test_phone= ['0' for i in range(10)]
for i in range(10):
	#creating test data
	num_range= int(i/9)
	char_range=int(i/25)
	name=""
	phone_no=""
	address=""
	test_phone[-1-num_range]= str(int(test_phone[-1-num_range])+1)
	test_name[-1-char_range]= chr(ord(test_name[-1-char_range])+1)
	for i in test_phone:
		phone_no=phone_no+i
	for i in test_name:
		name=name+i
#name, phone aaaaa, 00000


# created a diff index for test data
results = es_search.insert_doc(es, 'test-data', name, phone_no, address, i)

#es.indices.delete(index='test-data', ignore=[400, 404])

class Test_contacts_api(unittest.TestCase):
	def test_post(self):
		results = es_search.insert_doc(es, 'test-data', "TEST", "12345", "AAA", 0)
		self.assertEqual(results['result'], 'created')
	def test_view_all(self):
		results= ((es_search.paged_get(es, "test-data", 1, 1000,"")))
		self.assertEqual(results['hits']['total'], 10)
	def test_update(self):
		results=None
		try:
			results = es_search.update_doc(es, 'test-data', "aaaaaaaaab", "55555", "New place")
		except:
			pass
		self.assertEqual(results['result'],'updated')	
	def test_update_absent_name(self):
		results=None
		try:
			results = es_search.update_doc(es, 'test-data', "122112", "55555", "New place")
		except:
			pass
		self.assertEqual(results,-1)
	def test_delete_absent_name(self):
		results = es_search.delete_doc(es, 'address_book','9202921')
		self.assertEqual(results, -1)


if __name__ == '__main__':
    unittest.main()
