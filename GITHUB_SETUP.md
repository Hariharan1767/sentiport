# GitHub Setup Guide for SentiPort

## 🎯 Quick Start

You need to set up Git first, then connect to GitHub. Follow these steps:

---

## Step 1: Install Git

### Option A: Direct Download (Easiest)
1. Go to https://git-scm.com/download/win
2. Download the Windows installer
3. Run the installer
4. Accept all default settings
5. Click "Install"
6. Restart your computer

### Option B: Using Windows Package Manager
```powershell
winget install Git.Git
```

### Option C: Using Chocolatey
```powershell
choco install git
```

---

## Step 2: Verify Installation

After installing, open a new PowerShell and run:
```powershell
git --version
```

You should see something like: `git version 2.43.0.windows.1`

---

## Step 3: Create GitHub Account

1. Go to https://github.com
2. Click "Sign up"
3. Create your account
4. Verify your email
5. Done!

---

## Step 4: Connect Your Project to GitHub

After installing Git and creating GitHub account:

```powershell
# Navigate to project
cd C:\Users\HARIHARAN\Projects\SentiPort

# Initialize Git repository
git init

# Configure Git (use YOUR actual info)
git config user.name "Your Name"
git config user.email "your.email@gmail.com"

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete SentiPort project setup"

# Check if remote exists
git remote -v
```

---

## Step 5: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `SentiPort`
3. Description: "Sentiment-driven portfolio optimization web application"
4. Select "Private" (or Public)
5. Do NOT check "Initialize with README" (we have one)
6. Click "Create repository"

---

## Step 6: Push to GitHub

After creating the repository on GitHub, you'll see instructions. Copy the HTTPS URL and run:

```powershell
# Add GitHub as remote (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/SentiPort.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

If asked for credentials:
- Username: Your GitHub username
- Password: Use a Personal Access Token (not your password)

---

## Generate Personal Access Token

1. Go to GitHub Settings: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "SentiPort Development"
4. Check these scopes:
   - `repo` (full control of private repositories)
   - `workflow` (if you want CI/CD)
5. Click "Generate token"
6. **Copy the token and save it somewhere safe**

When Git asks for password, paste your token instead.

---

## Step 7: Daily Workflow

### Start Each Day

```powershell
# Navigate to project
cd C:\Users\HARIHARAN\Projects\SentiPort

# Pull latest changes (if working on multiple machines)
git pull origin main

# Start development
npm install    # Only if dependencies changed
npm run dev
```

### End of Day

```powershell
# Check what changed
git status

# Stage all changes
git add .

# Commit with message
git commit -m "feat: Add real-time data updates"

# Push to GitHub
git push origin main
```

---

## Useful Git Commands

```powershell
# See commit history
git log --oneline

# See changes in current files
git status

# See detailed changes in a file
git diff src/components/Dashboard.jsx

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create a new branch for features
git checkout -b feature/amazing-feature

# Switch between branches
git checkout main
git checkout feature/amazing-feature

# Merge feature into main
git checkout main
git merge feature/amazing-feature
```

---

## Using GitHub on VS Code

VS Code has built-in Git support! Here's how:

1. Open VS Code
2. Open your SentiPort folder
3. Click "Source Control" icon (left sidebar)
4. You'll see a list of changed files
5. Click the "+" icon to stage files
6. Type commit message in the box at top
7. Click the checkmark to commit
8. Click "..." menu → "Push" to push to GitHub

---

## If You Get Stuck

### Clone on Different Machine

After first setup on GitHub, you can clone on any other machine:

```powershell
# Navigate to where you want the project
cd C:\Users\YourName\Projects

# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/SentiPort.git

# Navigate into project
cd SentiPort

# Install dependencies
npm install

# Start development
npm run dev
```

### Troubleshooting

**"fatal: not a git repository"**
- Make sure you're in the SentiPort directory
- Run `git init` to initialize

**"Permission denied"**
- Check your Personal Access Token is correct
- Make sure you're using token, not password

**"Everything up-to-date"**
- This is good! It means no changes to push

---

## 🎉 You're Ready!

Once Git is installed and your GitHub repository is set up, follow the Daily Workflow in `DAILY_WORKFLOW.md`

Questions? Check out:
- Git docs: https://git-scm.com/doc
- GitHub Help: https://docs.github.com
- Atlassian Git Tutorial: https://www.atlassian.com/git/tutorials
