import requests
import os
from azure_auth import get_credential

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")

def get_costs():
    credential = get_credential()
    token = credential.get_token("https://management.azure.com/.default").token

    url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"

    body = {
        "type": "ActualCost",
        "timeframe": "MonthToDate",
        "dataset": {
            "granularity": "None",
            "aggregation": {
                "totalCost": {
                    "name": "PreTaxCost",
                    "function": "Sum"
                }
            },
            "grouping": [
                {"type": "Dimension", "name": "ResourceType"}
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=body)

    print("STATUS:", r.status_code)
    print("RAW RESPONSE:", r.text)

    return r.text