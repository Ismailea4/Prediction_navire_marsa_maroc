import joblib
import pandas as pd

def date_to_frame(date_start,date_end):
    df = pd.date_range(start=date_start, end=date_end, freq='D')
    df = pd.DataFrame(df,index=df.values,columns=['date'])
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month
    df['Day'] = df['date'].dt.day
    df['DayofWeek'] =df['date'].dt.day_of_week
    return df.drop('date',axis=1)


def predict_rf(date_start,date_end):
    X = date_to_frame(date_start,date_end)
    model = {}
    y_pred = {}
    columns = ['tavg','prcp','wspd','pres','exchange rate','oil value']
    for col in columns:
        model[col] = joblib.load('model/model_'+col+'.pkl')
        y_pred[col] = model[col].predict(X)

    prediction = pd.DataFrame(y_pred,index = X.index.values)
    prediction[['Year','Month','Day','DayofWeek']] = X[['Year','Month','Day','DayofWeek']]
    
    prediction.columns = ['Temperature Moyenne','Precipitation','Vitesse du vent','Pression atmospherique au niveau de la mer','Exchange Rate','Oil Value','Year','Month','Day','Day of week']
    
    return prediction