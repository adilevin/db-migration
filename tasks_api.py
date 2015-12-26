from flask import Flask, request, Response
app = Flask(__name__)

# Todo:
# - Refactor to abstract the data access, and the models

import json

mongo = {}

def connect_db():
    import mongodb_dao
    global mongo
    mongo = mongodb_dao.Mongo(
        connection_uri=app.config['ENVIRONMENT']['mongodb_connection_uri'],
        database_name=app.config['ENVIRONMENT']['mongodb_database_name'])

def clear_db():
    mongo.clear()

@app.route('/')
def home():
    return Response(json.dumps(app.config['ENVIRONMENT']),mimetype='application/json');

@app.route('/tasks',methods=['GET'])
def get_tasks():
    import ast
    filter = {}
    if 'assignee' in request.args.keys():
        filter['assignee'] = request.args['assignee']
    if 'done' in request.args.keys():
        filter['done'] = ast.literal_eval(request.args['done'])
    tasks = [x for x in mongo.collection.find(filter)]
    return Response(json.dumps(tasks),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['GET'])
def get_task(task_id):
    task = mongo.collection.find_one(filter = {'_id':task_id})
    return Response(json.dumps(task),mimetype='application/json');

@app.route('/tasks',methods=['POST'])
def add_task():
    assignee = request.form['assignee'];
    description = request.form['description'];
    import uuid
    task_id = str(uuid.uuid4())
    result = mongo.collection.insert_one({'_id':task_id,'assignee':assignee,'description':description,'done':False});
    return Response(json.dumps({'_id':result.inserted_id}),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['PUT'])
def mark_task_as_done(task_id):
    from pymongo import ReturnDocument
    doc = mongo.collection.find_one_and_update(filter={'_id':task_id},update={'$set': {'done':True}},
                                               return_document=ReturnDocument.AFTER)
    return Response(json.dumps(doc),mimetype='application/json');
