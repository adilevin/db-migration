from flask import Flask, request, Response
app = Flask(__name__)

class Mongo(object):
    def __init__(self):
        from pymongo import MongoClient
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.test
        self.collection = self.db.tasks

mongo = Mongo()
from bson.json_util import dumps

@app.route('/')
def home():
    return 'Application is running'

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

if __name__ == '__main__':
    app.run()
