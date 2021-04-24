from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
	return jsonify({'text':'Hello World!'})

if __name__ == '__main__':
	app.run(port=4200)
