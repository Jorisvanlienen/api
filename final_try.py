from flask import Flask
from flask import jsonify
from flask import request
from PIL import Image
import io
import numpy as np
import base64

app = Flask(__name__)


quarks = [{'name': [3,3,3,3,3,3]},]

@app.route('/', methods=['GET'])
def hello_world():

    return jsonify({'message' : 'Hello, World!'})

@app.route('/quarks', methods=['GET'])
def returnAll():
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['GET'])
def returnOne(name):
    theOne = quarks[0]
    for i,q in enumerate(quarks):
      if q['name'] == name:
        theOne = quarks[i]
    return jsonify({'quarks' : theOne})
def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))


@app.route('/quarks', methods=['POST'])
def addOne():
    #new_quark = request.get("http://127.0.0.1:5000/quarks",  params={'q': 'requests+language:python'})

    new_quark = request.get_json(force=True)
    new_quark = new_quark["name"]
    bytestring = str(new_quark)
    bytestring = bytestring[:-2]
    bytestring = bytestring[2:]
    decoded = base64.b64decode(bytestring)
    image = Image.open(io.BytesIO(decoded))
    image_np = np.array(image)
    new_quark = np.rot90(image_np, k=2, axes=(0, 1))

    im = Image.fromarray(new_quark)
    im.save("test.bmp")

    with open("test.bmp", "rb") as image_file:
        new_quark = base64.b64encode(image_file.read())
    new_quark = str(new_quark)
    new_quark = new_quark[2:]
    new_quark = new_quark[:-1]
    new_quark={'name': [new_quark]}
    quarks.append(new_quark)
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['PUT'])
def editOne(name):
    new_quark = request.get_json()
    for i,q in enumerate(quarks):
      if q['name'] == name:
        quarks[i] = new_quark
    qs = request.get_json()
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['DELETE'])
def deleteOne(name):
    for i,q in enumerate(quarks):
      if q['name'] == name:
        del quarks[i]
    return jsonify({'quarks' : quarks})

if __name__ == "__main__":
    app.run(debug=False, host = '10.100.102.4')
