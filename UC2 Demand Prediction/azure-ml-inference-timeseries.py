# SECTION 0: Setup and Variables ----

# Make sure these packages are installed
import pandas as pd
import requests
import json

API_KEY = ""
API_URL = "http://xxxxxxxxxxxxxxxxxxxxxxx.xxxx.azurecontainer.io/score"


# SECTION 1: API Request Function ----

def inference_request(timestamp, temp):
  
  # Bind columns to dataframe
  request_df = pd.DataFrame({"timeStamp":timestamp, "temp":temp})
  
  req = {
      "Inputs": {
          "data": list(request_df.to_dict('records'))
          },
         "GlobalParameters": {
             "quantiles": [0.025,0.975]
             }
         }
        
  # POST request - send JSON to API
  headers = {'Authorization': ("Bearer " + API_KEY), 
             'Content-Type': 'application/json'}

  result = requests.post(API_URL, data = str.encode(json.dumps(req)), headers=headers)
  return(result)


# SECTION 2: Data preprocessing ----
# Fetch data from Power Query workflow
df = dataset


# SECTION 3: Get Predictions ----
result = inference_request(df['timeStamp'], df['temp'])


# SECTION 4: Data postprocessing ----
result =  json.loads(result.content)

# Convert result to dataframe
results_df = pd.DataFrame(result['Results'])

# Move prediction intervals to separate columns
lower = []
upper = []
for element in results_df['prediction_interval']:
  lower.append(json.loads(element)[0])
  upper.append(json.loads(element)[1])

df['prediction_interval_lower'] = lower
df['prediction_interval_upper'] = upper
df['forecast'] = results_df['forecast']

# SECTION 5: Format output for Power BI ----
output = df