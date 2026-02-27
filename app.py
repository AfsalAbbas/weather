from flask import Flask,render_template,request,redirect,session
import pickle
import numpy as np

app=Flask(__name__)

with open('rfc-weather.pkl','rb') as file:
    model=pickle.load(file)
    print(model)

with open('scaler-weather.pkl','rb') as file:
    scaler=pickle.load(file)
    print(scaler)


def predict_weather(Temperature=40,Humidity=96, Wind_Speed=1,Precipitation=88,Cloud_Cover='clear',Atmospheric_Pressure=1021.63,
                    UV_Index=0,Season='Summer',Visibility=7.5,Location='mountain'):
    temp_array=list()

    if Cloud_Cover=='overcast':
        temp_array=temp_array+[1,0,0,0]
    elif Cloud_Cover=='partly cloudy':
        temp_array=temp_array+[0,1,0,0]
    elif Cloud_Cover=='clear':
        temp_array=temp_array+[0,0,1,0]
    elif Cloud_Cover=='cloudy':
        temp_array=temp_array+[0,0,0,1]


    if Season=='Autumn':
        temp_array=temp_array+[0]
    elif Season=='Spring':
        temp_array=temp_array+[1]
    elif Season=='Summer':
        temp_array=temp_array+[2]
    elif Season=='Winter':
        temp_array=temp_array+[3]

    
    if Location=='mountain':
        temp_array=temp_array+[1,0,0]
    elif Location=='inland':
        temp_array=temp_array+[0,1,0]
    elif Location=='coastal':
        temp_array=temp_array+[0,0,1]

    temp_array=temp_array+[Temperature]
    temp_array=temp_array+[Humidity]
    temp_array=temp_array+[Wind_Speed]
    temp_array=temp_array+[Precipitation]
    temp_array=temp_array+[Atmospheric_Pressure]
    temp_array=temp_array+[UV_Index]
    temp_array=temp_array+[Visibility]

    temp_array=np.array([temp_array])
    print(temp_array)
    temp_array=scaler.transform(temp_array)
    pred=model.predict(temp_array)[0]
    print(pred)
    if pred == 0:
        result = 'Cloudy'
    elif pred == 1:
        result = 'Rainy'
    elif pred == 2:
        result = 'Snowy'
    else:
        result = 'Sunny'

    return result

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/predict",methods=['POST','GET'])

def predict():
    if request.method=='POST':
        Temperature=float(request.form.get('Temperature'))
        Humidity=int(request.form.get('Humidity'))
        Wind_Speed=float(request.form.get('Wind_Speed'))
        Precipitation=float(request.form.get('Precipitation'))
        Cloud_Cover=request.form.get('Cloud_Cover')
        Atmospheric_Pressure=float(request.form.get('Atmospheric_Pressure'))
        UV_Index=int(request.form.get('UV_Index'))
        Season=request.form.get('Season')
        Visibility=float(request.form.get('Visibility'))
        Location=request.form.get('Location')

        weather=predict_weather(Temperature=Temperature,Humidity=Humidity,Wind_Speed=Wind_Speed,Precipitation=Precipitation,Cloud_Cover=Cloud_Cover,
                                Atmospheric_Pressure=Atmospheric_Pressure,UV_Index=UV_Index,Season=Season,Visibility=Visibility,Location=Location)
        print(weather)
        return render_template('predict.html', prediction=weather)
    return render_template('predict.html')
    

if __name__=='__main__':
    app.run(debug=True,port=9000,host='0.0.0.0')