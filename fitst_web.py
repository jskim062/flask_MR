from flask import Flask, request, jsonify  # Import Flask framework and request/response utilities  
from PIL import Image                     # Import Pillow for image processing  
import joblib
import os
import numpy as np
import keras
from keras import layers
from tensorflow import data as tf_data
import tensorflow
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
loaded_model1 = joblib.load('./knn_model.pkl')
loaded_model = keras.models.load_model("save_at_25.keras")
app = Flask(__name__)                     # Create a Flask application  

@app.route('/hello')                      # Handle GET requests to '/hello'  
def hello_world():  
    return 'Hello, World!'                # Return a simple greeting  
  
@app.route('/echo', methods=['POST','GET'])   # Handle POST and GET requests to '/echo'  
def post_echo_call():  
    param = request.get_json()                # Parse JSON data from the request  
    return jsonify(param)                     # Return the parsed JSON as a response  
  
@app.route("/upload_image", methods=['POST','GET'])    # Handle POST and GET requests to '/upload_image'  
def home():  
    img = Image.open(request.files['file'])             # Open the uploaded file as an image  
    width, height = img.size                            # Get the image's width and height  
    return jsonify({"width": width, "height": height})  # Return the dimensions as a JSON response  
  
@app.route("/predict_score", methods=['POST','GET'])    # Handle POST and GET requests to '/upload_image'  
def Predict_sc():  
    '''
    X = request.get_json()
    y_pred = loaded_model1.predict(X)
    return jsonify(y_pred)
    '''  
    horus_value = request.args.get('horus')
    horus_value = float(horus_value)   
    y_pred = loaded_model1.predict([[horus_value]])
    return jsonify({"prediction": float(y_pred[0])})

@app.route("/predict_image", methods=['POST','GET'])    # Handle POST and GET requests to '/upload_image'  
def pridict_img():  
    image_size = (180, 180)
    
    img = Image.open(request.files['file'])
    img = img.resize(image_size)


    img_array = keras.utils.img_to_array(img)
    img_array = keras.ops.expand_dims(img_array, 0)  # Create batch axis

    predictions = loaded_model.predict(img_array)
    score = float(keras.ops.sigmoid(predictions[0][0]))
    if score > 50:
        return jsonify({"predict_result": "cat"})
    else:
        return jsonify({"predict_result": "dog"})


if __name__ == "__main__":    # Run the app only if this file is executed directly  
    app.run()                 # Start the Flask development server
