import json
import requests
import base64

from flask import (
	Blueprint,
	request,
	current_app,
	jsonify,
	)
# Used for reusing the db connection
from flaskr.db import get_db

# Predefined response 
class Response:
	def __init__(self, successful=False, msg='', data=None):
		self.successful = successful
		self.msg = msg
		self.data = data
	
	def serialize(self):
		'''Used to send as json response'''
		return {
			'successful' : self.successful,
			'msg' : self.msg,
			'data' : self.data
		}


bp = Blueprint('api', __name__)

@bp.route("/", methods = ['GET'])
def index():
	return "Hello world :)"

@bp.route("/process", methods = ['POST'])
def procecess_document():
	""" Process the incoming base64 string with the help of typless api.
		On success, returns the extracted document info in json format.
	"""	
	# Create default response object
	resp = Response()

	# Read the request values
	file = request.files.get('file', None)
	file_name = request.form.get('file_name', None)
	document_type_name = request.form.get('document_type_name', None)


	# Perform basic input checking
	if not file or not file_name or not document_type_name:
		resp.msg = 'Please provide the base64 string, file name and document type of the document you wish to extract data from.'
		return resp.serialize(), 400

	try:
		base64_string = base64.b64encode(file.read()).decode('utf-8')
	except:
		resp.msg = 'There was a problem converting your file to base64'
		return resp.serialize(), 400


	
	# Build request for typless
	payload = {
		"file": base64_string,
		"file_name": file_name,
		"document_type_name": document_type_name,
	}

	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": 'Token ' + current_app.config['TYPLESS_API_KEY']
	}

	url = 'https://developers.typless.com/api/extract-data'
	
	typless_resp = requests.post(url, json=payload, headers=headers)

	if typless_resp.status_code != 200:
		resp.msg = 'There was an error processing the document with typless api. Check the console for more details.'
		resp.data = typless_resp.json()

		return resp.serialize(), typless_resp.status_code


	# If there was no error up to this point, we had success.
	resp.successful = True
	resp.msg = "Document was succesfully processed by Typless."
	resp.data = typless_resp.json()

	return resp.serialize(), 201


@bp.route("/documents", methods = ['GET'])
def get_all_documents():
	""" Return all saved documents from the database.
	"""	
	# Get all posts from database
	db = get_db()
	rows = db.execute(
		'SELECT *'
		'FROM documents'
	).fetchall()

	# Create default response object
	resp = Response()

	if rows is not None:
		resp.successful = True
		resp.data = [dict(row) for row in rows]
	else:
		resp.msg = 'Error occured while getting documents from database'

	return resp.serialize(), 200

@bp.route("/documents", methods = ["POST"])
def save_document():
	""" Save the document from request into database.
	"""	
	# Create default response object
	resp = Response()

	# Get the fields from request
	req_json = request.get_json()

	file_name = req_json['file_name']
	document_type_name =req_json['document_type_name']
	json_string = req_json['json_string']

	# Some basic input checking
	if not file_name or not document_type_name or not json_string:
		resp.msg = 'file_name, document_type_name and json_string are required fields.'
		return resp.serialize(), 400


	#! Convert json to string before saving to db
	try:
		print(type(json_string))
		json_string = json.dumps(json_string)
	except:
		resp.msg = 'Problem occured while stringifying json.'
		return resp.serialize(), 400

	# Insert and acquire the inserted row
	db = get_db()
	rows = db.execute(
		'INSERT INTO documents (file_name, document_type_name, json_string)'
		'VALUES (?, ?, ?) RETURNING *', [file_name, document_type_name, json_string,]
	).fetchall()
	db.commit()
	
	if rows is not None:
		resp.successful = True
		resp.msg = 'Document was succesfuly saved into the database.'
		resp.data = dict(rows[0])
	else:
		resp.msg = 'Error occured while getting documents from database'

	return resp.serialize(), 201

@bp.route("/document_type_names", methods = ["GET"])
def get_types():
	""" Return all document type names used for selecting the correct model for typless api.
	"""	

	# Get all posts from database
	db = get_db()
	rows = db.execute(
		'SELECT *'
		'FROM document_type_names'
	).fetchall()

	# Create default response object
	resp = Response()

	if rows is not None:
		resp.successful = True
		resp.data = [dict(row) for row in rows]
	else:
		resp.msg = 'Error occured while getting document type names from database'

	return resp.serialize(), 200