from flask import Flask, request, make_response, jsonify, send_file
from gevent.pywsgi import WSGIServer
import requests
import traceback
import pymysql
import json
from io import BytesIO
import urllib

app = Flask(__name__)


with open('config.json', 'r') as f:
    conf = json.load(f)
DATABASE = conf['mysql']
HYCON = conf['hycon']


def connect_db():
    return pymysql.connect(host=DATABASE['host'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            db=DATABASE['database'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/checkin')
def checkin():
    return

@app.route('/post')
def post(self, endpoint, uri, body=None):
    if body:
        body = json.dumps(body).encode()
    url = urllib.parse.urljoin(endpoint, uri)
    request = urllib.request.Request(url, data=body)
    # response = urllib.request.urlopen(request)
    # return json.load(response)
    x = urllib.request.urlopen(request)
    raw_data = x.read()
    encoding = x.info().get_content_charset('utf8')  # JSON default
    data = json.loads(raw_data.decode(encoding))
    return data


if __name__ == '__main__':
    # app.run()
    # http = WSGIServer(('0.0.0.0', 5000), app)
    # http.serve_forever()

    cert = './cert_key/pfx.mycattool_com.crt'
    key = './cert_key/pfx.mycattool_com.key'
    https = WSGIServer(('0.0.0.0', 5000), app, keyfile=key, certfile=cert)
    https.serve_forever()
