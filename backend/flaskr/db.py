import sqlite3
import os

import click
from flask import current_app, g


def init_app(app):
	# Make sure the app closes the db connection on teardown
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(clear_db_command)

# Create new database connection if one doesn't yet exist
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db

# Remove the database connection
def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


# ====================== Init the database ======================
@click.command('init-db')
def init_db_command():
	"""Create new tables if they don't exist yet."""
	try:
		init_db()
		click.echo('Initialized the database.')
	except sqlite3.OperationalError as err:
		print("Error occured while trying to create the database.")
		print(err)


def init_db():
	db = get_db()
	db.execute(
		'CREATE TABLE documents ('
			'id INTEGER PRIMARY KEY AUTOINCREMENT,'
			'file_name TEXT NOT NULL,'
			'document_type_name TEXT NOT NULL,'
			'json_string TEXT NOT NULL,'
			'timestamp DATETIME DEFAULT (cast(strftime(\'%s\', \'now\') as int)))'
		)
	db.execute(
		'CREATE TABLE document_type_names ('
			'id INTEGER PRIMARY KEY AUTOINCREMENT,'
			'document_type_name TEXT NOT NULL)'
		)
	db.execute(
		'INSERT INTO document_type_names (document_type_name)'
		'VALUES (\'api_test\')'
	)
	db.execute(
		'INSERT INTO document_type_names (document_type_name)'
		'VALUES (\'incorrect_type\')'
	)
	db.commit()

# ====================== Clear the database of all files ======================
@click.command('clear-db')
def clear_db_command():
	"""Clear table "documents" in the database"""

	clear_documents_table()
	clear_document_names_table()
	
	click.echo('Cleared table "documents".')

def clear_documents_table():
	db = get_db()
	db.execute(
		'DELETE FROM documents'
	)
	db.commit()

def clear_document_names_table():
	db = get_db()
	db.execute(
		'DELETE FROM document_type_names'
	)
	db.commit()
