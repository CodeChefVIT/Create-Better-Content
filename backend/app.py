from flask import Flask, request, jsonify
from helpers.search import *

app = Flask(__name__)

@app.route('/keyword',methods=["POST"])
def keyword():
    data = request.json
    response = keyword_s(data['keyword'])
    return jsonify(response)

@app.route('/url',methods=["POST"])
def url():
    data = request.json
    response = link(data["link"])
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
