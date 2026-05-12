Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Project Auto-Setup & Uploader"
$form.Size = New-Object System.Drawing.Size(450, 250)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(32, 34, 37)
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

$label = New-Object System.Windows.Forms.Label
$label.Text = "[ Drop Any Folder Here ]"
$label.Font = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$label.ForeColor = [System.Drawing.Color]::White
$label.AutoSize = $false
$label.Dock = "Fill"
$label.TextAlign = "MiddleCenter"
$form.Controls.Add($label)

$form.AllowDrop = $true

function Process-Folder($folderPath) {
    $folderName = Split-Path $folderPath -Leaf
    $label.Text = "Configuring $folderName..."
    $label.ForeColor = [System.Drawing.Color]::Yellow
    $form.Refresh()
    
    # 1. README.md
    $readmePath = Join-Path $folderPath "README.md"
    if (-not (Test-Path $readmePath)) {
@"
# $folderName

## Overview
A newly initialized project.

## Features
- Update this section with core features.
"@ | Out-File $readmePath -Encoding UTF8
    }

    # 2. Blueprint.md
    $blueprintPath = Join-Path $folderPath "Blueprint.md"
    if (-not (Test-Path $blueprintPath)) {
@"
# Blueprint

## Architecture
Describe the core architecture of the project here.

## File Structure
- src/ - Source code
- docs/ - Documentation
"@ | Out-File $blueprintPath -Encoding UTF8
    }

    # 3. CHANGELOG.md
    $changelogPath = Join-Path $folderPath "CHANGELOG.md"
    if (-not (Test-Path $changelogPath)) {
@"
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Initial auto-generated project structure.
"@ | Out-File $changelogPath -Encoding UTF8
    }

    # 4. INSTALL.md
    $installPath = Join-Path $folderPath "INSTALL.md"
    if (-not (Test-Path $installPath)) {
@"
# Installation and Usage

## Prerequisites
- List any dependencies here.

## Step-by-Step Installation
1. Clone the repository.
2. Install dependencies.

## Running from Command Line
start application
"@ | Out-File $installPath -Encoding UTF8
    }
    
    # Git & GitHub CLI Upload Logic
    $gitDir = Join-Path $folderPath ".git"
    $uploaded = $false
    
    $gitPath = "git"
    if (Test-Path "C:\Users\viper\git\cmd\git.exe") {
        $gitPath = "C:\Users\viper\git\cmd\git.exe"
    }
    $ghPath = "C:\Users\viper\scoop\shims\gh.exe"

    # Add portable git to environment PATH so gh.exe can find it
    $env:PATH = "C:\Users\viper\git\cmd;" + $env:PATH

    Set-Location $folderPath

    # Initialize git if it doesn't exist
    if (-not (Test-Path $gitDir)) {
        & $gitPath init
    }

    $label.Text = "Committing and Uploading..."
    $label.ForeColor = [System.Drawing.Color]::Cyan
    $form.Refresh()

    & $gitPath add .
    & $gitPath commit -m "Auto-setup: Generated docs and project files"

    # Check if a remote origin exists
    $remotes = & $gitPath remote
    if ($remotes -contains "origin") {
        # Remote exists, just push
        & $gitPath push origin main
        if ($LASTEXITCODE -ne 0) {
            & $gitPath push origin master
        }
        if ($LASTEXITCODE -eq 0) { $uploaded = $true }
    } else {
        # No remote, create a new public repo and push using gh CLI
        if (Test-Path $ghPath) {
            $label.Text = "Creating Public GitHub Repo..."
            $form.Refresh()
            
            # Using GitHub CLI to create repo
            & $ghPath repo create "$folderName" --public --source=. --remote=origin --push
            if ($LASTEXITCODE -eq 0) { $uploaded = $true }
        } else {
            $label.Text = "GitHub CLI not found."
            $label.ForeColor = [System.Drawing.Color]::Orange
            Start-Sleep -Seconds 2
        }
    }
    
    if ($uploaded) {
        $label.Text = "Success! Docs & Repo Uploaded!"
        $label.ForeColor = [System.Drawing.Color]::LightGreen
    } else {
        $label.Text = "Completed! (Locally only or Git failed)"
        $label.ForeColor = [System.Drawing.Color]::Orange
    }
    
    Start-Sleep -Seconds 3
    $label.Text = "[ Drop Any Folder Here ]"
    $label.ForeColor = [System.Drawing.Color]::White
}

$form.Add_DragEnter({
    if ($_.Data.GetDataPresent([System.Windows.Forms.DataFormats]::FileDrop)) {
        $_.Effect = [System.Windows.Forms.DragDropEffects]::Copy
    }
})

$form.Add_DragDrop({
    $files = $_.Data.GetData([System.Windows.Forms.DataFormats]::FileDrop)
    foreach ($file in $files) {
        if (Test-Path -Path $file -PathType Container) {
            Process-Folder $file
        }
    }
})

[void]$form.ShowDialog()
