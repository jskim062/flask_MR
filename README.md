# Flask Image & ML API  
  
This repository provides a Flask-based web API for image processing and machine learning predictions. The API includes endpoints for basic server testing, echoing JSON input, uploading images to retrieve their dimensions, and performing predictions using pre-trained KNN and Keras models.  
  
## Features  
  
- **Hello World Endpoint**: Basic GET endpoint for health check.  
- **Echo Endpoint**: Returns any received JSON payload.  
- **Upload Image Endpoint**: Accepts image files and returns their dimensions.  
- **Predict Score Endpoint**: Predicts a score using a pre-trained KNN model.  
- **Predict Image Endpoint**: Classifies uploaded images as either 'cat' or 'dog' using a Keras model.  
  
## Requirements  
  
- Python 3.7+  
- Flask  
- Pillow  
- scikit-learn (for joblib)  
- keras  
  
Install the required packages:  
  
```bash  
pip install Flask Pillow scikit-learn keras  
```
## Usage

1. Start the Server
Make sure your trained models (knn_model.pkl, save_at_25.keras) are in the project directory.
- python app.py  
2. API Endpoints
  /hello
- Method: GET
- Description: Returns "Hello, World!"
- Sample Request:

curl http://localhost:5000/hello  
/echo
- Method: GET or POST
- Description: Echoes back the JSON data sent in the request.
- Sample Request:
```
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:5000/echo  
```
/upload_image
- Method: GET or POST
- Description: Accepts an image file and returns its width and height.
- Sample Request:
```
curl -X POST -F "file=@your_image.jpg" http://localhost:5000/upload_image  
```
/predict_score
- Method: GET or POST
- Description: Returns a prediction from the KNN model based on the 'horus' parameter.
- Sample Request:
```
curl "http://localhost:5000/predict_score?horus=5.3"  
```
/predict_image
- Method: GET or POST
- Description: Accepts an image file, preprocesses it, and predicts whether it is a 'cat' or 'dog' using the Keras model.
- Sample Request:
```
curl -X POST -F "file=@your_image.jpg" http://localhost:5000/predict_image  
```
## File Structure
- app.py : Main Flask application file.
- knn_model.pkl : Pre-trained KNN model (place in the root directory).
- save_at_25.keras : Pre-trained Keras model (place in the root directory).
## Notes
- Make sure to provide the correct path to your models.
- For best results, use images of size 180x180 pixels for the /predict_image endpoint.
