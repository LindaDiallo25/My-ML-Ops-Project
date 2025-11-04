# GitHub Actions CI/CD Setup Guide

## 🚀 Overview

This project uses GitHub Actions with a self-hosted runner for continuous integration and deployment. The CI/CD pipeline includes automated testing, Docker image building, and optional deployment.

---

## 📋 Prerequisites

- GitHub repository: https://github.com/Andy-P626/ML-Ops-project
- Self-hosted runner machine (macOS/Linux/Windows)
- Docker installed on runner machine
- Git LFS installed
- Python 3.11+ and Node.js 18+

---

## 🔧 Setting Up Self-Hosted Runner

### Step 1: Navigate to Repository Settings

1. Go to: https://github.com/Andy-P626/ML-Ops-project/settings/actions/runners
2. Click "New self-hosted runner"

### Step 2: Install Runner on Your Machine

**For macOS/Linux:**

```bash
# Create a folder for the runner
mkdir actions-runner && cd actions-runner

# Download the latest runner package
curl -o actions-runner-osx-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-osx-x64-2.311.0.tar.gz

# Extract the installer
tar xzf ./actions-runner-osx-x64-2.311.0.tar.gz

# Configure the runner
./config.sh --url https://github.com/Andy-P626/ML-Ops-project --token YOUR_TOKEN

# Run the runner
./run.sh
```

**For Windows (PowerShell):**

```powershell
# Create a folder for the runner
mkdir actions-runner; cd actions-runner

# Download the latest runner package
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip

# Extract the installer
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.311.0.zip", "$PWD")

# Configure the runner
./config.cmd --url https://github.com/Andy-P626/ML-Ops-project --token YOUR_TOKEN

# Run the runner
./run.cmd
```

### Step 3: Install Runner as a Service (Optional)

**macOS/Linux:**
```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

**Windows (Admin PowerShell):**
```powershell
./svc.cmd install
./svc.cmd start
```

---

## 🔐 Configure GitHub Secrets

Go to: https://github.com/Andy-P626/ML-Ops-project/settings/secrets/actions

Add the following secrets:

### Required Secrets:

1. **DOCKER_USERNAME** (optional)
   - Your Docker Hub username
   - Example: `yourname`

2. **DOCKER_PASSWORD** (optional)
   - Your Docker Hub password or access token
   - Get token at: https://hub.docker.com/settings/security

### How to Add Secrets:

1. Click "New repository secret"
2. Enter name (e.g., `DOCKER_USERNAME`)
3. Enter value
4. Click "Add secret"

---

## 📝 Workflow Files

### 1. Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branch
- Pull requests to `main`
- Manual dispatch

**Jobs:**
1. **test-api**: Lint and test Python API code
2. **test-frontend**: Build and test React frontend
3. **build-docker**: Build Docker images
4. **deploy**: Deploy to self-hosted environment
5. **validate-model**: Validate ML model integrity

### 2. Model Training Pipeline (`.github/workflows/model-training.yml`)

**Trigger:** Manual dispatch only

**Features:**
- Configurable epochs and batch size
- MLflow experiment tracking
- Artifact upload (model + training history)
- Performance summary in GitHub UI

---

## 🎯 How to Use

### Automatic Deployment

1. **Push to main branch:**
   ```bash
   git add .
   git commit -m "Update code"
   git push origin main
   ```

2. **The pipeline will automatically:**
   - Run tests
   - Build Docker images
   - Deploy to self-hosted runner
   - Validate deployment

### Manual Model Training

1. Go to: https://github.com/Andy-P626/ML-Ops-project/actions
2. Select "Model Training Pipeline"
3. Click "Run workflow"
4. Configure parameters:
   - Epochs (default: 15)
   - Batch size (default: 32)
5. Click "Run workflow"

### View Results

- **Actions tab**: https://github.com/Andy-P626/ML-Ops-project/actions
- **Build logs**: Click on any workflow run
- **Artifacts**: Download from completed runs

---

## 🔍 Pipeline Status

Check pipeline status with badges in README.md:

```markdown
![CI/CD](https://github.com/Andy-P626/ML-Ops-project/actions/workflows/ci-cd.yml/badge.svg)
![Model Training](https://github.com/Andy-P626/ML-Ops-project/actions/workflows/model-training.yml/badge.svg)
```

---

## 📊 What Gets Tested

### API Tests:
- ✅ Python syntax (flake8)
- ✅ Model file exists and valid
- ✅ FastAPI app imports
- ✅ Health endpoint responds
- ✅ Model-info endpoint responds

### Frontend Tests:
- ✅ Dependencies install
- ✅ Build succeeds
- ✅ Output files generated

### Docker Tests:
- ✅ API image builds
- ✅ Frontend image builds
- ✅ Docker Compose config valid

### Model Tests:
- ✅ File size validation (not Git LFS pointer)
- ✅ Model loads successfully
- ✅ Correct input/output shapes
- ✅ Parameter count matches

---

## 🐛 Troubleshooting

### Issue: Runner not connecting

**Solution:**
```bash
# Check runner status
./run.sh

# Reconfigure if needed
./config.sh remove
./config.sh --url https://github.com/Andy-P626/ML-Ops-project --token NEW_TOKEN
```

### Issue: Docker commands fail

**Solution:**
```bash
# Ensure Docker is running
docker --version

# Add runner user to docker group (Linux)
sudo usermod -aG docker $USER
```

### Issue: Git LFS files not downloading

**Solution:**
```bash
# Install Git LFS
git lfs install

# Pull LFS files
git lfs pull
```

### Issue: Python dependencies fail

**Solution:**
```bash
# Install system dependencies (macOS)
brew install python@3.11

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Workflow Customization

### Modify Test Commands

Edit `.github/workflows/ci-cd.yml`:

```yaml
- name: Run custom tests
  run: |
    pytest tests/ --cov=api --cov-report=html
```

### Add Deployment Steps

```yaml
- name: Deploy to production
  run: |
    docker-compose -f docker-compose.prod.yml up -d
```

### Add Notifications

```yaml
- name: Notify on Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📈 Best Practices

1. **Keep runner updated**
   ```bash
   cd actions-runner
   ./config.sh remove
   # Download latest version
   ./config.sh --url ... --token ...
   ```

2. **Monitor runner health**
   - Check GitHub Actions settings regularly
   - Review failed workflow runs
   - Keep runner machine resources available

3. **Secure secrets**
   - Never commit secrets to repository
   - Rotate tokens periodically
   - Use repository secrets, not personal tokens

4. **Git LFS for large files**
   - Keep model files in Git LFS
   - Don't commit large files directly
   - Use `.gitattributes` to track patterns

---

## 🎓 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Self-hosted Runners Guide](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Docker Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [Git LFS](https://git-lfs.github.com/)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Self-hosted runner shows "Idle" status in GitHub
- [ ] Git LFS is installed and configured
- [ ] Docker is running on runner machine
- [ ] Python 3.11+ is available
- [ ] Node.js 18+ is available
- [ ] Secrets are configured (if using Docker Hub)
- [ ] First workflow run completes successfully

---

## 🚀 Quick Start Commands

```bash
# 1. Set up runner (one-time)
mkdir actions-runner && cd actions-runner
# Follow download and config steps from GitHub UI

# 2. Start runner
./run.sh

# 3. Push code to trigger pipeline
git add .
git commit -m "Trigger CI/CD"
git push origin main

# 4. Monitor at:
# https://github.com/Andy-P626/ML-Ops-project/actions
```

---

**Last Updated**: November 1, 2025  
**GitHub Repository**: https://github.com/Andy-P626/ML-Ops-project
