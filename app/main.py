# from flask import Flask, render_template, url_for
from flask import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    return render_template("index.html")

@app.route("/test_ajax/", methods=["GET", "POST"])
def test_ajax():
    value = request.args.get("value")
    value = str(value)
    result = value + ":日本です"
    return jsonify({"result":result})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8801)
