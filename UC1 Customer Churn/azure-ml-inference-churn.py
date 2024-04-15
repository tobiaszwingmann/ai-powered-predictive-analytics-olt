# SECTION 0: Setup and Variables ----

# Make sure these packages are installed
import pandas as pd
import requests
import json

API_KEY = ""
API_URL = "http://xxxxxxxxxxxxxxxxxxxxxx.eastus2.azurecontainer.io/score"


# SECTION 1: API Request Function ----

def inference_request(DayOfWeek, Origin, Dest, DepDelay, DepDelayMinutes, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, ArrTimeBlk, Distance, DistanceGroup):
  
  # Bind columns to dataframe
  request_df = pd.DataFrame({"DayOfWeek":DayOfWeek, "Origin":Origin, "Dest":Dest, "DepDelay":DepDelay, "DepDelayMinutes":DepDelayMinutes, "DepDel15":DepDel15, "DepartureDelayGroups":DepartureDelayGroups, "DepTimeBlk":DepTimeBlk, "TaxiOut":TaxiOut, "ArrTimeBlk":ArrTimeBlk, "Distance":Distance, "DistanceGroup":DistanceGroup})
  
  req = {
      "Inputs": {
          "data": list(request_df.to_dict('records'))
          },
         "GlobalParameters": {
             "method": "predict"
             }
         }
        
  # POST request - send JSON to API
  headers = {'Authorization': ('Bearer ' + API_KEY), 
             'Content-Type': 'application/json'}

  result = requests.post(API_URL, data = str.encode(json.dumps(req)), headers=headers)
  return(result)


# SECTION 2: Data preprocessing ----
# Fetch data from Power Query workflow
df = dataset


# SECTION 3: Get Predictions ----
result = inference_request(df['DayOfWeek'], df['Origin'], df['Dest'], df['DepDelay'], df['DepDelayMinutes'], df['DepDel15'], df['DepartureDelayGroups'], df['DepTimeBlk'], df['TaxiOut'], df['ArrTimeBlk'], df['Distance'], df['DistanceGroup'])


# SECTION 4: Data postprocessing ----
result = pd.DataFrame(json.loads(result.content))
df['ArrDel15_Prediction'] = result

# SECTION 5: Format output for Power BI ----
output = df

