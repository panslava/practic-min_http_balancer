from pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

db_client = MongoClient('mongodb://root:password@mongo')
db = db_client.server_storage
storage = db.storage


@app.route('/', endpoint="root")
def put():
    return "Hello, world!"


@app.route('/put', methods=['POST', 'PUT'], endpoint="put")
def put():
    response = {}
    storage.find_one_and_update(
        {"key": request.values.get("key")}, {"$set": {"key": request.values.get("key"), "value": request.values.get("value")}}, upsert=True)
    return response, 200


@app.route('/get', methods=['GET'], endpoint="get")
def get():
    response = {}
    response_code = 200
    storage_ans = storage.find_one({"key": request.values.get("key")})
    if storage_ans:
        response["value"] = storage_ans['value']
    else:
        response_code = 404
    return response, response_code


@app.route('/delete', methods=['DELETE'], endpoint="delete")
def get():
    response = {}
    response_code = 200
    deleted_count = storage.delete_one({"key": request.values.get("key")}).deleted_count
    if not deleted_count:
        response_code = 404
    return response, response_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
