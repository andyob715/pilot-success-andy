#IMPORT NECESSARY LIBRARIES
from flask import Flask, render_template, request
import pandas as pd 
import pickle
import json
import math

#IMPORT ALL THE THINGS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.datasets import make_regression, make_swiss_roll
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# # SQLALCHEMY SETUP
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func
# import psycopg2

#os allows you to call in environment variables
# we will set the remote environment variables in heroku 
# from dotenv import load_dotenv
# import os 

# load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", 'POST'])
def index():
    return render_template("index.html") 


@app.route("/predict", methods=["GET", 'POST'])
def predict():
        #Line below will load your machine learning model
    # Output = "Your Value Here!"
    
    if request.method == 'POST': 

        # load up the model saved via Pickle
        filename = 'static/pickle/pilot_forest_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        loaded_scaler = pickle.load(open('static/pickle/scaler.pkl', 'rb'))
    
        #grab the elements from the index page entered by user
        input_1=request.json.get("course_input_json")
        input_2=request.json.get("start_month_json")
        input_3=request.json.get("classes_taken_json")
        input_4=request.json.get("expected_days_json")
        input_5=request.json.get("max_flight_hours")

        #update value to integer
        var1 = int(input_1)
        var2 = int(input_2)
        var3 = int(input_3)
        var4 = int(input_4)
        var5 = int(input_5)*240
        
        input_list = ["coursename", "start_month", "course_count", "e2e_course_days"]

        raw_user_input = pd.DataFrame([[var1,var2,var3,var4]],columns=input_list)

        scaled_user_input = loaded_scaler.transform(raw_user_input)
        
        Guess = loaded_model.predict(scaled_user_input)

        Max_Income = var5

        Actual_Cost = Guess[0]*175

        Actual_Income = Guess[0]*240

        if Actual_Income > Max_Income:
            Set_Income = Max_Income
        else: 
            Set_Income = Actual_Income
        
        Net_Income = Set_Income - Actual_Cost

        Income_Ratio = Net_Income / Set_Income

        return {"Prediction": Guess[0],"Max_Income":Max_Income,"Actual_Income":Actual_Income,"Cost":Actual_Cost,"Net_Income":Net_Income,"Income_Pct":Income_Ratio}
        
    return render_template("prediction.html")

if __name__ == '__main__':
    app.run(debug=True)
