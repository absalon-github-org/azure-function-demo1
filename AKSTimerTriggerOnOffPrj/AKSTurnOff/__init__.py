import datetime
import logging
import requests
import json

import azure.functions as func

# Tennat / Subscription
subscription_id = 'c9ba6f43-025f-4a57-8414-4cb09f01a872'
tennat_id = '60256843-8a51-4b3b-b260-54d8d161690e'

# AKS
resourceGroupName = 'terraform-aks-labcluster1'
resourceName = 'terraform-aks-labcluster1-cluster'

# Service principal
client_id="b6369d52-672c-4efd-9122-5d2b8fadd92b"
client_secret="gml8Q~q5x8oEvRudDn4Mf~T8X2QkidLPeHYOJaWb"

def main(mytimer: func.TimerRequest) -> None:
    # utc_timestamp = datetime.datetime.utcnow().replace(
    #     tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due! from Github action')

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    data= {
            'client_id':client_id, 
            'client_secret': client_secret , 
            'grant_type': 'client_credentials',
            'scope':'https://management.azure.com/.default'
        }

    logging.info("Obteniendo access_token ...")

    req = requests.post("https://login.microsoftonline.com/"+
            str(tennat_id)+"/oauth2/v2.0/token",headers=headers,data=data)

    js = json.loads(req.text)
    access_token = js['access_token']
    logging.info(str(access_token))

    headers = {'Authorization': 'Bearer '+ str(access_token)}

    logging.info("Stopping AKS...")
    try:
        req = requests.post(
            "https://management.azure.com/subscriptions/"+subscription_id+
            "/resourceGroups/"+resourceGroupName+
            "/providers/Microsoft.ContainerService/managedClusters/"+resourceName+
            "/stop?api-version=2022-04-01",headers=headers
        )

        logging.info("Response stop AKS http status: "+str(req.status_code))
    except Exception as e:
        logging.info("Error al llamar API de Stop AKS")
        logging.info(str(e))
