import json
import requests
from urllib.request import urlopen
from flask import Flask, render_template, request, redirect, url_for
import os
import jinja2
import recommend
import spont

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('templates'))

app = Flask(__name__, static_folder=os.path.join(os.getcwd(),'static'))

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        university = request.form['university']
        recommended = json.loads(recommend.uni_data(university))
        print( json.dumps(recommended, indent=2))
        return render_template('flights.html', flights=recommended)
    else:
        return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template('contact.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')