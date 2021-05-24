
import os
import numpy as np
from flask import Flask, redirect, url_for, request, render_template
from search import *

# Define a flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])#display page
def predict():
    return render_template('index.html')


@app.route('/show', methods=['GET', 'POST'])#page to show the o/p
def keyword():
    if request.method == 'POST':
        search=request.form['text']
        return render_template('index.html',prediction_text=str(keyword_s(search)))
# def show():
#     if request.method == 'POST':
#         search=request.form['text']
#         return render_template('index.html',prediction_text=str(keyword_s(search)))

if __name__=="__main__":
    app.run(debug=True)