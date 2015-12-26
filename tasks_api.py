from flask import Flask, request, Response
app = Flask(__name__)

# Todo:
# - Refactor to abstract the data access, and the models

import json
import model

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
    tasks = mongo.get_tasks_by_filter(filter)
    return Response(model.array_to_json(tasks),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['GET'])
def get_task(task_id):
    task = mongo.get_task_by_id(task_id)
    return Response(model.obj_to_json(task),mimetype='application/json');

@app.route('/tasks',methods=['POST'])
def add_task():
    assignee = request.form['assignee'];
    description = request.form['description'];
    import uuid
    task_id = str(uuid.uuid4())
    inserted_id = mongo.add_task(model.Task(task_id,assignee,description,False));
    return Response(json.dumps({'id':inserted_id}),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['PUT'])
def mark_task_as_done(task_id):
    task = mongo.mark_task_as_done(task_id)
    return Response(model.obj_to_json(task),mimetype='application/json');
