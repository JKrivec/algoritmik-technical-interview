from flask import Flask
from flask_cors import CORS
import os



def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=False)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=False)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	app.config.from_mapping(
		DATABASE=os.path.join(app.instance_path, app.config['DATABASE_NAME']),
	)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Init the database connection
	from . import db
	db.init_app(app)

	from . import api
	app.register_blueprint(api.bp)

	# Enable cross-origin resource sharing
	#! This allows access from all addresses
	CORS(app)
	
	return app
