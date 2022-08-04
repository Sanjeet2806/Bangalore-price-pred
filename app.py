from flask import Flask, request, jsonify, render_template
import pickle
import json
import numpy as np
#global variables storing set of locations,data columns and the model itself
__locations = None
__data_columns = None
__model = None

app = Flask(__name__)
__data_columns = json.load(open("columns.json", "r"))['data_columns']
__locations = __data_columns[3:]
__model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))

#getting estimated price from the loaded model
def get_estimated_price(location,sqft,bhk,bath):
    global __data_columns
    global __model
    try:
        loc_index = __data_columns.index(location.lower()) #fetiching the index of the asked location in data_columns
    except:
        loc_index = -1 #if no such location exists

    x = np.zeros(len(__data_columns)) #preparing the values in correct format [[sqft,bath,bhk,0,....,1,....,0]] where 1 is for the location index of asked location
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2) #predicts the result and rounds it upto 2 decimal places

# def load_saved_artifacts():
#     #function to load artifacts(the model and the column list) to be called from the server
#     print("loading saved artifacts...start")
#     #reference to global variables
#     global  __data_columns
#     global __locations

#     with open("./columns.json", "r") as f: #opening the json file
#         __data_columns = json.load(f)['data_columns'] #loading json file contents into a dictionary object
#         __locations = __data_columns[3:]  # first 3 columns of this dictionary are sqft, bath, bhk, so the rest corresponds to the location list which we have stored here
#     print("Loading the columns")
#     print(__locations)

#     global __model #reference to global model variable
#     if __model is None:
#         with open('./banglore_home_prices_model.pickle', 'rb') as f: #rb for loading binary file and storing in __model
#             __model = pickle.load(f)
#     print("Model loading done")

#     print("loading saved artifacts...done")  #done loading both artifacts


#home page will show template for prediction
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('app.html')

#endpoint which can be requested to fetch all the location names whenever required in a json format and return it as response
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    #testing our __locations
    global __locations
    if __locations == None:
        response = jsonify({
        'locations': ["1st block jayanagar", "1st phase jp nagar", "2nd phase judicial layout"]
        })
    else:
        response = jsonify({
        'locations': __locations
        })
       
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

#endpoint which is requested with the user prediction query data to fetch the predictions from our model and response is returned as a json
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

#endpoint to test loading of resources
@app.route('/show_resources', methods=['GET', 'POST'])
def show_resources():

    response = jsonify({
        'modelValue': __model,
        'locationsValue': __locations,
        'dataclmValue': __data_columns
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
#     load_saved_artifacts() #loading artifacts on server startup
    app.run() #then running this app (server)
    
    


