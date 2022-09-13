import json
from flask import (
	Blueprint,
	request,
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

@bp.route("/strings", methods = ['GET'])
def get_all_strings():
	# Get all posts from database
	db = get_db()
	rows = db.execute(
		'SELECT *'
		'FROM test'
	).fetchall()

	# Create default response object
	resp = Response()

	if rows is not None:
		resp.successful = True
		print(rows[0])
		resp.data = [dict(row) for row in rows]
	else:
		resp.msg = 'Error occured while getting posts from database'

	return resp.serialize(), 200

@bp.route("/strings", methods = ["POST"])
def save_string():
	# Create default response object
	resp = Response()
	# Get the string from request form
	string = request.form["string"]
	
	if not string:
		resp.msg = 'Title is required.'
		return resp.serialize(), 400
	else:
		db = get_db()
		db.execute(
			'INSERT INTO test (string)'
			'VALUES (?)',
			[string]
		)
		db.commit()

	resp.successful = True
	resp.msg = "Succesfuly inserted a string."

	return resp.serialize(), 201
