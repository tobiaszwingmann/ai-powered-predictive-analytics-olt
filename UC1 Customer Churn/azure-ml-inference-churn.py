# SECTION 0: Setup and Variables ----

# Make sure these packages are installed
import pandas as pd
import requests
import json

API_KEY = ""
API_URL = "http://xxxxxxxxxxxxxxxxxxxxxx.eastus2.azurecontainer.io/score"


# SECTION 1: API Request Function ----

def inference_request(df):

  # Define the expected order of columns as per the model's training
  expected_columns = [
      "Country", "State", "City", "Senior Citizen", "Partner", "Dependents", 
      "Tenure Months", "Phone Service", "Multiple Lines", "Internet Service", 
      "Online Security", "Online Backup", "Device Protection", "Tech Support", 
      "Streaming TV", "Streaming Movies", "Contract", "Paperless Billing", 
      "Payment Method", "Monthly Charges", "Total Charges", "CLTV"
  ]

  # Bind columns to dataframe
  request_df = df[expected_columns]
  
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
result = inference_request(df)


# SECTION 4: Data postprocessing ----
result = pd.DataFrame(json.loads(result.content))
df['Churn_AzureML_Prediction'] = result

# SECTION 5: Format output for Power BI ----
output = df

