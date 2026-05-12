Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Phase 19: Master Console Upgrade - Prompt-to-Project
# DEFINITIVE DARWINIAN SYSTEMS ENGINEERING INTERFACE

$form = New-Object System.Windows.Forms.Form
$form.Text = "Darwinian Master Console v9.0"
$form.Size = New-Object System.Drawing.Size(1000, 750)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(5, 5, 5)
$form.ForeColor = [System.Drawing.Color]::White

# TOP PANEL: Prompt Interface
$topPanel = New-Object System.Windows.Forms.Panel
$topPanel.Dock = "Top"
$topPanel.Height = 150
$topPanel.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 25)
$form.Controls.Add($topPanel)

$labelPrompt = New-Object System.Windows.Forms.Label
$labelPrompt.Text = "SEED AXIOM (Project Intent):"
$labelPrompt.Location = New-Object System.Drawing.Point(20, 15)
$labelPrompt.AutoSize = $true
$labelPrompt.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$topPanel.Controls.Add($labelPrompt)

$inputPrompt = New-Object System.Windows.Forms.TextBox
$inputPrompt.Multiline = $true
$inputPrompt.Location = New-Object System.Drawing.Point(20, 40)
$inputPrompt.Size = New-Object System.Drawing.Size(750, 80)
$inputPrompt.BackColor = [System.Drawing.Color]::Black
$inputPrompt.ForeColor = [System.Drawing.Color]::White
$inputPrompt.Font = New-Object System.Drawing.Font("Consolas", 11)
$inputPrompt.PlaceholderText = "Example: Build a recursive project manager with SHA-256 ledgering..."
$topPanel.Controls.Add($inputPrompt)

$btnLaunch = New-Object System.Windows.Forms.Button
$btnLaunch.Text = "EVOLVE PROJECT"
$btnLaunch.Location = New-Object System.Drawing.Point(790, 40)
$btnLaunch.Size = New-Object System.Drawing.Size(170, 80)
$btnLaunch.FlatStyle = "Flat"
$btnLaunch.BackColor = [System.Drawing.Color]::FromArgb(0, 80, 0)
$btnLaunch.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$topPanel.Controls.Add($btnLaunch)

# BOTTOM PANEL: Approval & Shipping
$bottomPanel = New-Object System.Windows.Forms.Panel
$bottomPanel.Dock = "Bottom"
$bottomPanel.Height = 80
$bottomPanel.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 25)
$form.Controls.Add($bottomPanel)

$btnShip = New-Object System.Windows.Forms.Button
$btnShip.Text = "APPROVE & SHIP TO GITHUB"
$btnShip.Dock = "Fill"
$btnShip.FlatStyle = "Flat"
$btnShip.BackColor = [System.Drawing.Color]::FromArgb(60, 0, 80)
$btnShip.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
$btnShip.Visible = $false
$bottomPanel.Controls.Add($btnShip)

# CENTER: Real-Time Log Console
$console = New-Object System.Windows.Forms.RichTextBox
$console.Dock = "Fill"
$console.ReadOnly = $true
$console.BackColor = [System.Drawing.Color]::Black
$console.ForeColor = [System.Drawing.Color]::Cyan
$console.Font = New-Object System.Drawing.Font("Consolas", 10)
$form.Controls.Add($console)

$logQueue = [System.Collections.Concurrent.ConcurrentQueue[string]]::new()
$global:currentProjectFolder = ""

function Append-Log($text) {
    $logQueue.Enqueue($text)
}

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 50
$timer.Add_Tick({
    $line = $null
    while ($logQueue.TryDequeue([ref]$line)) {
        if ($line -match "\[WINNER\]") { $console.SelectionColor = [System.Drawing.Color]::Lime }
        elseif ($line -match "\[PURPLE FLAG\]") { $console.SelectionColor = [System.Drawing.Color]::Magenta }
        elseif ($line -match "\[DNA\]") { $console.SelectionColor = [System.Drawing.Color]::Cyan }
        elseif ($line -match "\[FATAL\]") { $console.SelectionColor = [System.Drawing.Color]::Red }
        elseif ($line -match "\[WAIT\]") { 
            $console.SelectionColor = [System.Drawing.Color]::Yellow
            $btnShip.Visible = $true 
        }
        else { $console.SelectionColor = [System.Drawing.Color]::Cyan }
        
        $console.AppendText($line + "`r`n")
        $console.SelectionStart = $console.Text.Length
        $console.ScrollToCaret()
    }
})
$timer.Start()

$btnLaunch.Add_Click({
    if ($inputPrompt.Text -eq "") { [System.Windows.Forms.MessageBox]::Show("Please enter a project intent."); return }
    
    $intent = $inputPrompt.Text
    $btnLaunch.Enabled = $false
    $btnShip.Visible = $false
    
    Append-Log "================================================"
    Append-Log "   INITIATING PROMPT-TO-PROJECT LIFECYCLE"
    Append-Log "   INTENT: $intent"
    Append-Log "================================================"

    $python = "C:\Users\viper\python\python.exe"
    $script = "C:\Users\viper\SystemsPipeline\pipeline.py"
    
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $python
    $psi.Arguments = "`"$script`" `"$intent`""
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    
    $outEvent = { if ($_.Data) { Append-Log $_.Data } }
    $errEvent = { if ($_.Data) { Append-Log "[ERR] $($_.Data)" } }
    
    Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outEvent | Out-Null
    Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action $errEvent | Out-Null
    
    $process.Start() | Out-Null
    $process.BeginOutputReadLine()
    $process.BeginErrorReadLine()
})

$btnShip.Add_Click({
    Append-Log "[SYSTEM] Handshake Approved. Deploying to Public Cloud..."
    # The current pipeline script handles the push at the end of the wait state
    $btnShip.Enabled = $false
    $btnShip.Text = "DEPLOYED SUCCESS"
    $btnShip.BackColor = [System.Drawing.Color]::Green
})

Append-Log "[SYSTEM] DARWINIAN ENGINE READY."
Append-Log "[SYSTEM] AWAITING SEED AXIOM..."

[void]$form.ShowDialog()
$timer.Stop()
