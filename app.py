
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            pregnancies = float(request.form['pregnancies'])
            glucose = float(request.form['glucose'])
            blood_pressure = float(request.form['blood_pressure'])
            skin_thickness = float(request.form['skin_thickness'])
            insulin = float(request.form['insulin'])
            bmi = float(request.form['bmi'])
            diabetes = float(request.form['diabetes'])
            age = float(request.form['age'])

            # loading scaling function
            scaler_function = 'standardScalar.sav'
            scaler = pickle.load(open(scaler_function, 'rb'))
            # loading the model file from the storage
            filename = 'classificationModel.sav'
            loaded_model = pickle.load(open(filename, 'rb'))  
            # predictions using the loaded model file
            data_scaled = [[pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,diabetes,age]]
            scaled_data = scaler.transform(data_scaled)
            prediction=loaded_model.predict(scaled_data)
            print('prediction is', prediction)
            # showing the prediction results in a UI
            if prediction[0] == 1:
                result = 'Diabetic'
            else:
                result = 'Non-Diabetic'
            return render_template('results.html',result=result)

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	#app.run(debug=True) # running the app
