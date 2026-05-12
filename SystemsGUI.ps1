Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 10 Core Rules Compliance: Phase 9
# Systems Engineering Automation Pipeline GUI

$form = New-Object System.Windows.Forms.Form
$form.Text = "Systems Automation Pipeline - Rolling Console"
$form.Size = New-Object System.Drawing.Size(800, 500)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$form.ForeColor = [System.Drawing.Color]::White

# Console Mirror (RichTextBox)
$console = New-Object System.Windows.Forms.RichTextBox
$console.Dock = "Fill"
$console.ReadOnly = $true
$console.BackColor = [System.Drawing.Color]::Black
$console.ForeColor = [System.Drawing.Color]::LightGreen
$console.Font = New-Object System.Drawing.Font("Consolas", 10)
$form.Controls.Add($console)

# Drop Zone (Overlay Label)
$dropZone = New-Object System.Windows.Forms.Label
$dropZone.Text = "DRAG AND DROP FOLDER HERE TO START"
$dropZone.Dock = "Top"
$dropZone.Height = 60
$dropZone.TextAlign = "MiddleCenter"
$dropZone.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
$dropZone.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$form.Controls.Add($dropZone)

$form.AllowDrop = $true

# Queue for real-time log streaming
$logQueue = [System.Collections.Concurrent.ConcurrentQueue[string]]::new()

function Append-Log($text) {
    $logQueue.Enqueue($text)
}

# Timer to poll the queue (Avoids Race Conditions)
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 100
$timer.Add_Tick({
    $line = $null
    while ($logQueue.TryDequeue([ref]$line)) {
        $console.AppendText($line + "`r`n")
        $console.SelectionStart = $console.Text.Length
        $console.ScrollToCaret()
    }
})
$timer.Start()

function Start-Pipeline($folderPath) {
    Append-Log "------------------------------------------------"
    Append-Log "INITIATING PIPELINE FOR: $folderPath"
    Append-Log "------------------------------------------------"
    
    $python = "C:\Users\viper\python\python.exe"
    $script = "C:\Users\viper\rolling_core.py"
    
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $python
    $psi.Arguments = "`"$script`" `"$folderPath`""
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    
    # Event Handlers for Real-Time Streaming
    $outEvent = {
        if ($_.Data) { Append-Log "[CLI] $($_.Data)" }
    }
    $errEvent = {
        if ($_.Data) { Append-Log "[ERR] $($_.Data)" }
    }
    
    Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outEvent | Out-Null
    Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action $errEvent | Out-Null
    
    $process.Start() | Out-Null
    $process.BeginOutputReadLine()
    $process.BeginErrorReadLine()
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
            Start-Pipeline $file
        }
    }
})

Append-Log "SYSTEM READY. Verified for Phase 9."
Append-Log "Waiting for project drop..."

[void]$form.ShowDialog()
$timer.Stop()
