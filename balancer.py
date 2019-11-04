import redis
import requests
from flask import Flask, request

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

BASE_URL = 'http://server_'


@app.route('/', endpoint='root')
def put():
    return 'Hello, world!'


@app.route('/put', methods=['POST', 'PUT'], endpoint='put')
def put():
    response = {}
    server_num = hash(request.values.get('key')) % 2
    requests.post(f'{BASE_URL}{server_num}/put', data=request.values)
    return response, 200


@app.route('/get', methods=['GET'], endpoint='get')
def get():
    response = {
        'from-cache': False
    }
    response_code = 200
    cached_ans = None
    if not request.values.get('no-cache'):
        cached_ans = cache.get(request.values.get('key'))

    if request.values.get('no-cache') or not cached_ans:
        server_num = hash(request.values.get('key')) % 2
        server_response = requests.get(f'{BASE_URL}{server_num}/get',
                                       params={
                                           'key': request.values.get('key')
                                       })
        response_code = server_response.status_code
        if response_code == 200:
            response['value'] = server_response.json()['value']
            if not request.values.get('no-cache'):
                cache.set(request.values.get("key"), str(response['value']))
    else:
        if type(cached_ans) is bytes:
            cached_ans = cached_ans.decode('utf-8')
        response['value'] = cached_ans
        response['from-cache'] = True
    return response, response_code


@app.route('/delete', methods=['DELETE'], endpoint='delete')
def get():
    response = {}
    response_code = 200
    cache.delete(request.values.get('key'))
    server_num = hash(request.values.get('key')) % 2
    server_response = requests.delete(f'{BASE_URL}{server_num}/delete',
                                      data={
                                          'key': request.values.get('key')
                                      })
    response_code = server_response.status_code
    return response, response_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=65432)
