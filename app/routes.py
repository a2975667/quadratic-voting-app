from app import app, mongo
from flask import request, jsonify, url_for, session
from flask import render_template, make_response
import json.decoder
import os
import uuid 
from pprint import pprint
import random

filename = os.path.join(app.static_folder, 'qv.json')
questions = open(filename, "r")
questions = json.load(questions)

@app.route('/')
@app.route('/welcome')
def welcome():
    rd = random.Random()
    rd = rd.getrandbits(128)
    userid=str(uuid.UUID(int=rd))
    # print(userid, rd)
    while mongo.db.users.find_one({"userid":userid}) is not None:
        rd = random.Random()
        rd = rd.getrandbits(128)
        userid = str(uuid.UUID(int=rd))
    
    mongo.db.users.insert_one({"userid":userid}) 
    resp = make_response(render_template('welcome.html', data={'form':''}))
    resp.set_cookie('UserId', userid)
    return resp

@app.route('/complete')
def complete():
    resp = make_response(render_template('thankyou.html', data={}))
    # resp.set_cookie('UserId', '', expires=0)
    # TODO: move save to user here
    return resp

@app.route('/qv/<qvid>')
def dv(qvid):
    filename='qv'+str(qvid)+'.js'
    url_for('static', filename=filename)
    url_for('static', filename='qv.css')
    url_for('static', filename='loading.gif')
    url_for('static', filename='jquery-magnet.js')  
    return render_template('qv.html', q_list = questions['questions'],filename=filename)

@app.route('/api/welcome')
def api_index():
    return "API version 0.0.0"

@app.route('/submit_qv598', methods=['POST'])
def submit_qv598():
    data = request.json
    uid = request.cookies.get('UserId')
    insert_data = {
        "userid": uid,
        "form": "qv598",
        "results":data
    }
    mongo.db.result_598.insert_one(insert_data)
    return jsonify({'ok': True}), 200


@app.route('/api/updateScript', methods=['POST'])
def update_script():
    data = request.json
    mongo.db.users.insert_one({"userid": data['userid']})
    return jsonify({'ok': True}), 200

@app.route('/results')
def results():
    lookup = {"1)": "Yuxin & Zecheng",
              "2)": "Junting",
              "3)": "Sneha & Grace",
              "4)": "Ti-Chung & Tiffany",
              "5)": "Anant",
              "6)": "Chaoyue",
              "7)": "Xinran",
              "8)": "Yiyu",
              "9)": "Lan",
              "10)": "Surya",
              "11)": "Deepak",
              "12)": "Raymond"}
    agg = {}
    for s in mongo.db.result_598.find():
        for vote in s['results']:
            pprint(vote)
            item = vote['name']
            item = lookup[item]
            value = int(vote["value"])
            if item not in agg:
                agg[item] = value
            else:
                agg[item] += value
    pprint(agg)

    insert_data = []
    for key in agg:
        insert_data.append({"group": key, "value": agg[key]})

    return render_template('results.html', data=insert_data)
