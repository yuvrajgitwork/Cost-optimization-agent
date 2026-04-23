from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os
import json
from tools_costs import get_costs
from tools_resources import get_resources

client = OpenAI(
    api_key=os.getenv("GITHUB_PAT"),
    base_url=os.getenv("GITHUB_MODEL_ENDPOINT")
)

MODEL = os.getenv("GITHUB_MODEL", "gpt-4o-mini")

# FinOps Optimization Categories from Microsoft's Toolkit
OPTIMIZATION_CATEGORIES = {
    "IDLE_RESOURCES": {
        "name": "💡 Idle Resource Detection",
        "description": "Find unused or idle resources that can be shut down, deallocated, or resized",
        "examples": ["Idle VM instances", "Deallocated VMs (stopped but not deallocated)", "Orphaned disks", "Orphaned public IPs"]
    },
    "UNDERUTILIZED": {
        "name": "📊 Underutilized Resources",
        "description": "Identify resources running below capacity that can be optimized",
        "examples": ["Underutilized VM Scale Sets", "Premium SSD disks with low usage", "App Service plans with excess capacity", "SQL databases with low DTU usage"]
    },
    "STORAGE_OPTIMIZATION": {
        "name": "💾 Storage Optimization",
        "description": "Optimize storage configurations and remove unnecessary storage resources",
        "examples": ["Storage accounts without retention policy", "Unmanaged disks", "Redundancy analysis"]
    },
    "LOAD_BALANCING": {
        "name": "⚖️ Load Balancer Optimization",
        "description": "Optimize load balancer and gateway configurations",
        "examples": ["Load balancers without backend pool", "Application gateways without backend", "Basic vs Standard LB analysis"]
    },
    "APP_SERVICE": {
        "name": "🚀 App Service Optimization",
        "description": "Optimize App Service plans and deployments",
        "examples": ["App Service plans without applications", "Unused App Service instances", "Plan downsizing recommendations"]
    },
    "HIGH_AVAILABILITY": {
        "name": "🏗️ High Availability Assessment",
        "description": "Verify high availability and disaster recovery posture",
        "examples": ["VM availability zones", "Managed disk usage", "Redundancy across regions"]
    },
    "SECURITY": {
        "name": "🔒 Security & Compliance",
        "description": "Identify security misconfigurations and compliance gaps",
        "examples": ["Expired service principal credentials", "NSG rules with orphaned resources", "RBAC governance issues"]
    },
    "OPERATIONAL": {
        "name": "⚙️ Operational Excellence",
        "description": "Improve operational readiness and resource management",
        "examples": ["RBAC assignment limits", "Resource group limits", "Empty subnets", "Orphaned NICs"]
    }
}

def generate_optimizations(question: str = None):
    """Generate detailed optimization recommendations based on FinOps toolkit"""
    
    costs = get_costs()
    resources = get_resources()
    
    # If specific question is asked, analyze it
    if question:
        analysis_prompt = f"""
You are an Azure FinOps expert using the Microsoft Azure Optimization Engine framework.

User question: {question}

Based on cost and resource data provided, give specific, actionable optimization recommendations with:
1. Category (from: IDLE_RESOURCES, UNDERUTILIZED, STORAGE_OPTIMIZATION, LOAD_BALANCING, APP_SERVICE, HIGH_AVAILABILITY, SECURITY, OPERATIONAL)
2. Issue Title
3. Current Impact (what's happening now)
4. Recommendation (specific action to take)
5. Estimated Savings (monthly in dollars)
6. Priority (CRITICAL, HIGH, MEDIUM, LOW)
7. Effort Level (LOW, MEDIUM, HIGH)
8. Implementation Steps (3-5 specific steps)

Format as JSON array of optimization objects.
"""
    else:
        # Generic comprehensive analysis
        analysis_prompt = f"""
You are an Azure FinOps expert using the Microsoft Azure Optimization Engine (AOE) framework.
Analyze this Azure environment for cost optimization opportunities.

Cost Data:
{costs}

Resource Data:
{resources}

Generate optimization recommendations across these categories:
- IDLE_RESOURCES: Unused VMs, deallocated VMs, orphaned disks/IPs
- UNDERUTILIZED: VMs, Scale Sets, App Service plans, SQL databases with low usage
- STORAGE_OPTIMIZATION: Storage accounts, retention policies, unmanaged disks
- LOAD_BALANCING: Load balancers and gateways without backends
- APP_SERVICE: Unused App Service plans and instances
- HIGH_AVAILABILITY: Availability zones, managed disks, redundancy
- SECURITY: Expired credentials, NSG issues, RBAC governance
- OPERATIONAL: RBAC limits, resource groups, empty subnets, orphaned NICs

For EACH potential optimization, provide:
1. category: (one of the above)
2. title: Brief title
3. description: What was found
4. impact: Current negative impact
5. recommendation: What to do about it
6. savings: Monthly savings in dollars (estimate)
7. priority: CRITICAL/HIGH/MEDIUM/LOW
8. effort: LOW/MEDIUM/HIGH
9. steps: [list of implementation steps]
10. affectedResources: [list of affected resource names/IDs]

Return as valid JSON array. Generate 5-8 recommendations based on the data provided.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert Azure FinOps engineer. Return only valid JSON in your response."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.3
    )
    
    response_text = response.choices[0].message.content
    
    # Parse JSON from response
    try:
        # Try to extract JSON from the response
        import re
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            optimizations = json.loads(json_match.group())
        else:
            optimizations = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback: create a structured response
        optimizations = [{
            "category": "IDLE_RESOURCES",
            "title": "Manual Review Recommended",
            "description": response_text[:200],
            "impact": "Unable to parse AI response",
            "recommendation": "Please review the cost and resource data manually",
            "savings": 0,
            "priority": "MEDIUM",
            "effort": "MEDIUM",
            "steps": ["Contact support", "Review raw data"],
            "affectedResources": []
        }]
    
    return optimizations

def get_optimization_summary(optimizations: list = []) -> dict:
    """Generate summary metrics from optimizations"""
    if not optimizations:
        optimizations = generate_optimizations()
    
    total_savings = sum(opt.get("savings", 0) for opt in optimizations)
    critical_count = sum(1 for opt in optimizations if opt.get("priority") == "CRITICAL")
    high_count = sum(1 for opt in optimizations if opt.get("priority") == "HIGH")
    
    return {
        "total_savings_monthly": total_savings,
        "critical_issues": critical_count,
        "high_priority_issues": high_count,
        "total_recommendations": len(optimizations),
        "categories": list(set(opt.get("category", "UNKNOWN") for opt in optimizations))
    }

def explain_optimization(title: str, description: str) -> str:
    """Get detailed explanation for a specific optimization"""
    query = f"""
You are an Azure FinOps expert. Provide a detailed explanation for this optimization recommendation:

Title: {title}
Description: {description}

Explain:
1. Why this matters for cost optimization
2. What risks exist if not addressed
3. Step-by-step implementation guide
4. Expected outcomes and benefits
5. Common pitfalls to avoid
6. Best practices

Be specific and actionable.
"""
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert Azure FinOps engineer."},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content
