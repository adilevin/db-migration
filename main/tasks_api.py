from flask import Flask, request, Response
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Todo:
# - Refactor to abstract the data access, and the models

import json
from model import task_model
import data_access_objects

dao = None

def connect_db():
    global dao
    dao = data_access_objects.dao_factory.create_dao(app.config['ENVIRONMENT'])

def disconnect_db():
    global dao
    del(dao)
    dao = None

def clear_db():
    dao.delete_all_tasks()

@app.route('/')
def home():
    return Response(json.dumps(app.config['ENVIRONMENT']),mimetype='application/json');

@app.route('/tasks',methods=['GET'])
def get_tasks():
    import ast
    filter_dict = {}
    if 'assignee' in request.args.keys():
        filter_dict['assignee'] = request.args['assignee']
    if 'done' in request.args.keys():
        filter_dict['done'] = ast.literal_eval(request.args['done'])
    tasks = dao.get_tasks_by_filter(filter_dict)
    return Response(task_model.array_to_json(tasks),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['GET'])
def get_task(task_id):
    task = dao.get_task_by_id(task_id)
    return Response(task_model.obj_to_json(task),mimetype='application/json');

@app.route('/tasks',methods=['POST'])
def add_task():
    assignee = request.form['assignee'];
    description = request.form['description'];
    import uuid
    task_id = str(uuid.uuid4())
    inserted_id = dao.add_task(task_model.Task(task_id,assignee,description,False));
    return Response(json.dumps({'id':inserted_id}),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['PUT'])
def mark_task_as_done(task_id):
    task = dao.mark_task_as_done(task_id)
    return Response(task_model.obj_to_json(task),mimetype='application/json');
