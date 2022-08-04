import pickle
import json
import numpy as np

#global variables storing set of locations,data columns and the model itself
__locations = None
__data_columns = None
__model = None

#getting estimated price from the loaded model
def get_estimated_price(location,sqft,bhk,bath):
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


def load_saved_artifacts():
    #function to load artifacts(the model and the column list) to be called from the server
    print("loading saved artifacts...start")
    #reference to global variables
    global  __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f: #opening the json file
        __data_columns = json.load(f)['data_columns'] #loading json file contents into a dictionary object
        __locations = __data_columns[3:]  # first 3 columns of this dictionary are sqft, bath, bhk, so the rest corresponds to the location list which we have stored here

    global __model #reference to global model variable
    if __model is None:
        with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as f: #rb for loading binary file and storing in __model
            __model = pickle.load(f)
    print("loading saved artifacts...done")  #done loading both artifacts

def get_location_names(): #returns the location list
    return __locations

def get_data_columns(): #returns the data columns list
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts() #loading artifacts into the corresponding global variables
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location