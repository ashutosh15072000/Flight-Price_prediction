# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 14:56:45 2022

@author: ayush
"""

import pandas as pd
import pickle
import re
loaded_model = pickle.load(open('finalized_model.pkl','rb'))
s=loaded_model['Noramlization']
model=loaded_model['model']


def test_set_preprocessing(test_set):
## Changing Date of Journey column Datatype 
    test_set['Date_of_Journey']=pd.to_datetime(test_set['Date_of_Journey'])
    ## only taking arrival time ie hr:min some of values are '12:56 10 Mar'
    pattern='\d{2}:\d{2}'
    test_set['Arrival_Time']=test_set['Arrival_Time'].apply(lambda x:re.findall(pattern,x)[0])
    ## In Duration Column Adding 00m Where only Hr is given
    ## After that we Calualate total duration in minutes
    pattern='\d{1,2}\w\s\d{2}\w'
    Time=[]
    for time in test_set['Duration']:
        if re.findall(pattern,time):
            Time.append(time)    
        else:
            time=time+' '+'00m'
            Time.append(time)
    test_set['Duration']=Time
    hour=test_set['Duration'].apply(lambda x:x.split(' ')[0][:-1]).astype('int')
    minute=test_set['Duration'].apply(lambda x:x.split(' ')[1][:-1]).astype('int')
    test_set['Duration']=hour*60+minute
    ## extracting Day and month
    test_set['month']=test_set['Date_of_Journey'].dt.month
    test_set['Day']=test_set['Date_of_Journey'].dt.day
    test_set.drop('Date_of_Journey',axis=1,inplace=True)
    ## creating new col from dep_time .
    test_set['Dep_hour']=(test_set['Dep_Time'].apply(lambda x:x.split(':')[0])).astype('int')
    test_set['Dep_min']=(test_set['Dep_Time'].apply(lambda x:x.split(':')[1])).astype('int')
    ## creating new col from arrival_time
    test_set['Arrival_hour']=(test_set['Arrival_Time'].apply(lambda x:x.split(':')[0])).astype('int')
    test_set['Arrival_min']=(test_set['Arrival_Time'].apply(lambda x:x.split(':')[1])).astype('int')
    test_set.drop(['Arrival_Time','Dep_Time'],1,inplace=True)
    # As this is case of Ordinal Categorical type we perform LabelEncoder
    # Here Values are assigned with corresponding keys
    test_set['Total_Stops']=test_set['Total_Stops'].replace({"1 stop":1,'non_stop':0,'2 stops':2,'3 stops':3,'4 stops':3})
    # Additional_Info contains almost 80% no_info
    test_set.drop(['Additional_Info'],1,inplace=True)
    ## dropping the Route col from dataset
    test_set.drop(['Route'],1,inplace=True)
    
    test_set['Destination']=(test_set['Destination'].replace({'New Delhi':'Delhi'}))
    ## # As Source is Nominal Categorical data we will perform OneHotEncoding
    
    if test_set['Airline'][0]=='IndiGo':                          
        test_set['Airline_Air India']=0                         
        test_set['Airline_GoAir'] =0  
        test_set['Airline_IndiGo']=1                                                     
        test_set['Airline_Jet Airways' ]= 0                       
        test_set['Airline_Jet Airways Business'  ] =0           
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
    
    elif test_set['Airline'][0]=='Air India'  :                         
        test_set['Airline_Air India']=1                        
        test_set['Airline_GoAir'] =0 
        test_set['Airline_IndiGo']=0                                                       
        test_set['Airline_Jet Airways' ]= 0                       
        test_set['Airline_Jet Airways Business'  ] =0           
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
    
    elif test_set['Airline'][0]=='GoAir'  :                         
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =1
        test_set['Airline_IndiGo']=0                                                       
        test_set['Airline_Jet Airways' ]= 0                       
        test_set['Airline_Jet Airways Business'  ] =0           
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
        
        
    elif test_set['Airline'][0]=='Jet Airways'  :                          
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0
        test_set['Airline_IndiGo']=0                                                       
        test_set['Airline_Jet Airways' ]= 1                      
        test_set['Airline_Jet Airways Business'  ] =0           
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
        
        
    elif test_set['Airline'][0]=='Jet Airways Business'  :                         
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0
        test_set['Airline_IndiGo']=0                                                       
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =1         
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
        
    
    elif test_set['Airline'][0]=='Multiple carriers'  :
                                  
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0
        test_set['Airline_IndiGo']=0                                                     
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =0         
        test_set['Airline_Multiple carriers']= 1                 
        test_set['Airline_Multiple carriers Premium economy']= 0 
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
        
    elif test_set['Airline'][0]=='Multiple carriers Premium economy'  :                          
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0 
        test_set['Airline_IndiGo']=0                                                      
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =0         
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 1
        test_set['Airline_SpiceJet']=0                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0
        
    elif test_set['Airline'][0]=='SpiceJet'  :
                                  
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0
        test_set['Airline_IndiGo']=0                                                       
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =0         
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0
        test_set['Airline_SpiceJet']=1                          
        test_set['Airline_Vistara']=0  
        test_set['Airline_Vistara Premium economy']=0    
    
    
    elif test_set['Airline'][0]=='Vistara'  :
                                 
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0 
        test_set['Airline_IndiGo']=0                                                      
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =0         
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0
        test_set['Airline_SpiceJet']=0                         
        test_set['Airline_Vistara']=1 
        test_set['Airline_Vistara Premium economy']=0  
        
    else:
                               
        test_set['Airline_Air India']=0                        
        test_set['Airline_GoAir'] =0 
        test_set['Airline_IndiGo']=0                                                      
        test_set['Airline_Jet Airways' ]= 0                     
        test_set['Airline_Jet Airways Business'  ] =0         
        test_set['Airline_Multiple carriers']= 0                 
        test_set['Airline_Multiple carriers Premium economy']= 0
        test_set['Airline_SpiceJet']=0                         
        test_set['Airline_Vistara']=0
        test_set['Airline_Vistara Premium economy']=1
        
        
    if test_set['Source'][0]=='Banglore':
        test_set['Source_Chennai']=0                           
        test_set['Source_Delhi']=0                              
        test_set['Source_Kolkata']= 0                            
        test_set['Source_Mumbai']=0
        
        
    elif  test_set['Source'][0]=='Chennai':
        test_set['Source_Chennai']=1                           
        test_set['Source_Delhi']=0                              
        test_set['Source_Kolkata']= 0                            
        test_set['Source_Mumbai']=0
        
        
    elif  test_set['Source'][0]=='Delhi':
        test_set['Source_Chennai']=0                          
        test_set['Source_Delhi']=1                              
        test_set['Source_Kolkata']= 0                            
        test_set['Source_Mumbai']=0
        
    elif  test_set['Source'][0]=='Kolkata':
        test_set['Source_Chennai']=0                          
        test_set['Source_Delhi']=0                              
        test_set['Source_Kolkata']= 1                           
        test_set['Source_Mumbai']=0
    
    else:
        test_set['Source_Chennai']=0                          
        test_set['Source_Delhi']=0                              
        test_set['Source_Kolkata']= 0                            
        test_set['Source_Mumbai']=1
        
        
        
    if test_set['Destination'][0]=='Banglore':
        test_set['Destination_Cochin']=0                           
        test_set['Destination_Delhi']=0
        test_set['Destination_Hyderabad']=0
        test_set['Destination_Kolkata']= 0    
        
    elif test_set['Destination'][0]=='Cochin':
        test_set['Destination_Cochin']=1                          
        test_set['Destination_Delhi']=0
        test_set['Destination_Hyderabad']=0
        test_set['Destination_Kolkata']= 0
    
    elif test_set['Destination'][0]=='Delhi':
        test_set['Destination_Cochin']=0                           
        test_set['Destination_Delhi']=1
        test_set['Destination_Hyderabad']=0
        test_set['Destination_Kolkata']= 0
        
    elif test_set['Destination'][0]=='Hyderabad':
        test_set['Destination_Cochin']=0                           
        test_set['Destination_Delhi']=0
        test_set['Destination_Hyderabad']=1
        test_set['Destination_Kolkata']= 0
        
    else:
        test_set['Destination_Cochin']=0                           
        test_set['Destination_Delhi']=0
        test_set['Destination_Hyderabad']=0
        test_set['Destination_Kolkata']= 1
    test_set.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
    normalization=['Duration','Total_Stops','month','Day','Dep_hour','Dep_min','Arrival_hour','Arrival_min']
    test_set[normalization]=s.transform(test_set[normalization])
   
    
    
    
    return test_set