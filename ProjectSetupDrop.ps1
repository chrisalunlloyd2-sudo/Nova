Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Project Auto-Setup & Rolling Uploader"
$form.Size = New-Object System.Drawing.Size(450, 250)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(32, 34, 37)
$form.FormBorderStyle = "FixedDialog"
$form.TopMost = $true

$label = New-Object System.Windows.Forms.Label
$label.Text = "[ DROP FOLDER HERE ]"
$label.Font = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$label.ForeColor = [System.Drawing.Color]::White
$label.AutoSize = $false
$label.Dock = "Fill"
$label.TextAlign = "MiddleCenter"
$form.Controls.Add($label)

$form.AllowDrop = $true

$gitPath = "C:\Users\viper\git\cmd\git.exe"
$ghPath = "C:\Users\viper\scoop\shims\gh.exe"
$env:PATH = "C:\Users\viper\git\cmd;" + $env:PATH

function Log-Step($msg, $color = "White") {
    Write-Host "[STEP] $msg" -ForegroundColor $color
}

function Process-Folder($folderPath) {
    $folderName = Split-Path $folderPath -Leaf
    Log-Step "Starting Rolling Upload for: $folderName" "Cyan"
    
    $label.Text = "Processing: $folderName"
    $label.ForeColor = [System.Drawing.Color]::Yellow
    $form.Refresh()

    Set-Location $folderPath
    Log-Step "Changed directory to $folderPath"
    
    # 1. Generate Smart README
    Log-Step "Scanning files for Smart README..."
    $files = Get-ChildItem -Path $folderPath -File | Where-Object { $_.Name -notmatch "README|Blueprint|CHANGELOG|INSTALL" }
    $fileList = if ($files) { ($files | Select-Object -ExpandProperty Name) -join "`n- " } else { "No additional files found." }
    
    $readmePath = Join-Path $folderPath "README.md"
    Log-Step "Writing README.md..."
@"
# $folderName

## Overview
Automated project bootstrap.

## Project Files
- $fileList

## Auto-Generated Features
- Recursive Documentation
- Public GitHub Deployment
"@ | Out-File $readmePath -Encoding UTF8

    # 2. Generate other docs if missing
    Log-Step "Checking for secondary documentation..."
    @("Blueprint.md", "CHANGELOG.md", "INSTALL.md") | ForEach-Object {
        $path = Join-Path $folderPath $_
        if (-not (Test-Path $path)) {
            Log-Step "Generating $_..."
            "# $_ Placeholder" | Out-File $path -Encoding UTF8
        }
    }

    # 3. Git Logic
    if (-not (Test-Path (Join-Path $folderPath ".git"))) {
        Log-Step "Initializing Git..." "Yellow"
        & $gitPath init
    }

    Log-Step "Staging files..."
    & $gitPath add .
    
    Log-Step "Committing changes..."
    & $gitPath commit -m "Rolling Auto-Setup: Project documents and files"
    
    # 4. Upload Logic
    $remotes = & $gitPath remote
    if ($remotes -contains "origin") {
        Log-Step "Existing remote found. Pushing..." "Cyan"
        & $gitPath push origin main
        if ($LASTEXITCODE -ne 0) { & $gitPath push origin master }
    } else {
        Log-Step "No remote found. Creating Public Repo via GitHub CLI..." "Magenta"
        if (Test-Path $ghPath) {
            & $ghPath repo create "$folderName" --public --source=. --remote=origin --push
        } else {
            Log-Step "ERROR: GitHub CLI (gh.exe) not found at $ghPath" "Red"
        }
    }

    if ($LASTEXITCODE -eq 0) {
        Log-Step "SUCCESS: $folderName is live on GitHub!" "Green"
        $label.Text = "✅ SUCCESS!"
        $label.ForeColor = [System.Drawing.Color]::LightGreen
    } else {
        Log-Step "FAILURE: Could not complete upload for $folderName" "Red"
        $label.Text = "❌ FAILED"
        $label.ForeColor = [System.Drawing.Color]::Red
    }

    Start-Sleep -Seconds 3
    $label.Text = "[ DROP FOLDER HERE ]"
    $label.ForeColor = [System.Drawing.Color]::White
    $form.Refresh()
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

Log-Step "GUI Ready. Waiting for drag-and-drop..." "Green"
[void]$form.ShowDialog()
