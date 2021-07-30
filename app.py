# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# pickle
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy 

#for webscraping
import requests
import bs4 
from bs4 import BeautifulSoup
import time

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
encoder_file = open('models/Departure_encoder.pkl', 'rb')
le_encode = pickle.load(encoder_file)
encoder_file.close()

decoder_file = open('models/Departure_decoder.pkl', 'rb')
le_decode = pickle.load(decoder_file)
decoder_file.close()

model = pickle.load(open('models/mod.pkl', 'rb'))
  

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('prediction_index.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():
    # return render_template('res.html')
    data_list = list()
    for i in range(1,39):
      data_list[i] = int(request.form['q'+ str(i)])
    
    arr = [data_list,]
    testdf = pd.DataFrame(arr)
    data123 = testdf.iloc[:,:].values
        
    for i in range(14,38):
        data123[:,i] = le_encode[i].transform(data123[:,i]) 

    md = model.predict(data123)
    pred = le_decode.inverse_transform([md])
    predrole = "".join(pred)
    role =  predrole.split()

    BaseURL = ["https://in.indeed.com/jobs?q=", "&l="]
    URL = BaseURL[0] +  "+".join(role) + BaseURL[1]
 
    #conducting a request of the stated URL above:
    page = requests.get(URL)
    #specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
    soup = BeautifulSoup(page.text, "html.parser")

    job = extract_job_title_from_result(soup)
    company = extract_company_from_result(soup)
    location = extract_location_from_result(soup)

    return render_template('prediction_result.html', sugrole = predrole, len = len(job), jbr = job, comp = company, loc = location)


def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      jobs.append(a["title"])
  return(jobs)



def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
         companies.append(span.text.strip())
  return(companies)
 



def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return(locations)


    

if __name__ == "__main__":
    app.run(debug=True) 