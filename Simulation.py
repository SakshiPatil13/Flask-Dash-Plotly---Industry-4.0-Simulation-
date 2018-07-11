import random  # import random to genrate random machine data
import time    # import time to specify data upload interval
import requests  # Import requests library to send requests to Thingworx
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
#    #<script src="https://bower_components/chartist/dist/chartist.min.js"></script>
url = 'http://127.0.0.1:5000/method'
# Specify the server url

headers = {
    'Content-Type': 'application/json'
}
parameter1 = 34
parameter2 = 20
parameter3 = 58

running_hours = [0, 0, 0,]
downtime_hours = [0, 0, 0]
total_pieces=[0,0,0]
pieces = [0]
status=''
running_status=[0]
downtime=[0]
run=[0]


def flask_upload(machine_number, running_status, status, running_hours,
                     downtime_hours, pieces, total_pieces, parameter1, parameter2, parameter3):

    data = {'machine_number': machine_number, 'running_status': running_status,
            'status': status, 'total_running_time': running_hours,
            'total_downtime': downtime_hours, 'number_of_pieces': pieces,
            'total_pieces': total_pieces, 'parameter_1': parameter1,
            'parameter_2': parameter2, 'parameter_3': parameter3}


    response = requests.post(url, headers=headers, json=data)
    print 'Response Code:', response.status_code
    print '\n'

while True:
    for machine in range(1,4):
        print 'Machine Number: ', machine

        running = random.sample(range(0, 2), 1)
        print 'Running Status:', running[0]

        if running[0] == 1:
            status = 'ON'

            run = random.sample(range(1,6), 1)
            running_hours[machine-1] += run[0]
            print 'Total Running Time: ', running_hours[machine-1]

            pieces = random.sample(range(1, 6), 1)
            print 'Pieces: ', pieces[0]
            total_pieces[machine - 1] += pieces[0]
            print 'Total Pieces: ', total_pieces[machine - 1]

        else:
            status = 'OFF'
            print 'status: ', status
            downtime = random.sample(range(1, 6), 1)
            downtime_hours[machine - 1] += downtime[0]
            print 'Total Downtime: ',downtime_hours[machine - 1]




        flask_upload(machine, running[0], status, running_hours[machine-1],
                     downtime_hours[machine - 1], pieces[0],
                     total_pieces[machine-1], parameter1, parameter2, parameter3)

    time.sleep(5)