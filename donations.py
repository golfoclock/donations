from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

MONGODB_URI = os.getenv('MONGODB_URI')

# MONGO_HOST = 'localhost'
# MONGO_PORT = 2701

DBS_NAME = os.getenv('MONGO_DB_NAME','donorsUSA')
COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME','projects')
FIELDS = {'funding_status': True, 'school_state': True, 'resource_type': True, 'poverty_level': True,
          'date_posted': True, 'total_donations': True, 'teacher_prefix': True,'_id': False}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donorsUS/projects")
def donor_projects():
    connection = MongoClient(MONGODB_URI)

    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find({"school_state": "NY"}, projection=FIELDS, limit=55000)


    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects)
    connection.close()
    return json_projects


if __name__ == "__main__":
    app.run(debug=True)

