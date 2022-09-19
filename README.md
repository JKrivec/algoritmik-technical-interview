# Algoritmik technical interview

## Description

Small full-stack app with VueJS front-end, Flask back-end with local SQLite database.\
Downloads and saves a document via provided api into a local database to show knowledge of simple concepts.

<br />

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Nodejs](https://nodejs.org/en/) (which comes with [npm](https://docs.npmjs.com) packet manager), [Python](https://www.python.org/downloads/) (which comes with [pip](https://pypi.org/project/pip/) package installer) and [SQLite](https://www.sqlite.org/download.html) installed on your computer.<br/>From your command line:

```bash
# Install prerequisites
$ pip install flask
$ pip install flask_cors
$ pip install python-dotenv

# Clone this repository into an empty directory
$ git clone https://github.com/JKrivec/algoritmik-technical-interview

# Go into the repository
$ cd algoritmik-technical-interview
```

### Running the backend

```bash
# Navigate to the backend directory
$ cd backend

# Initialize an empty database
$ flask --app flaskr init-db

# Run the backend
$ flask --app flaskr run

# If you wish to clear the database
$ flask --app flaskr clear-db

```

### Running the frontend

```bash
# Open a new terminal and navigate to the frontend directory
$ cd ../frontend

# Install the prerequisites with npm
$ npm install

# Run the frontend (develop)
$ npm run serve

# OR you can build the production files
$ npm run build

# You will need a http server to serve the files (ex. serve)
$ npm install -g serve

# Serve the files with serve
$ serve -s build

```

### Setting the environment variables

If Perhaps the ip address of the backend server is different on your machine, you can change the ip in .env file in the frontend.
Including .env files into git is a crime (and even more so uploading api keys), but I did it anyway for the sake of simplicity.

### User interface

![image](https://user-images.githubusercontent.com/32847450/190931344-53bce24b-0977-46e9-84bf-4bb5aee91c90.png)

### Usage

To read the data from documents, a model first has to be trained (You can do so by visiting [typless](https://app.typless.com/) and creating your own document type). For sake of simplicity, I have already trained a model with the name "api_test". You can test test the usage by selecting the "amazing_company_1.pdf" invoice provided in the main folder of the repository, selecting "api_test" document type name and clicking "process"

# Final words

There is a lot left to be implemented for smoother experience but perhaps for some other day.
