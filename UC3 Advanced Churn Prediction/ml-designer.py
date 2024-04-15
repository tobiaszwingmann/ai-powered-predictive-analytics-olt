# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# Imports
import pandas as pd
import json
import requests

# Your Azure Cognitive Services Text Analytics Key and Endpoint
KEY = "xxxxxxxxxxxx"
ENDPOINT = "https://xxxxxxxxxxxx.cognitiveservices.azure.com/"

# Custom Functions

## Get successive n-sized chunks from list.
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## Sentiment Analysis API call
def sentiment_analysis(documents, endpoint, key):
  url = endpoint + "text/analytics/v3.2-preview.1/sentiment?opinionMining=False"

  payload = json.dumps({
      "documents": documents
  })

  headers = {
      "Content-Type": "application/json",
      "Ocp-Apim-Subscription-Key": key,
  }

  result = requests.post(url, data=payload, headers = headers)
  result = json.loads(result.content)
  try:
    result = result['documents']
    doc_result = [doc for doc in result]
    return(doc_result)
  except:
    print(result['error'])
    return(result['error'])

# Main Function
def azureml_main(dataframe1 = None, dataframe2 = None):
  #   Param<dataframe1>: a pandas.DataFrame
  #   Param<dataframe2>: a pandas.DataFrame
    
  # Batch input dataframe in chunks of 10 to not exceed API limit
  batches = list(chunks(dataframe1.index, 10))
  results = []
  for batch in batches:
    documents_batch = dataframe1.loc[batch]
    documents_batch = documents_batch.to_dict("records")
    results_batch = sentiment_analysis(documents_batch, ENDPOINT, KEY)
    results.append(results_batch)

  # Flatten list
  results = [doc for batch in results for doc in batch]
  results_df = pd.DataFrame(results)

  # Get sentiment from results
  dataframe1 = dataframe1.merge(results_df[['id', 'sentiment']], on = "id", how = "left")

  return(dataframe1)