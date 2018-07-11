from flask import Flask, render_template, request, redirect, url_for, jsonify
from random import sample
import time
import datetime
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lmtech123@localhost:3306/industry6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# let me know the changes in the database but i don't want to know

db = SQLAlchemy(app)

class Simulation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    machine_number = db.Column(db.String(10))
    status = db.Column(db.String(10))
    number_of_pieces = db.Column(db.Integer)
    total_pieces = db.Column(db.Integer)
    running_status = db.Column(db.Integer)
    total_running_time = db.Column(db.Integer)
    total_downtime = db.Column(db.Integer)
    parameter_1 = db.Column(db.Integer)
    parameter_2 = db.Column(db.Integer)
    parameter_3 = db.Column(db.Integer)

@app.route('/')
def index():
    #return render_template('bar.html')
    return render_template('chart.html')

@app.route('/data')
def data():
    #return jsonify({'results': sample(range(1, 10), 5)})

    running_time = []
    run = []
    #b = list1[-3:]

    all_data = Simulation.query.all()


    for record in all_data:

        #print 'record' , record, record.running_status
        if record.machine_number == '1':
            #print 'running', record.running_status
            running_time.append(int(record.running_status))
            #print 'list', running_time

            run = running_time[-10:]
    return jsonify({'results' : run})


@app.route('/pieces')
def pieces():
    #return jsonify({'results': sample(range(1, 10), 5)})

    pieces = []
    p=[]

    all_data = Simulation.query.all()


    for record in all_data:

        #print 'record' , record, record.total_pieces
        if record.machine_number == '1':
            #print 'Pieces', record.total_pieces
            pieces.append(int(record.total_pieces))
            #print 'list', pieces


            p = pieces[-10:]
            # if len(pieces)>10:
            #     break
    return jsonify({'results' : p})






@app.route('/home')   # http://127.0.0.1:5000/
def home():
    all_data = Simulation.query.all()  # Gives all data in Comments table
    # #return render_template('db_index.html', all_data=all_data)
    # print 'all data:', all_data
    for record in all_data:
       # print'record: ', record.status
        if record.machine_number == '1':
            print record

@app.route('/method', methods=['GET', 'POST'])  # http://127.0.0.1:5000/method
def request_check():
    if request.method == 'POST':
        print 'received'

        print 'Post request data:', request.json
        # print type(request.data)
        json_dumps = json.dumps(request.json)
        print 'dumps:', json_dumps
        json_loads = json.loads(str(json_dumps))
        print 'loads:', json_loads
        #print json_loads['total_pieces']

        # machine = machine
        machine_number = json_loads['machine_number']
        status = json_loads['status']
        number_of_pieces = json_loads['number_of_pieces']
        total_pieces = json_loads['total_pieces']
        running_status = json_loads['running_status']
        total_running_time = json_loads['total_running_time']
        total_downtime = json_loads['total_downtime']
        parameter_1 = json_loads['parameter_1']
        parameter_2 = json_loads['parameter_2']
        parameter_3 = json_loads['parameter_3']

        signature = Simulation(machine_number=machine_number, total_pieces=total_pieces,
                               status=status, number_of_pieces=number_of_pieces,
                               running_status=running_status, total_running_time=total_running_time,
                               total_downtime=total_downtime, parameter_1=parameter_1,
                               parameter_2=parameter_2, parameter_3=parameter_3)

        db.session.add(signature)
        db.session.commit()
        return 'Success'

    else:
        return 'Fail'

if __name__ == '__main__':
    app.run(debug=True)
