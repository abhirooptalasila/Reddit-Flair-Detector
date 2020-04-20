import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import praw
import string
import tensorflow as tf
import os
import itertools
import nltk
from tensorflow.keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from tensorflow.keras.backend import set_session

nltk.download('stopwords')

sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)

app = Flask(__name__)

dict = {8:"Scheduled", 7:"Politics",5:"Photography",6:"Policy/Economy",3:"Food", 2:"Coronavirus",1:"Business/Finance",4:"Non-Political",9:"Science/Technology",10:"Sports",0:"AskIndia"}


reddit = praw.Reddit(client_id='wJgNcO68RMNFbw', client_secret='MlVciTgnPvtTODltLPSM4FBxSfY', user_agent='new scrapper')

model = load_model("../models/model.h5")

with open('../models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def predictAPI(title):
    global model
    global graph
    with sess.as_default():
        with graph.as_default():
            response = predict_title(model, title)
    return response

def nltk_clean(field):
    # remove punctuation from each word
    words = field.split(" ")
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    field = ' '.join(stripped)

    # filter out stop words
    words = field.split(" ")
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    field = ' '.join(words)
    return field

def predict_title(model, title):
    sequences = tokenizer.texts_to_sequences([title])
    X = pad_sequences(sequences, maxlen=35)
    result = model.predict([X,X,X])
    return np.argmax(result,axis=-1)

def extract_id(input_url):
    input_title = input_url.split("/")
    if input_title[-1].isalpha():
        id_val = input_title[-2]
    else:
        id_val = input_title[-3]
    return str(id_val)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    url = [str(x) for x in request.form.values()]
    id_val = extract_id(str(url[0]))
    sub = reddit.submission(id=id_val)
    clean_title=nltk_clean(str(sub.title))
    pred = predictAPI(clean_title)

    return render_template('index.html', prediction_text='Flair: {}'.format(dict.get(int(pred[0]))))

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.route('/reqp',methods=['POST','GET'])
def reqp():
    data = request.get_json(force=True)
    id_val = str(data["title"])
    sub = reddit.submission(id=id_val)
    clean_title=nltk_clean(sub.title)
    pred = predictAPI(clean_title)
    return jsonify({"class":str(pred)})

@app.route("/automated_testing", methods=['POST'])
def automated():
    file = request.files['file']
    content = file.readlines()
    content = [x.strip() for x in content]
    values = {} 
    for x in content:
        x = x.decode()
        id_val = extract_id(x)
        sub = reddit.submission(id=id_val)
        clean_title=nltk_clean(sub.title)
        pred = predictAPI(clean_title)
        values.update({x:str(dict.get(int(pred[0])))})
    return jsonify(values)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
