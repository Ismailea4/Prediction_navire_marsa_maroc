from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder,StandardScaler
from Predi_data_utile import predict_rf

navires = pd.read_csv('data/NAVIRES.csv')
def predict_conteneur(nom_navire,ETA):
    df = navires[navires['NOM NAVIRE']==nom_navire][['N° LOYD NAVIRE','LONGUEUR NAVIRE', "TIRANT D'EAU"]]
    
    date = datetime.strptime(ETA, '%Y-%m-%d').date()
    df['ETA_year'] = [date.year]
    df['ETA_month'] = [date.month]
    df['ETA_day'] = [date.day]
    meteo = predict_rf(date,date)

    df['tavg'] = meteo['Temperature Moyenne'].values
    df['wspd'] = meteo['Vitesse du vent'].values
    df['pres'] = meteo['Pression atmospherique au niveau de la mer'].values
    
    
    NBTC2 = predi_cont1(df)
    NBTC4 = predi_cont2(df)
    
    return (NBTC2,NBTC4)
def predi_cont1(data):
    # Charger le modèle depuis le disque
    model = joblib.load('model/random_forest_model_conteneur1.pkl')
    
    le = joblib.load('model/label_encoder_N_LOYD.pkl')
    scalerr = joblib.load('model/X_scaled.pkl')
    data_scaled = scalerr.transform(data)

    return np.round(model.predict(data_scaled))
    
def predi_cont2(data):
    # Charger le modèle depuis le disque
    model = joblib.load('model/random_forest_model_conteneur2.pkl')
    
    le = joblib.load('model/label_encoder_N_LOYD.pkl')
    scalerr = joblib.load('model/X_scaled.pkl')
    data_scaled = scalerr.transform(data)

    return np.round(model.predict(data_scaled))