import pickle
import os
from webbrowser import get
import pandas as pd
from sklearn.preprocessing import StandardScaler

#to get the current working directory
directory = os.getcwd()

def get_random_forest():
    file = directory+'/model_anouar/model.pkl'
    if os.path.exists(file):
        pickle_in = open(file, 'rb')
        model = pickle.load(pickle_in)
        pickle_in.close()
        print('model : ', type(model))
        print('parameters : ', model.get_params)
        print("Model successfully loaded!")
        return model
        #result = loaded_model.score(X_test, Y_test)
        #print(result)
    print('Sorry no model :(')

def scale_data(data):
    scaler = StandardScaler()
    return scaler.fit_transform(data)