import json
import requests
from urllib.request import urlopen
from flask import Flask, render_template, request

app = Flask(__name__)

#URL =  'https;//website.com"

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.methods == 'POST':
        university = request.form['university']
        flights = (university)
        return render_template('flights.html', flights=flights)
    else:
        return render_template('index.html')



#var output
## Uploading flight data