import functools
from flask import (
	Blueprint,
	flash,
	g,
	redirect,
	render_template,
	request,
	session,
	url_for
	)
from flaskr.db import get_db

bp = Blueprint('api', __name__)

@bp.route("/", methods = ['GET'])
def index():
	return "Hello world :)"

@bp.route("/strings", methods = ['GET'])
def showStrings():
	db = get_db()
	posts = db.execute(
		'SELECT id, string'
		'FROM test'
	).fetchall()

	return posts

@bp.route("/strings", methods = ["POST"])
def saveString():
	error = None
	string = request.form["string"]

	if not string:
		error = 'Title is required.'

	if error is not None:
			return "Wrong request form."
	else:
		db = get_db()
		db.execute(
			'INSERT INTO test (string)'
			' VALUES (?)',
			(string)
		)
		db.commit()

	return "Succesfuly inserted a string."
