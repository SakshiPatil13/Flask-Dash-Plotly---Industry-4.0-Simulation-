import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import datetime
import MySQLdb

ct = datetime.datetime.now()
print 'current time:', ct
X = deque(maxlen=20)
X.append(str(ct)[11:19])
Y = deque(maxlen=20)
Y.append(1)




db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="lmtech123",  # your password
                     db="industry6")      # name of the database
cur = db.cursor()


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval= 5 * 1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    # X.append(X[-1]+1)
    ct = datetime.datetime.now()
   # X.append(str(ct)[11:19])

    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="lmtech123",  # your password
                         db="industry6")  # name of the database
    cur = db.cursor()

    cur.execute("SELECT * FROM simulation WHERE id=(SELECT MAX(id) FROM simulation)")
    # Now, print all the rows
    for row in cur.fetchall():
        print row
        no_pieces = int(row[5])
        print no_pieces, type(no_pieces), row[1],
        dt=row[1]
        Y.append(no_pieces)
        break
    X.append(str(dt)[11:19])
    db.commit()  # This will save the data in actual database
    cur.close()
    db.close()

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(title='Number Of Pieces',xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}



if __name__ == '__main__':
    app.run_server(debug=True)