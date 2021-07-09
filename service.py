import numpy as np
from flask import Flask, request, render_template

#from flask_restx import Api
from flask_restful import Resource, Api
import tabula
from transformers import pipeline
import pandas as pd
import logging
import sys
from flask import Flask, render_template
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, request, url_for
import pandas as pd
from fastai.text.all import *
from transformers import *

from blurr.data.all import *
from blurr.modeling.all import *
#logging.basicConfig(format='%(asctime)s - %(message)s',filename='app.log', filemode='w', level=logging.INFO)
#logging.info("Test working")

app = Flask(__name__)
api = Api(app)

large_model = load_learner(fname='para_full_export.pkl')
def return_answers(question):
    print(question)
    result=""
    outputs = large_model.blurr_generate(question, early_stopping=True, num_beams=7, num_return_sequences=1)
    for idx, o in enumerate(outputs):
        result=o
    print("FINAL",result)
    return result


@app.route('/')
def info():
    return render_template('info.html')    

    
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        #uploaded_file = request.files['file']
        #filename = secure_filename(uploaded_file.filename)
        #if uploaded_file.filename != '':
            #uploaded_file.save(os.path.join('C:\RootDirectory', filename))
        return redirect(url_for('home'))
    else:
        return render_template('upload.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      
        ade_drg=[]
        search_obj = ""
        dose_drg=[]
        status=""
        try:
            data = request.form['SearchObj']
            status=return_answers(data)
            print("Status",status)
        except:
            print("Exception while executing post operation")
            #print(sys.exc_info())
            #logging.info(sys.exc_info())
            #answers.append("Unable to get URL. Please make sure it's valid and try again.")
        return render_template('yes_no.html',answers=[status],query=data)
    else:
        #nothing
        return render_template('home.html')

#This function is to perform search operation.
@app.route('/neryesno', methods=['GET', 'POST'])
def neryesno():
    data = request.form['description']
    response = extract_entities_desc(data)
    #return json.dumps(response)
    return json.dumps(list(map(tuple,response)))
    
if __name__ == '__main__':
     app.run(debug=True)
