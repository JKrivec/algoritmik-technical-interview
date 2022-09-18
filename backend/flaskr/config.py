"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


DEBUG=True
DATABASE_NAME='db.sqlite'
TYPLESS_API_KEY=environ.get('API_KEY')