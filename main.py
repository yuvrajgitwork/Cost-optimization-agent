from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from agent import analyze_azure_costs
from tools_costs import get_costs
from tools_resources import get_resources
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Azure Cost Optimizer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/ask")
def ask(q: str):
    return {"answer": analyze_azure_costs(q)}

@app.get("/api/costs")
def api_costs():
    try:
        costs_data = get_costs()
        import json
        # Parse if it's a string, otherwise return as-is
        if isinstance(costs_data, str):
            return json.loads(costs_data)
        return costs_data
    except Exception as e:
        return {"error": str(e), "properties": {"rows": []}}

@app.get("/api/resources")
def api_resources():
    try:
        resources_data = get_resources()
        import json
        # Parse if it's a string, otherwise return as-is
        if isinstance(resources_data, str):
            return json.loads(resources_data)
        return resources_data
    except Exception as e:
        return {"error": str(e), "data": []}

@app.get("/api/insights")
def api_insights(q: str = "What are my top cost optimization opportunities?"):
    try:
        insights = analyze_azure_costs(q)
        return {"insights": insights}
    except Exception as e:
        return {"error": str(e), "insights": "Unable to generate insights at this time."}