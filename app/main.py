# from flask import Flask, render_template, url_for
from flask import *
import requests
import random

global url
url = "https://fastapi-try-git-rina-7-31-tsr-rina.vercel.app/items/art/v2/"
url_japan = "https://fastapi-try-git-rina-7-31-tsr-rina.vercel.app/items/art/v2/japan"

country = ['japan', 'france', 'america', 'italy', 'spain']

translation_country = {"japan":"日本", "france":"フランス", "america":"アメリカ", "italy":"イタリア", "spain":"スペイン"}

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():

    res = requests.get(url)
    data_all = json.loads(res.text)

    p_name, p_kana, p_exp, a_country = get_random(data_all)

    return render_template("index.html", name=p_name, kana=p_kana, explain=p_exp, country=a_country)


def get_random(data_all):
    p_name = []
    p_kana = []
    p_exp = []
    a_country = []

    for i in range(len(data_all)):
        cn = randoms(0,4)
        pn = randoms(1,5)

        p_name.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_name'])
        p_kana.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_kana'])
        p_exp.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['p_explanation'])
        a_country.append(data_all[country[cn]][0]['product_'+str(country[cn][:1])+str(pn)][0]['author'][0]['a_from'])

    return p_name, p_kana, p_exp, a_country



def get_p(data):
    p_name = []
    p_kana = []
    p_exp = []

    for i in range(1, len(data[0])+1):
        p_name.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_name'])
        p_kana.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_kana'])
        p_exp.append(data[0]['product_'+str(c[:1])+str(i)][0]['p_explanation'])
    
    return p_name, p_kana, p_exp

def get_a(data):
    a_name = []
    a_kana = []
    a_birth = []
    a_exp = []
    a_country = []

    for i in range(1, len(data[0])+1):
        a_name.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_name'])
        a_kana.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_kana'])
        a_birth.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_birthday'])
        a_exp.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_info'])
        a_country.append(data[0]['product_'+str(c[:1])+str(i)][0]['author'][0]['a_from'])
    
    return a_name, a_kana, a_birth, a_exp, a_country




@app.route("/test_ajax/", methods=["GET", "POST"])
def test_ajax():

    c = request.args.get("value")

    res = requests.get(url+c)
    data = json.loads(res.text)

    p_name, p_kana, p_exp = get_p(data)

    a_name, a_kana, a_birth, a_exp, a_country = get_a(data)


    return jsonify({"product":[p_name, p_kana, p_exp], "author":[a_name, a_kana, a_birth, a_exp ,a_country]})
    # return jsonify({"result":url+c})

@app.route("/popup_ajax/", methods=["GET", "POST"])
def popup():
    a_name = ""
    a_kana = ""
    a_birth = ""
    a_exp = ""
    a_from = ""


    name = request.args.get("name")
    country = request.args.get("country")
    
    res = requests.get(url + country)
    data = json.loads(res.text)

    name_array, kana_array, birth_array, exp_array, country_array = get_a(data)


    for i in range(1, len(data[0])+1):
        tmp = data[0]['product_'+str(country[:1])+str(i)][0]['p_name']

        if tmp == name:
            a_name = data[0]['product_'+str(country[:1])+str(i)][0]['author'][0]['a_name']
            a_kana = data[0]['product_'+str(country[:1])+str(i)][0]['author'][0]['a_kana']
            a_birth = data[0]['product_'+str(country[:1])+str(i)][0]['author'][0]['a_birthday']
            a_exp = data[0]['product_'+str(country[:1])+str(i)][0]['author'][0]['a_info']
            a_from = translate(data[0]['product_'+str(country[:1])+str(i)][0]['author'][0]['a_from'])

    return jsonify({"author":[a_name, a_kana, a_birth, a_exp, a_from]})


def randoms(s, e):
    n = random.randint(s, e)
    return n

def translate(e_country):
    
    send = ""

    for key, value in translation_country.items():
        if key == e_country:
            send = value

    return send



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8801)
