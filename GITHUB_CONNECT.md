# 🚀 Connect SentiPort to GitHub

Your local Git repository is ready! Now connect it to GitHub.

---

## ✅ What's Done Locally

- [x] Git initialized
- [x] 42 files committed
- [x] Initial commit created: `3e69b11`
- [x] User configured (Hariharan / hariharan@sentiport.dev)

---

## 📋 Next: Connect to GitHub (5 Steps)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `SentiPort`
3. **Description**: "Sentiment-driven portfolio optimization web application"
4. **Privacy**: Select "Public" or "Private"
5. **Do NOT** check "Initialize with README"
6. Click **Create repository**

### Step 2: Copy the HTTPS URL

After creating the repository, GitHub shows:
```
https://github.com/YOUR_USERNAME/SentiPort.git
```

Copy this URL. You'll need it in the next step.

---

### Step 3: Add Remote to Local Repository

Open PowerShell in SentiPort folder and run:

```powershell
$env:PATH += ";C:\Program Files\Git\bin"

# Replace with YOUR URL from Step 2
& "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/YOUR_USERNAME/SentiPort.git
```

### Step 4: Rename Branch to 'main' (if needed)

```powershell
$env:PATH += ";C:\Program Files\Git\bin"
& "C:\Program Files\Git\bin\git.exe" branch -M main
```

### Step 5: Push to GitHub

```powershell
$env:PATH += ";C:\Program Files\Git\bin"
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

When prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (NOT your GitHub password)

---

## 🔑 Generate Personal Access Token (If Needed)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. **Token name**: `SentiPort-Dev`
4. **Expiration**: 90 days (or your preference)
5. **Select scopes**:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (if you want GitHub Actions)
6. Click **Generate token**
7. **Copy the token** and save it somewhere safe

**When Git asks for password, paste this token instead of your password.**

---

## ✨ After Pushing to GitHub

You can now:

### Clone on Another Machine
```powershell
$env:PATH += ";C:\Program Files\Git\bin"
& "C:\Program Files\Git\bin\git.exe" clone https://github.com/YOUR_USERNAME/SentiPort.git
cd SentiPort
npm install
npm run dev
```

### Daily Workflow
```powershell
# Start day
cd C:\Users\HARIHARAN\Projects\SentiPort
& "C:\Program Files\Git\bin\git.exe" pull origin main
npm run dev

# End of day
& "C:\Program Files\Git\bin\git.exe" add .
& "C:\Program Files\Git\bin\git.exe" commit -m "feat: Your description here"
& "C:\Program Files\Git\bin\git.exe" push origin main
```

---

## 🛠️ Simplify Git Commands

To use `git` command directly instead of the full path, add this to your PowerShell profile:

1. Open PowerShell
2. Run: `notepad $PROFILE`
3. Add these lines:
```powershell
$env:PATH += ";C:\Program Files\Git\bin"
$env:PATH += ";C:\Program Files\Git\cmd"
Set-Alias git "C:\Program Files\Git\bin\git.exe"
```
4. Save and close
5. Restart PowerShell
6. Now you can use: `git status`, `git push`, etc.

---

## ✅ Commands Cheat Sheet

```powershell
# Setup
git init                          # Initialize (already done)
git config user.name "Name"       # Configure (already done)
git config user.email "email"     # Configure (already done)

# Daily Use
git status                        # See changes
git add .                         # Stage all changes
git commit -m "message"           # Create commit
git push origin main              # Push to GitHub
git pull origin main              # Pull from GitHub

# Viewing
git log --oneline                 # See commit history
git diff                          # See file changes
git show 3e69b11                  # See specific commit

# Branches
git branch                        # List branches
git checkout -b feature/name      # Create feature branch
git checkout main                 # Switch to main
git merge feature/name            # Merge feature to main
```

---

## ❓ Troubleshooting

### "fatal: not a git repository"
- Make sure you're in the SentiPort folder
- Run `git init` (should already be done)

### "Permission denied" or "Authentication failed"
- Check your Personal Access Token is correct
- Make sure you're using token, not your GitHub password
- Token must have `repo` scope

### "fatal: The current branch master has no upstream"
- Run: `git branch -M main`
- Then: `git push -u origin main`

### "Everything up-to-date"
- This is good! No new changes to push
- Make edits, then commit and push again

---

## 📚 Documentation Files

Once connected, these files help you continue work:

- **`DAILY_WORKFLOW.md`** - Day-by-day development guide
- **`PROGRESS.md`** - Track what's completed
- **`ARCHITECTURE.md`** - Project structure reference
- **`README.md`** - Project overview

---

## 🎉 You're Almost There!

Once you push to GitHub:
1. Your project is backed up in the cloud ☁️
2. You can work on any machine 💻
3. You have full version history 📚
4. You can collaborate with others 👥

Good luck! 🚀
