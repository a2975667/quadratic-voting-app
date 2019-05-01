from app import app, mongo
from flask import request, jsonify, url_for, session
from flask import render_template, make_response
import json.decoder
import os
import uuid 
from pprint import pprint
import random

# filename = os.path.join(app.static_folder, 'qv.json')
# questions = open(filename, "r")
# questions = json.load(questions)

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
    json_filename='qv'+str(qvid)+'.json'
    url_for('static', filename=json_filename)
    url_for('static', filename='qv.css')
    url_for('static', filename='loading.gif')
    url_for('static', filename='jquery-magnet.js')  
    q_file = os.path.join(app.static_folder, ('qv'+str(qvid)+'.json'))
    questions = open(q_file, "r")
    questions = json.load(questions)
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

@app.route('/submit_qv5982', methods=['POST'])
def submit_qv5982():
    data = request.json
    uid = request.cookies.get('UserId')
    insert_data = {
        "userid": uid,
        "form": "qv5982",
        "results":data
    }
    mongo.db.result_5982.insert_one(insert_data)
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
            #pprint(vote)
            item = vote['name']
            item = lookup[item]
            value = int(vote["value"])
            if item not in agg:
                agg[item] = value
            else:
                agg[item] += value
    #pprint(agg)

    insert_data = []
    for key in agg:
        insert_data.append({"group": key, "value": agg[key]})

    return render_template('results.html', data=insert_data)

@app.route('/paper-results')
def results2():
    lookup = {"1)": "1/18",
              "2)": "2/01",
              "3)": "2/08",
              "4)": "2/13",
              "5)": "2/15",
              "6)": "2/20",
              "7)": "2/27",
              "8)": "3/01-1",
              "9)": "3/01-2",
              "10)": "3/06",
              "11)": "3/08",
              "12)": "3/13",
              "13)": "3/15",
              "14)": "3/27",
              "15)": "3/29",
              "16)": "4/03",
              "17)": "4/05",
              "18)": "4/10",
              "19)": "4/12"}
    agg = {}
    for s in mongo.db.result_5982.find():
        for vote in s['results']:
            #pprint(vote)
            item = vote['name']
            item = lookup[item]
            value = int(vote["value"])
            if item not in agg:
                agg[item] = value
            else:
                agg[item] += value
    #pprint(agg)

    insert_data = []
    for key in agg:
        insert_data.append({"group": key, "value": agg[key]})

    return render_template('results.html', data=insert_data)