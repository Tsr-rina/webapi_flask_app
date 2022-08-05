# from flask import Flask, render_template, url_for
from flask import *
import requests
import random

global url
url = "https://fastapi-try-git-rina-7-31-tsr-rina.vercel.app/items/art/v2/"
url_japan = "https://fastapi-try-git-rina-7-31-tsr-rina.vercel.app/items/art/v2/japan"

country = ['japan', 'france', 'america', 'italy', 'spain']

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    p_name = []
    p_kana = []
    p_exp = []

    res = requests.get(url)
    data_all = json.loads(res.text)

    for i in range(len(data_all)):
        cn = randoms(0,4)
        pn = randoms(1,5)
        p_name.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_name'])
        p_kana.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_kana'])
        p_exp.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_explanation'])

    return render_template("index.html", name=p_name, kana=p_kana, explain=p_exp)

@app.route("/test_ajax/", methods=["GET", "POST"])
def test_ajax():
    p_name = []
    p_kana = []
    p_exp = []

    a_name = []
    a_kana = []
    a_birth = []
    a_exp = []

    c = request.args.get("value")
    res = requests.get(url+c)
    data = json.loads(res.text)
    for i in range(1, len(data[0])+1):
        p_name.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_name'])
        p_kana.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_kana'])
        p_exp.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_explanation'])
        a_name.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_name'])
        a_kana.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_kana'])
        a_birth.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_birthday'])
        a_exp.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_info'])
    return jsonify({"product":[p_name, p_kana, p_exp], "author":[a_name, a_kana, a_birth, a_exp]})
    # return jsonify({"result":url+c})

def randoms(s, e):
  n = random.randint(s, e)
  return n


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8801)
