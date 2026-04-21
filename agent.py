from dotenv import load_dotenv
load_dotenv()
from openai import AzureOpenAI
import os
from tools_costs import get_costs
from tools_resources import get_resources

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def analyze_azure_costs(question: str):
    costs = get_costs()
    resources = get_resources()

    prompt = f"""
You are an Azure FinOps expert.

User question:
{question}

Cost data:
{costs}

Resources:
{resources}

Give actionable cost optimization insights.
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are an expert Azure FinOps engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content