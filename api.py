import os
import json
import urllib
import ssl
import numpy as np

from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import Flask, flash, request, redirect, url_for, jsonify, Response

from Resources.generateGrade import GenerateGrade

# import GenerateGrade from "."

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello():
    js = {
        'message': "deejAI Works"
    }
    return jsonify(js)


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
#


api.add_resource(GenerateGrade, '/generateGrade')

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     host = os.environ.get("HOST", '127.0.0.1')
#     app.run(host=host, port=port)
if __name__ == '__main__':
    host = os.environ.get("HOST", '0.0.0.0')
    app.run(debug=True, host=host)
