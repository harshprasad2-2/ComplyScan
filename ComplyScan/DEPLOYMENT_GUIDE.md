# ComplyScan GitHub Deployment Guide

## Quick Start: Deploy to GitHub

### Step 1: Install Git (if not already installed)

**Windows:**
```powershell
# Download from https://git-scm.com/download/win
# Or install via chocolatey:
choco install git
```

**Mac/Linux:**
```bash
sudo apt-get install git  # Ubuntu/Debian
brew install git          # Mac
```

### Step 2: Navigate to Project & Initialize Git

```powershell
cd f:\Dev\SIH\ComplyScan

# Initialize repository
git init

# Configure git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 3: Add Files & Commit

```powershell
# Add all files (respects .gitignore)
git add .

# Commit
git commit -m "Initial commit: ComplyScan v1.0.0 - Legal Metrology compliance screening"

# Check status
git status
```

### Step 4: Create GitHub Repository

**Option A: Create via GitHub Web UI (Recommended)**

1. Go to **https://github.com/new**
2. Create new repository:
   - Repository name: `ComplyScan` (or `legal-metrology-scanner`)
   - Description: `AI-assisted Legal Metrology compliance screening system`
   - Visibility: **Public** (for hackathon judges to access)
   - DO NOT initialize with README/license (you already have them)
3. Click **Create Repository**
4. Copy the repository URL (HTTPS or SSH)

**Option B: Use GitHub CLI**

```powershell
# Install GitHub CLI: https://cli.github.com/
gh auth login
gh repo create ComplyScan --public --source=. --remote=origin --push
```

### Step 5: Push to GitHub

```powershell
# Add remote (replace URL with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/ComplyScan.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify on GitHub

1. Visit: `https://github.com/YOUR_USERNAME/ComplyScan`
2. Confirm all files are uploaded ✅
3. Share the link with judges/team

---

## On Another Laptop: Clone & Run

Once deployed to GitHub, anyone can use it:

```powershell
# Clone repository
git clone https://github.com/YOUR_USERNAME/ComplyScan.git
cd ComplyScan

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Generate demo images
python -m modules.demo_data

# Run the app
python -m streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## GitHub Repository Structure

```
ComplyScan/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── RUN_DEMO.md            # Demo guide
├── BUILD_COMPLETE.md      # Build status
├── run.bat                # Windows launcher
├── .gitignore             # Git ignore patterns
│
├── modules/               # Core Python modules
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── image_processing.py
│   ├── ocr_engine.py
│   ├── extraction.py
│   ├── rules_engine.py
│   ├── report_generator.py
│   ├── demo_data.py
│   ├── utils.py
│   └── analytics.py
│
├── tests/                 # Unit tests
│   ├── test_extraction.py
│   └── test_rules.py
│
├── assets/
│   └── demo_images/       # Auto-generated demo images
│
└── docs/                  # (Optional) Additional documentation
```

---

## Tips for Judges

1. **Add this to README** (judges see this first):

```markdown
## 🚀 Quick Start

### Option 1: Online Demo (Fastest)
Download the repo → Run `python -m streamlit run app.py` → Open http://localhost:8501

### Option 2: Full Setup
```bash
git clone https://github.com/YOUR_USERNAME/ComplyScan.git
cd ComplyScan
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python -m modules.demo_data  # Generate demo images
python -m streamlit run app.py
```

### Option 3: Docker (if you add Dockerfile)
```bash
docker build -t complyscan .
docker run -p 8501:8501 complyscan
```
```

2. **Add GitHub Actions** (optional - auto-tests on push):

Create `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

---

## Common Issues

**Issue: "fatal: not a git repository"**
→ Run `git init` first

**Issue: "fatal: 'origin' does not appear to be a 'git' repository"**
→ Run `git remote add origin <URL>` with your repo URL

**Issue: "ERROR: permission denied"**
→ Use HTTPS instead of SSH, or set up SSH keys: `ssh-keygen -t ed25519`

**Issue: Large files (database, images)**
→ Already handled by `.gitignore` (excludes `*.db`, `uploads/`, `reports/`)

---

## Upload to Different Account

If you want to use a **different GitHub account**:

1. Create new GitHub account or use existing one
2. Generate Personal Access Token:
   - Settings → Developer Settings → Personal access tokens → Generate new token
   - Scopes: `repo`, `user`
3. Store token securely
4. In PowerShell, use token as password when `git push` asks

Or use GitHub Desktop app for easier management.

---

## Share with Team

Once on GitHub, share the URL:

```
🎯 ComplyScan Repository:
https://github.com/YOUR_USERNAME/ComplyScan

📋 Instructions:
1. Clone: git clone <URL>
2. Install: pip install -r requirements.txt
3. Run: python -m streamlit run app.py
4. Open: http://localhost:8501
```

---

## Next Steps

After deploying:
1. ✅ Add GitHub link to your hackathon submission
2. ✅ Add screenshots to README (judges like visuals)
3. ✅ Document any setup requirements
4. ✅ Share with judges 2-3 days before presentation

---

**Questions?** Check GitHub docs: https://docs.github.com/
