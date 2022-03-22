import pickle
import os
import pandas as pd

#to get the current working directory
directory = os.getcwd()

def get_decision_tree():
    file = directory+'/model_audrey/save/decision_tree_regressor.pickle'
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

def get_decision_tree_rfe():
    file = directory+'/model_audrey/save/decision_tree_regressor_rfe.pickle'
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


def get_data_from_csv():
    df = pd.read_csv(directory+'/model_audrey/data/dataAuto_clean.csv', sep = ';', header=0, usecols=['Marque', 'Carburant','Transmission','Emission Co2','nbPortes','nbPlace'])
    
    marques_under_mean = []
    s = df.Marque.value_counts() > df.Marque.value_counts().mean()
    for marque, bool in s.items():
        if bool == False:
            marques_under_mean.append(marque)
    df = df[df.Marque.isin(marques_under_mean) == False]

    criterias = {}
    for col in df.columns:
        items = set(pd.Series(df[col]))
        names = {}
        index = 1
        for i in sorted(items):
            names[index] = i
            index += 1
        criterias[col] = names

    return criterias
        