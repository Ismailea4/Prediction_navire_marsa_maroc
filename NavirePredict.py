import torch
import torch.nn as nn
import joblib
from sklearn.preprocessing import StandardScaler ,MinMaxScaler
import pandas as pd
import numpy as np
from Predi_data_utile import predict_rf

scalerInput = joblib.load('model/scalerInput.pkl')
scalerOutput = joblib.load('model/scalerOutput.pkl')



class NavirePredictor(nn.Module):
    def __init__(self, input_size, hidden_layer_size, output_size):
        super(NavirePredictor, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        input_seq = input_seq.reshape(len(input_seq), 1, -1)
        lstm_out, self.hidden_cell = self.lstm(input_seq, self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]

model = NavirePredictor(10,100,1)

model.load_state_dict(torch.load('model/modelrnn.pth'))


def predi_nav(data):
    df = scalerInput.transform(data)
    
    df = torch.FloatTensor(df)
    
    df = df.unsqueeze(0)
    df = df.unsqueeze(0)
    
    model.eval()
    
    with torch.no_grad():
        model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))

        # Faire la prédiction
        prediction = model(df)

        predictions = np.array(prediction).reshape(-1, 1)
        predictions_inversed = scalerOutput.inverse_transform(predictions)
    return np.round(predictions_inversed)

def predi_nav_frame(data):
    prediction = []
    for i in range(len(data)):
        df = data.iloc[i,:].values.reshape(1, -1)
        predi = int(predi_nav(df)[0][0])
        prediction.append(predi)
    
    return prediction
        

def predi_frame(date_start,date_end):
    prediction = predict_rf(date_start,date_end)
    prediction['Nombre de Navire'] = predi_nav_frame(prediction)
    
    return np.round(prediction,3)