from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os
from tools_costs import get_costs
from tools_resources import get_resources

client = OpenAI(
    api_key=os.getenv("GITHUB_PAT"),
    base_url=os.getenv("GITHUB_MODEL_ENDPOINT")
)

MODEL = os.getenv("GITHUB_MODEL", "gpt-4o-mini")

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
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert Azure FinOps engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content