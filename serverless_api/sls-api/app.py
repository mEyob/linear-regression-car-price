import numpy as np
from collections import namedtuple
from flask import Flask, request, jsonify, render_template

model = namedtuple('model', 'coef_ intercept_ pred_interval')
toyota_model = model(coef_=np.array([ -772, -1008, 1457, 4775, 2185]), intercept_=30514, pred_interval=3600)
honda_model = model(coef_=np.array([-1346, -1051, 921,  2610, 1310, 6272]), intercept_=39554, pred_interval=4100)
hyundai_model = model(coef_=np.array([-1194, -766, 34,  1460, 2354]), intercept_=34093, pred_interval=3400)
nissan_model = model(coef_=np.array([-1238, -780,  0, -253, 405]), intercept_=35730, pred_interval=3000)
ford_model = model(coef_=np.array([-1169, -920, 813, 954, 3405, 4596]), intercept_=34026, pred_interval=3800)

app = Flask(__name__) #Initialize the flask App

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    car_model = request.form.get('model')
    year = request.form.get('year')
    trim = request.form.get('trim')
    trim = trim.lower()
    mileage = request.form.get('mileage')
    # features = [x for x in request.form.values()]
    if car_model == 'camry':
        trim_level = [1 if entry else 0 for entry in [trim == 'xle', trim == 'xse', trim == 'hybrid']]
        prediction = toyota_model.coef_.dot(np.array([np.log2(int(mileage)), 2019 - int(year), *trim_level])) + toyota_model.intercept_
        prediction_interval = toyota_model.pred_interval
    elif car_model == 'accord':
        trim_level = [1 if entry else 0 for entry in [trim == 'ex', trim == 'exl', trim == 'sport', trim == 'touring']]
        prediction = honda_model.coef_.dot(np.array([np.log2(int(mileage)), 2019 - int(year), *trim_level])) + honda_model.intercept_
        prediction_interval = honda_model.pred_interval
    elif car_model == 'altima':
        trim_level = [1 if entry else 0 for entry in [trim == 'sr', trim == 'sv', trim == 'sl']]
        prediction = nissan_model.coef_.dot(np.array([np.log2(int(mileage)), 2019 - int(year), *trim_level])) + nissan_model.intercept_
        prediction_interval = nissan_model.pred_interval
    elif car_model == 'sonata':
        trim_level = [1 if entry else 0 for entry in [trim ==  'sel', trim == 'sport', trim == 'limited']]
        prediction = hyundai_model.coef_.dot(np.array([np.log2(int(mileage)), 2019 - int(year), *trim_level])) + hyundai_model.intercept_
        prediction_interval = hyundai_model.pred_interval
    elif car_model == 'fusion':
        trim_level = [1 if entry else 0 for entry in [trim == 'se', trim == 'sel', trim == 'titanium', trim == 'sport']]
        prediction = ford_model.coef_.dot(np.array([np.log2(int(mileage)), 2019 - int(year), *trim_level])) + ford_model.intercept_
        prediction_interval = ford_model.pred_interval
    prediction = round(prediction)
    lower = prediction - prediction_interval
    upper = prediction + prediction_interval
    return render_template(
        'index.html', 
        prediction_text='Estimated average price: ${}'.format(int(prediction)), 
        interval_text='Estimated price range: ${} - ${}'.format(int(lower), int(upper))
        )

if __name__ == "__main__":
    app.run(debug=True)