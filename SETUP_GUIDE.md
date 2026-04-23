# Azure Cost Optimizer - Setup Guide

## Quick Start: Using with Any Azure Account

### Step 1: Create an Azure App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Enter a name (e.g., "AzureCostOptimizer")
5. Click **Register**

### Step 2: Get Your Credentials

From the App Registration overview page, copy:
- **Application (client) ID** → Set as `CLIENT_ID`
- **Directory (tenant) ID** → Set as `TENANT_ID`

Go to **Certificates & secrets**:
- Click **New client secret**
- Set expiry (e.g., 90 days)
- Copy the secret value → Set as `CLIENT_SECRET`

### Step 3: Grant Permissions

1. Go to your **Subscription**
2. Click **Access control (IAM)** > **Add role assignment**
3. Select Role: **Reader**
4. Assign to your App Registration
5. Click **Save**

### Step 4: Get Your Subscription ID

1. In Portal, search for "Subscriptions"
2. Click your subscription
3. Copy the **Subscription ID** → Set as `SUBSCRIPTION_ID`

### Step 5: Set up GitHub Models API

1. Go to [GitHub.com](https://github.com/settings/tokens)
2. Click **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**
3. Click **Generate new token (classic)**
4. Select scopes: `api`
5. Copy token → Set as `GITHUB_PAT`

### Step 6: Configure the Application

Create `.env` file in the project root:

```env
TENANT_ID=your_tenant_id
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SUBSCRIPTION_ID=your_subscription_id

GITHUB_PAT=github_pat_...
GITHUB_MODEL_ENDPOINT=https://models.inference.ai.azure.com/
GITHUB_MODEL=gpt-4o-mini
```

### Step 7: Run the Application

```bash
# Activate virtual environment
.\venv\Scripts\Activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Visit: `http://localhost:8000`

---

## Using with Multiple Azure Subscriptions

### Option 1: Sequential Switching (Recommended)

Simply update the `SUBSCRIPTION_ID` in `.env` and restart:

```env
SUBSCRIPTION_ID=subscription_id_1  # Change this
```

Then restart the application.

### Option 2: Store Multiple Configurations

Create separate `.env` files:

- `.env.prod` - Production subscription
- `.env.staging` - Staging subscription
- `.env.dev` - Development subscription

Then load the desired one:

```bash
# Copy the desired config
cp .env.prod .env
uvicorn main:app --reload
```

### Option 3: Different App Registrations per Subscriptions

If each subscription is in different Azure AD tenants:

1. Create separate app registrations in each tenant
2. Create separate `.env` files with different credentials
3. Switch `.env` file before running

---

## API Endpoints Available

### Cost Analysis
- `GET /api/costs` - Get current costs
- `GET /api/resources` - Get all resources
- `GET /api/insights?q=query` - Get cost insights

### Optimization Recommendations
- `GET /api/optimizations` - Get all optimization recommendations
- `GET /api/optimization-details?title=...&description=...` - Get details for specific optimization

### Interactive Chat
- `GET /ask?q=query` - Ask questions about your Azure costs

---

## Optimization Categories

The system analyzes Azure costs across these categories:

1. **💡 Idle Resource Detection** - Unused VMs, orphaned disks/IPs
2. **📊 Underutilized Resources** - Resources running below capacity
3. **💾 Storage Optimization** - Storage accounts, retention policies
4. **⚖️ Load Balancer Optimization** - LB and gateway configurations
5. **🚀 App Service Optimization** - App Service plans and instances
6. **🏗️ High Availability Assessment** - Availability zones and redundancy
7. **🔒 Security & Compliance** - Credentials, RBAC governance
8. **⚙️ Operational Excellence** - RBAC limits, resource groups

---

## Troubleshooting

### "Unauthorized" Errors
- Check that TENANT_ID, CLIENT_ID, CLIENT_SECRET are correct
- Verify the app registration has Reader role on the subscription
- Ensure SUBSCRIPTION_ID is valid

### "Invalid GitHub PAT"
- Regenerate the token in GitHub settings
- Ensure token has `api` scope selected
- Check token hasn't expired

### No Data Showing
- Wait 5-10 minutes after first deployment (data pulls from Azure)
- Check internet connection
- Verify subscription has active resources

### Model Issues
- Check GitHub Models API is accessible
- Try different model: `gpt-4o-mini` or `gpt-4o`
- Check GitHub PAT has correct scopes

---

## Security Notes

⚠️ **Never commit `.env` file to version control**

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

---

## Production Deployment

For production, use Azure Key Vault instead of .env:

1. Create an Azure Key Vault
2. Store secrets in Key Vault
3. Use Managed Identity to access Key Vault
4. Update code to load from Key Vault

---
