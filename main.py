from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import es_search as es_search

host= input("Elasticsearch Host: ")
port= input("Elasticsearch Port: ")

try:
	es = Elasticsearch([{'host': host, 'port': port}])
except:
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__)


# class to keep track of id numbers in ES
class data_stats:
	def __init__(self):
		self.i=0
es_data = data_stats()
#es.indices.delete(index='address_book', ignore=[400, 404])

# Custom error for invalid delete/update user
class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code="", payload=""):
        Exception.__init__(self)
        self.message = message
        if status_code is not "":
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#route for single GET, PUT and DELETE operations
@app.route('/contact/<name>', methods=['GET', 'POST','DELETE','PUT'])
def user(name):
	if request.method == 'GET' and name:
		return jsonify(es_search.single_get(es,'address_book', name))

	elif request.method== "DELETE" and name:
		results = es_search.delete_doc(es, 'address_book',name)
		if results==-1:
			raise InvalidUsage("Error: User to be deleted can't be found.", status_code=400)
		return jsonify(results)
	elif request.method=="PUT" and name:
		try:
			new_phone_no = request.form['phone_no']
		except:
			new_phone_no=""
		try:
			new_address = request.form['new_address']
		except:
			new_address=""			
		results = es_search.update_doc(es, 'address_book', name, new_phone_no, new_address)
		if results==-1:
			raise InvalidUsage("Error: User to be updated can't be found.", status_code=400)
		if results==-2:
			raise InvalidUsage("Error: Neither field was updated", status_code=390)			
		return jsonify(results)

# route for paged GET and single POST
@app.route('/contact', methods=['GET', 'POST'])
def users_page():
	if request.method == 'GET':
		page= request.args.get('page', default = 1, type = int)
		page_size= request.args.get('pageSize', default = 10, type = int)
		return jsonify(es_search.paged_get(es, "address_book", page, page_size))

	elif request.method == 'POST':
		try:
			name = request.form['name']
		except:
			return ("Error: No user name")
		try:
			phone_no = request.form['phone_no']
		except:
			phone_no=""
		try:
			address = request.form['address']
		except:
			address=""
		result = es_search.insert_doc(es, 'address_book', name, phone_no, address, es_data.i)
		es_data.i+=1
		return jsonify(result)


app.run(port=5000, debug=True)
