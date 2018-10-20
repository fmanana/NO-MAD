import json
import requests
from urllib.request import urlopen
from flask import Flask, render_template, request
import os
import jinja2

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('templates'))

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.methods == 'POST':
        university = request.form['university']
        #flights = (university)
        return render_template('flights.html', university=university)

if __name__ == "__main__":
    app.run(debug=True)