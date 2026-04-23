# Integration Guide: Using Azure Cost Optimizer in Another Repository

This guide shows how to integrate the Azure Cost Optimizer (FinOps Agent) into your own GitHub repository.

## Table of Contents
1. [Option 1: Clone as Submodule](#option-1-clone-as-submodule) - Recommended
2. [Option 2: Import as Python Package](#option-2-import-as-python-package)
3. [Option 3: Fork and Customize](#option-3-fork-and-customize)
4. [Option 4: Docker Integration](#option-4-docker-integration)
5. [Integration Examples](#integration-examples)

---

## **Option 1: Clone as Submodule** ⭐ Recommended

Use git submodule to add the optimizer to your existing project.

### Setup (5 minutes)

```bash
# Navigate to your repository
cd your-repo

# Add as submodule
git submodule add https://github.com/yuvrajgitwork/Cost-optimization-agent.git cost-optimizer
cd cost-optimizer

# Copy environment template
cp .env.example .env

# Edit with your credentials
# Fill in: TENANT_ID, CLIENT_ID, CLIENT_SECRET, SUBSCRIPTION_ID, GITHUB_PAT
nano .env

# Install dependencies
python -m pip install -r requirements.txt
```

### Use in Your Project

```python
# your_project/main.py
import sys
sys.path.insert(0, './cost-optimizer')

from cost_optimizer.agent import analyze_azure_costs
from cost_optimizer.optimization_agent import generate_optimizations

# Get recommendations
optimizations = generate_optimizations()

# Ask specific questions
insights = analyze_azure_costs("How can I reduce costs?")
```

### Update Submodule

```bash
# Update to latest version
git submodule update --remote

# Commit the update
git add cost-optimizer
git commit -m "Update cost optimizer to latest version"
```

---

## **Option 2: Import as Python Package**

Copy specific modules into your project.

### Setup (3 minutes)

```bash
# Create a directory in your project
mkdir -p your_project/finops

# Copy the modules you need
cp cost-optimization-agent/optimization_agent.py your_project/finops/
cp cost-optimization-agent/agent.py your_project/finops/
cp cost-optimization-agent/tools_costs.py your_project/finops/
cp cost-optimization-agent/tools_resources.py your_project/finops/
cp cost-optimization-agent/azure_auth.py your_project/finops/

# Copy dependencies
cp cost-optimization-agent/requirements.txt your_project/finops/

# Create __init__.py
touch your_project/finops/__init__.py
```

### Use in Your Project

```python
# your_project/cost_analysis.py
from your_project.finops.optimization_agent import generate_optimizations, get_optimization_summary
from your_project.finops.agent import analyze_azure_costs

async def run_optimization_analysis():
    # Generate recommendations
    optimizations = generate_optimizations("What's my biggest cost issue?")
    summary = get_optimization_summary(optimizations)
    
    return {
        "recommendations": optimizations,
        "summary": summary
    }
```

---

## **Option 3: Fork and Customize**

Create your own fork and customize for your organization.

### Setup (10 minutes)

```bash
# 1. Fork the repository on GitHub
#    Visit: https://github.com/yuvrajgitwork/Cost-optimization-agent
#    Click "Fork"

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/Cost-optimization-agent.git
cd Cost-optimization-agent

# 3. Add upstream to sync with original
git remote add upstream https://github.com/yuvrajgitwork/Cost-optimization-agent.git

# 4. Customize for your needs
# - Modify static/index.html styling
# - Update optimization rules in optimization_agent.py
# - Add custom Azure integrations

# 5. Deploy to your infrastructure
```

### Keep Synchronized

```bash
# Sync with original repo
git fetch upstream
git rebase upstream/main

# Push your changes
git push origin main
```

---

## **Option 4: Docker Integration**

Run the optimizer in a Docker container.

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/yuvrajgitwork/Cost-optimization-agent.git .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  cost-optimizer:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TENANT_ID=${TENANT_ID}
      - CLIENT_ID=${CLIENT_ID}
      - CLIENT_SECRET=${CLIENT_SECRET}
      - SUBSCRIPTION_ID=${SUBSCRIPTION_ID}
      - GITHUB_PAT=${GITHUB_PAT}
      - GITHUB_MODEL_ENDPOINT=https://models.inference.ai.azure.com/
      - GITHUB_MODEL=gpt-4o-mini
    volumes:
      - ./static:/app/static
    restart: unless-stopped
```

### Run with Docker

```bash
# Create .env file with your credentials
cp .env.example .env
# Edit .env with your values

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## **Integration Examples**

### Example 1: CI/CD Pipeline Integration

```yaml
# .github/workflows/cost-analysis.yml
name: Cost Analysis

on:
  schedule:
    - cron: '0 8 * * MON'  # Every Monday at 8 AM
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install -r cost-optimizer/requirements.txt

      - name: Run cost analysis
        env:
          TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          GITHUB_PAT: ${{ secrets.GITHUB_PAT }}
        run: |
          python scripts/run_optimization.py

      - name: Create GitHub issue with recommendations
        run: |
          python scripts/create_issue.py
```

### Example 2: FastAPI Microservice

```python
# your_service/api/cost_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys

# Add cost optimizer to path
sys.path.insert(0, '../cost-optimizer')
from optimization_agent import generate_optimizations

router = APIRouter(prefix="/api/costs", tags=["costs"])

@router.get("/optimizations")
async def get_optimizations(db: Session = Depends(get_db)):
    """Get Azure cost optimizations"""
    try:
        optimizations = generate_optimizations()
        return {
            "success": True,
            "recommendations": optimizations,
            "count": len(optimizations)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/ask")
async def ask_about_costs(question: str):
    """Ask AI questions about cost optimization"""
    from agent import analyze_azure_costs
    answer = analyze_azure_costs(question)
    return {"question": question, "answer": answer}
```

### Example 3: Scheduled Reports

```python
# scripts/generate_monthly_report.py
import json
import sys
from datetime import datetime
sys.path.insert(0, './cost-optimizer')

from optimization_agent import generate_optimizations, get_optimization_summary
from tools_costs import get_costs
from tools_resources import get_resources

def generate_report():
    """Generate monthly cost optimization report"""
    
    # Get data
    optimizations = generate_optimizations()
    summary = get_optimization_summary(optimizations)
    costs = get_costs()
    resources = get_resources()
    
    report = {
        "date": datetime.now().isoformat(),
        "summary": summary,
        "optimizations": optimizations,
        "total_resources": len(resources) if isinstance(resources, list) else 0,
        "cost_data": costs
    }
    
    # Save report
    filename = f"reports/cost_analysis_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report generated: {filename}")
    print(f"Potential savings: ${summary.get('total_savings_monthly', 0)}")
    print(f"Recommendations: {summary.get('total_recommendations', 0)}")

if __name__ == "__main__":
    generate_report()
```

---

## **Configuration for Your Repository**

### Required Secrets (GitHub / Environment)

```env
# Azure
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SUBSCRIPTION_ID=your_subscription_id

# GitHub Models
GITHUB_PAT=your_github_pat
GITHUB_MODEL_ENDPOINT=https://models.inference.ai.azure.com/
GITHUB_MODEL=gpt-4o-mini
```

### Directory Structure with Submodule

```
your-repo/
├── cost-optimizer/               # Submodule
│   ├── agent.py
│   ├── optimization_agent.py
│   ├── tools_costs.py
│   ├── tools_resources.py
│   ├── requirements.txt
│   └── static/
├── your_code/
│   ├── main.py
│   └── utils/
├── scripts/
│   ├── analyze_costs.py
│   └── generate_report.py
├── requirements.txt              # References cost-optimizer
└── .env                          # Credentials
```

---

## **Migration Checklist**

- [ ] Fork or clone the repository
- [ ] Create `.env` with your Azure credentials
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test locally: `uvicorn main:app --reload`
- [ ] Configure CI/CD pipeline if needed
- [ ] Set up GitHub secrets for production
- [ ] Deploy to your hosting platform
- [ ] Test all API endpoints
- [ ] Set up monitoring/alerts
- [ ] Document for your team

---

## **Support & Customization**

### Modify Optimization Rules

Edit `optimization_agent.py` to customize:

```python
OPTIMIZATION_CATEGORIES = {
    "YOUR_CUSTOM_RULE": {
        "name": "Your optimization",
        "description": "What it does"
    }
}
```

### Add Custom Azure Resources

Extend `tools_resources.py`:

```python
def get_custom_resources():
    # Query Azure for your custom resource types
    # Return recommendations specific to your setup
    pass
```

### Customize UI

Modify `static/index.html` to match your branding:

```html
<!-- Change colors, logos, layout -->
<div class="logo">🏢 Your Company Cost Optimizer</div>
```

---

## **FAQ**

**Q: Can I use this in production?**
A: Yes! Use environment variables, secrets management, and proper authentication.

**Q: How do I update when new versions are released?**
A: If using submodule: `git submodule update --remote`. Otherwise, manually pull changes.

**Q: Can I integrate with my billing system?**
A: Yes! Extend `tools_costs.py` to connect to your billing API.

**Q: What about multiple subscriptions?**
A: Change `SUBSCRIPTION_ID` in `.env` and redeploy, or create an API wrapper that manages multiple configs.

---

**🚀 Ready to integrate? Start with Option 1 (Submodule) for easiest setup!**

For questions: Open an issue on [GitHub](https://github.com/yuvrajgitwork/Cost-optimization-agent)
