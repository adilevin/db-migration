from flask import Flask, request, Response
app = Flask(__name__)

# Todo:
# - Add unittest
# - Refactor to abstract the data access, and the models


from bson.json_util import dumps
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
    import json
    return Response(json.dumps(app.config['ENVIRONMENT']),mimetype='application/json');

@app.route('/tasks',methods=['GET'])
def get_tasks():
    filter = {}
    if 'assignee' in request.args.keys():
        filter = {'assignee':request.args['assignee']}
    tasks_bson = [x for x in mongo.collection.find(filter)]
    return Response(dumps(tasks_bson),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['GET'])
def get_task(task_id):
    task_bson = mongo.collection.find_one(filter = {'_id':task_id})
    return Response(dumps(task_bson),mimetype='application/json');

@app.route('/tasks',methods=['POST'])
def add_task():
    assignee = request.form['assignee'];
    description = request.form['description'];
    import uuid
    task_id = str(uuid.uuid4())
    result = mongo.collection.insert_one({'_id':task_id,'assignee':assignee,'description':description,'done':False});
    return Response(dumps({'_id':result.inserted_id}),mimetype='application/json');

@app.route('/tasks/<task_id>',methods=['PUT'])
def mark_task_as_done(task_id):
    from pymongo import ReturnDocument
    doc = mongo.collection.find_one_and_update(filter={'_id':task_id},update={'$set': {'done':True}},
                                               return_document=ReturnDocument.AFTER)
    return Response(dumps(doc),mimetype='application/json');
