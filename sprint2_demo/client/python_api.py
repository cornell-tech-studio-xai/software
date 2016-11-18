from flask import Flask, jsonify
from flask_restful import Resource, Api
import time
import sys

from parser import parse

app = Flask(__name__)
api = Api(app)


class ParseEmails(Resource):
    def get(self, text):
        output = jsonify(parse(text))
        return output

api.add_resource(ParseEmails, '/parse/<string:text>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)