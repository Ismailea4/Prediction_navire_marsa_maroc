from flask import Flask, render_template, request, jsonify, send_file,url_for
import pandas as pd
from ConteneurPredict import predi_cont1,predi_cont2,predict_conteneur
from NavirePredict import predi_nav,predi_nav_frame,predi_frame
from werkzeug.utils import secure_filename
import os
from datetime import datetime

navires = pd.read_csv('data/NAVIRES.csv').sort_values(by=['NOM NAVIRE'])

ship_names = navires['NOM NAVIRE'].unique().tolist()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Your prediction function here

@app.route('/')
def home():
    min_date = datetime.today().strftime('%Y-%m-%d')

    return render_template('home.html')

@app.route('/predictionConteneur', methods=['GET','POST'])
def predictionConteneur():
    min_date = datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        data = request.get_json()
        name_ship = data.get('name_ship')
        ETA_date = data.get('ETA_date')
        Num_loyd = navires[navires['NOM NAVIRE']==name_ship]['N° LOYD NAVIRE'].values[0]
        prediction = predict_conteneur(name_ship, ETA_date)
        result = {
            'name_ship': name_ship.strip(),
            'N_LOYD_NAVIRE': int(Num_loyd),
            'ETA_date': ETA_date,
            'container_2': float(prediction[0][0]),
            'container_4': float(prediction[1][0])
        }
        return jsonify(result)
    return render_template('predictionConteneur.html',min_date=min_date,ship_names=ship_names)

@app.route('/predictShip', methods=['GET','POST'])
def predictShip():
    min_date = datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        data = request.get_json()
        start_date = data['start_date']
        end_date = data['end_date']
        
        predictions = predi_frame(start_date, end_date)
        predictions['Date'] = pd.date_range(start=start_date, end=end_date, freq='D')
        predictions['Date'] = predictions['Date'].dt.strftime('%Y-%m-%d')
        predictions.drop(['Year','Month','Day of week','Day'],axis=1,inplace=True)
        response_data = predictions.to_dict(orient='records')
        return jsonify({'data': response_data})
    return render_template('predictShip.html',min_date=min_date)


@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        plot_type = request.form['plot_type']
        year = request.form['year']
        image_filename = f'{plot_type}_{year}.png'  # Assume images are named in this format
        image_url = url_for('static', filename=f'images/{image_filename}')
        return jsonify({'image_url': image_url})
    return render_template('visualization.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
