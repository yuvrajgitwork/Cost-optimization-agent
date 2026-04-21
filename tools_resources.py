import requests
import os
from azure_auth import get_credential

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

def get_resources():
    credential = get_credential()
    token = credential.get_token("https://management.azure.com/.default").token

    url = f"https://management.azure.com/providers/Microsoft.ResourceGraph/resources?api-version=2021-03-01"

    query = {
        "subscriptions": [SUBSCRIPTION_ID],
        "query": "resources | project name, type, location"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=query)
    print("RES STATUS:", r.status_code)
    print("RES RAW:", r.text)

    return r.text