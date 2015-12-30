from flask import Flask, request, Response

app = Flask(__name__)

#from flask.ext.cors import CORS
#cors = CORS(app)

import json
from model import task_model
from data_access_objects import dao_factory

def obj_to_json(obj):
    return json.dumps(obj.__dict__)

def array_to_json(arr):
    return json.dumps([item.__dict__ for item in arr])

dao = None

def connect_db():
    global dao
    dao = dao_factory.create_dao(app.config['ENVIRONMENT'])

def disconnect_db():
    global dao
    del(dao)
    dao = None

def clear_db():
    dao.delete_all_tasks()

@app.route('/',methods=['GET'])
def root():
    return app.send_static_file('userConsole.html')

@app.route('/config',methods=['GET'])
def get_config():
    return Response(json.dumps(app.config['ENVIRONMENT']),mimetype='application/json');

@app.route('/tasks',methods=['GET'])
def get_all_undone_tasks_for_assignee():
    tasks = dao.get_all_undone_tasks_for_assignee(request.args['assignee'])
    return Response(array_to_json(tasks),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['GET'])
def get_task(task_id):
    task = dao.get_task_by_id(task_id)
    return Response(obj_to_json(task),mimetype='application/json');

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
    return Response(obj_to_json(task),mimetype='application/json');
