# Quick GitHub Push Script for SentiPort
# Run this after creating your GitHub repository

param(
    [Parameter(Mandatory=$true, HelpMessage="Your GitHub username")]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false, HelpMessage="Repository name (default: SentiPort)")]
    [string]$RepoName = "SentiPort"
)

$gitPath = "C:\Program Files\Git\bin\git.exe"
$repoUrl = "https://github.com/$GitHubUsername/$RepoName.git"

Write-Host "🚀 SentiPort GitHub Push Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is available
if (-not (Test-Path $gitPath)) {
    Write-Host "❌ Git not found at $gitPath" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git found" -ForegroundColor Green
Write-Host "📍 Repository: $repoUrl" -ForegroundColor White
Write-Host ""

# Add remote
Write-Host "1️⃣  Adding GitHub remote..." -ForegroundColor Yellow
& $gitPath remote add origin $repoUrl
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Remote added" -ForegroundColor Green
} else {
    Write-Host "⚠️  Remote might already exist. Updating..." -ForegroundColor Yellow
    & $gitPath remote set-url origin $repoUrl
}

# Set branch to main
Write-Host ""
Write-Host "2️⃣  Setting branch to 'main'..." -ForegroundColor Yellow
& $gitPath branch -M main
Write-Host "✅ Branch set to main" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "3️⃣  Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "⏳ This may take a moment..." -ForegroundColor Cyan
& $gitPath push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Your code is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 You can now:" -ForegroundColor Cyan
    Write-Host "   • Access your code at: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor White
    Write-Host "   • Clone on other machines: git clone $repoUrl" -ForegroundColor White
    Write-Host "   • Start development: npm install && npm run dev" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Check:" -ForegroundColor Red
    Write-Host "   • Your GitHub username is correct" -ForegroundColor Yellow
    Write-Host "   • Your repository exists on GitHub" -ForegroundColor Yellow
    Write-Host "   • Your Personal Access Token is correct" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "See GITHUB_CONNECT.md for more help." -ForegroundColor Cyan
}
