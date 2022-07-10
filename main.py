

import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import helper
import pickle
from sklearn.ensemble import GradientBoostingRegressor


flight=pd.read_excel('Data_Train.xlsx')
print(flight)



image = Image.open('Flight-Price-Prediction.png')

st.image(image, caption='Flight Price Prediction')



st.header("DataFrame")
st.dataframe(flight)


with st.form(key='my-form'):
    airline=sorted(flight['Airline'].unique())
    Airline=st.sidebar.selectbox(label='Airline Company', options=airline)
    
    
    stops=['non_stop','1 stop','2 stops','3 stops','4 stops']
    Stops=st.sidebar.selectbox(label='Total Stops', options=stops)
    
    
    Source=sorted(flight['Source'].unique())
    source=st.sidebar.selectbox(label='Source', options=Source)
    
    
    Destination=sorted(flight['Destination'].unique())
    destination=st.sidebar.selectbox(label='Destination', options=Destination)
    
    date = st.sidebar.date_input("Date of Journey",datetime.date(2019, 1, 1))
    
    Departure = st.sidebar.text_input('Departure Time', '00:00')
    Arrival= st.sidebar.text_input('Arrival Time', '00:00')
    
    
    Duration = st.sidebar.text_input('Duration', '00h 00m')
    
    
    df={'Airline':[],'Date_of_Journey':[],'Source':[],'Destination':[],'Route':[],'Additional_Info':[],'Duration':[],'Dep_Time':[],'Arrival_Time':[],'Total_Stops':[]}
    
    df['Airline'].append(Airline)
    df['Date_of_Journey'].append(date)
    df['Source'].append(source)
    df['Destination'].append(destination)
    df['Dep_Time'].append(Departure)
    df['Arrival_Time'].append(Arrival)
    df['Total_Stops'].append(Stops)
    df['Route'].append(0)
    df['Additional_Info'].append(0)
    df['Duration'].append(Duration)
    test_set=pd.DataFrame(df)
    submit_button=st.form_submit_button(label='Price Prediciton')
    
if  submit_button:   
    test_set=helper.test_set_preprocessing(test_set)
    loaded_model = pickle.load(open('finalized.pkl','rb'))
    model=loaded_model['model']
    price=model.predict(test_set)
    image = Image.open('istockphoto-1131335393-612x612.jpg')
    st.image(image)
    st.success(f'₹{round(price[0])}')
    st.balloons()
  


        

           
            



        

           
            
