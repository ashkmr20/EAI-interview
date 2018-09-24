from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

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
		results = es.search(index="address_book", body={"query": {"match": {'name': name}}})
		return (jsonify(results['hits']['hits']))#[0]['_source']))


	elif request.method== "DELETE" and name:
		results = es.delete_by_query(index='address_book',doc_type='address', body={"query": {"match": {'name': name}}})
		if results['deleted']==0:
			raise InvalidUsage("Error: User to be deleted can't be found.", status_code=400)
		return jsonify(results)
	elif request.method=="PUT" and name:
		try:
			new_phone_no = request.form['phone_no']
		except:
			new_phone_no=""
		body = {
			'script':
				{
					"source": "ctx._source.phone_no ='%s'"% new_phone_no,
				},
			'query': 
				{
					'match': 
						{'name': name}
				}
		}
		results = es.update_by_query(index='address_book',doc_type='address', body=body)
		if results['updated']==0:
			raise InvalidUsage("Error: User to be updated can't be found.", status_code=400)
		return jsonify(results)

# route for page GET and POST
@app.route('/contact', methods=['GET', 'POST'])
def users_page():
	if request.method == 'GET':
		page= request.args.get('page', default = 1, type = int)
		page_size= request.args.get('pageSize', default = 10, type = int)
		results = es.search(index="address_book", from_=(page-1)*10, size=page_size, body={'query' :{ 'match_all':{}}})
		return jsonify(results)
	elif request.method == 'POST':
		try:
			name = request.form['name']
		except:
			return ("Error: No user name")
		try:
			phone_no = request.form['phone_no']
		except:
			phone_no=""
		body = {
			'name': name,
			'phone_no': phone_no,
		}
		result = es.index(index='address_book', doc_type='address', id=es_data.i, body=body)
		es_data.i+=1
		return jsonify(result)


app.run(port=5000, debug=True)
