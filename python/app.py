from flask import Flask, request, send_from_directory, jsonify
from flask_pymongo import PyMongo
from task import AddonGetTask
app = Flask(__name__, static_url_path='/dist')

app.config['MONGO_URI'] = 'mongodb://localhost:27017/jira-dev'
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/app-installed-callback', methods=['POST'])
def on_installed():
    validation = True # @todo

    if not validation:
        return 'Error', 400

    data = request.get_json()
    mongo.db.datas.update_one(
        {'baseUrl': data['baseUrl']},
        {'$set': data},
        True
    )

    return '', 200


@app.route('/example')
def example():
    domain = 'https://base-url.atlassian.net'

    data = mongo.db.datas.find_one(
        {'baseUrl': domain}
    )

    test = AddonGetTask(domain, data['sharedSecret'], data['key'])
    res1 = test.get_data('TEST-1')
    res2 = test.get_data('TEST-2')
    res3 = test.get_data('TEST-3')

    return jsonify({'res1': res1, 'res2': res2, 'res3': res3}), 200


@app.route('/atlassian-connect.json')
def get_app_config():
    return send_from_directory('dist', 'atlassian-connect.json')


@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return '', 404


if __name__ == '__main__':
    app.run()
