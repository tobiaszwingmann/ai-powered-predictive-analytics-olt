# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# Imports
import pandas as pd
import json
import requests

# Your Azure Cognitive Services Text Analytics Key and Endpoint
KEY = "xxxxxxxxxxxxxxxxxxx"
ENDPOINT = "https://xxxxxxxxxxxxxxxxxxxx.cognitiveservices.azure.com/"

# Custom Functions

## Get successive n-sized chunks from list.
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## Sentiment Analysis API call
def sentiment_analysis(documents, endpoint, key):
  url = endpoint + "/language/:analyze-text?api-version=2023-04-15-preview"
# Adding empty header as parameters are being sent in payload
  payload = json.dumps({
      "kind": "SentimentAnalysis",
      "parameters": {
          "modelVersion": "latest",
          "opinionMining": "False"
          },
      "analysisInput":{
          "documents":documents
          }
  })

  headers = {
      "Content-Type": "application/json",
      "Ocp-Apim-Subscription-Key": key,
  }

  result = requests.post(url, data=payload, headers = headers)
  result = json.loads(result.content)
  try:
    result = result['results']['documents']
    doc_result = [doc for doc in result]
    return(doc_result)
  except:
    print(result)
    return(result)

# Main Function
def azureml_main(dataframe1 = None, dataframe2 = None):
  #   Param<dataframe1>: a pandas.DataFrame
  #   Param<dataframe2>: a pandas.DataFrame
    
  # Batch input dataframe in chunks of 10 to not exceed API limit
  batches = list(chunks(dataframe1.index, 10))
  results = []
  for batch in batches:
    documents_batch = []
    df = dataframe1.loc[batch]
    results_batch = sentiment_analysis(df[['id', 'text']].to_dict('records'), ENDPOINT, KEY)
    results.append(results_batch)

  # Flatten list
  results = [doc for batch in results for doc in batch]

  # Get sentiment from results
  sentiment = []
  for result in results:
    try:
      sentiment.append(result['sentiment'])
    except:
      sentiment.append('Error, please check logs')
  
  dataframe1['sentiment'] = sentiment
  return(dataframe1)
