# Azure Cost Optimizer - FinOps Intelligence Agent 🚀

A comprehensive, AI-powered Azure cost optimization platform powered by GitHub Models and Microsoft's FinOps toolkit. Analyze Azure costs, identify savings opportunities, and generate actionable recommendations automatically.

**Live Demo:** Access at `http://localhost:8000` when running locally

---

## ✨ Features

### 🤖 AI-Powered Analysis
- **GitHub Models Integration** - Uses free/paid GitHub inference models (no Azure OpenAI costs)
- **FinOps Alignment** - Based on Microsoft's Azure Optimization Engine framework
- **Intelligent Recommendations** - ML-powered cost optimization suggestions
- **Multi-Account Support** - Works with any Azure subscription

### 📊 Comprehensive Dashboard
- **Real-time Cost Tracking** - Monitor Azure spending in real-time
- **Interactive Charts** - Visualize cost trends and resource distribution
- **Resource Inventory** - Complete view of all Azure resources
- **Optimization Score** - Overall cost optimization health

### 🔧 FinOps Optimization Engine
Analyzes across 8 categories:
- 💡 **Idle Resource Detection** - Find unused/idle resources
- 📊 **Underutilized Resources** - Downsize over-provisioned resources
- 💾 **Storage Optimization** - Optimize storage configurations
- ⚖️ **Load Balancer Optimization** - Clean up LB/gateway configs
- 🚀 **App Service Optimization** - Streamline App Services
- 🏗️ **High Availability** - Verify HA/DR posture
- 🔒 **Security & Compliance** - Check security misconfigs
- ⚙️ **Operational Excellence** - Improve resource management

### 💰 Expandable Recommendation Cards
- **Priority Levels** - CRITICAL → LOW
- **Estimated Savings** - Monthly cost impact
- **Implementation Steps** - 3-5 actionable steps
- **Affected Resources** - Which resources are impacted
- **One-Click Details** - View full recommendations instantly

### 🔌 RESTful API
```
GET /               - Dashboard UI
GET /api/costs      - Cost data
GET /api/resources  - Resource inventory
GET /api/insights   - AI insights
GET /api/optimizations           - All recommendations
GET /api/optimization-details    - Specific recommendation details
GET /ask?q=query    - Ask questions about costs
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Azure subscription with app registration
- GitHub account with PAT token (for models)

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yuvrajgitwork/Cost-optimization-agent.git
cd Cost-optimization-agent

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edit .env with your Azure and GitHub credentials
```

### Configuration

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions.**

Quick config:
```env
# Azure
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SUBSCRIPTION_ID=your_subscription_id

# GitHub Models API
GITHUB_PAT=github_pat_...
GITHUB_MODEL_ENDPOINT=https://models.inference.ai.azure.com/
GITHUB_MODEL=gpt-4o-mini
```

### Run

```bash
# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open browser
# Visit: http://localhost:8000
```

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup for any Azure account
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - How to use in other projects
- **[README_OPTIMIZATION.md](README_OPTIMIZATION.md)** - Feature overview

---

## 🔗 Integration

Use this in your own repository:

### Option 1: Git Submodule (Recommended)
```bash
git submodule add https://github.com/yuvrajgitwork/Cost-optimization-agent.git cost-optimizer
```

### Option 2: Python Package
Copy modules to your project and use as internal library

### Option 3: Docker
```bash
docker-compose up -d
```

### Option 4: Fork & Customize
Create your own fork and customize for your organization

**See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed integration examples.**

---

## 🏗️ Architecture

```
FastAPI Backend
├── agent.py                 # Claude integration for cost analysis
├── optimization_agent.py    # FinOps engine & recommendations
├── tools_costs.py          # Azure Cost Management API
├── tools_resources.py      # Azure Resource Graph queries
└── azure_auth.py           # Azure authentication

Frontend Dashboard
├── static/index.html       # Interactive UI
├── Expandable cards        # Detailed recommendations
├── Charts & graphs         # Cost visualizations
└── Resource inventory      # Complete resource listing
```

---

## 📊 What You Get

### Dashboard Shows:
- 💰 Total monthly costs
- 💾 Estimated monthly savings
- 📦 Total active resources
- 📈 Optimization score
- 📊 Cost trends (30 days)
- 🎯 AI recommendations
- 📋 Expandable optimization cards

### Each Recommendation Includes:
- Priority level (CRITICAL/HIGH/MEDIUM/LOW)
- Estimated monthly savings
- Implementation effort (LOW/MEDIUM/HIGH)
- Step-by-step implementation guide
- List of affected resources
- Cost-benefit analysis

---

## 🔐 Security

✅ **Best Practices Included:**
- Environment variables for secrets (never in code)
- `.gitignore` excludes sensitive files
- No hardcoded credentials
- GitHub secret scanning compatible
- RBAC minimal permissions (Reader role only)
- Audit logging ready

⚠️ **Production Checklist:**
- [ ] Use Azure Key Vault for secrets
- [ ] Deploy with Managed Identity
- [ ] Set up VPC/network isolation
- [ ] Enable audit logging
- [ ] Use HTTPS/TLS
- [ ] Rate limiting on APIs
- [ ] Monitor failed authentications

---

## 💡 Use Cases

- **FinOps Teams** - Centralized cost optimization platform
- **DevOps** - Automated cost monitoring in CI/CD
- **Cost Management** - Dashboard for executives/finance
- **Cloud Migration** - Identify over-provisioned resources
- **Multi-Account Setup** - Manage costs across subscriptions
- **Budget Planning** - Forecast savings opportunities

---

## 🛠️ Customization

### Add Custom Optimization Rules
Edit `optimization_agent.py`:
```python
OPTIMIZATION_CATEGORIES = {
    "YOUR_CATEGORY": {
        "name": "Your optimization",
        "description": "What it does"
    }
}
```

### Modify Azure Resource Queries
Edit `tools_resources.py` to add custom resource types

### Customize Dashboard
Edit `static/index.html` for your branding

---

## 📝 API Examples

### Get All Optimizations
```bash
curl http://localhost:8000/api/optimizations
```

### Ask About Costs
```bash
curl "http://localhost:8000/ask?q=What%20are%20my%20biggest%20cost%20drivers?"
```

### Get Cost Data
```bash
curl http://localhost:8000/api/costs
```

---

## 🤝 Contributing

Contributions welcome! Areas for contribution:
- Additional optimization rules
- UI enhancements
- Integration examples
- Documentation improvements
- Azure resource type extensions

---

## 📄 License

[Add your license here]

---

## 🆘 Support

**Questions?**
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for configuration help
2. Review [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for integration issues
3. Open an issue on [GitHub](https://github.com/yuvrajgitwork/Cost-optimization-agent)

**Problems?**
- Verify Azure credentials are correct
- Check GitHub PAT has right scopes
- Ensure app registration has Reader role

---

## 🚀 What's Next?

- Deploy to Azure Container Instances
- Set up CI/CD for automated cost analysis
- Integrate with Slack for alerts
- Create Power BI dashboards
- Add remediation automation
- Multi-account federation

---

**Start optimizing your Azure costs today! 💰⬇️**

[Get Started with SETUP_GUIDE.md](SETUP_GUIDE.md) | [Integrate into Your Project](INTEGRATION_GUIDE.md)
