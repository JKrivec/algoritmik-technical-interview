# algoritmik-technical-intrview

Small full-stack app with VueJS front-end, Flask back-end with local SQLite database.\
Downloads and saves a document via provided api into a local database to show knowledge of simple concepts.

<br />

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) (which comes with [pip](https://pypi.org/project/pip/) package installer) and [SQLite](https://www.sqlite.org/download.html) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/JKrivec/algoritmik-technical-interview

# Go into the repository
$ cd algoritmik-technical-interview

# Install flask
$ pip install -U Flask

# Initialize an empty database
$ flask --app flaskr init-db

# Run the backend
$ flask --app flaskr --debug run
```
