# Run this script as the logged-in Windows user.
# Do not run as SYSTEM or Administrator.

$ErrorActionPreference = "Stop"

# Chrome extension ID:
# Replace this with the actual UiPath extension ID
$ExtensionId = "YOUR_UIPATH_EXTENSION_ID"

# Locate Chrome
$ChromePaths = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$Chrome = $ChromePaths |
    Where-Object { $_ -and (Test-Path $_) } |
    Select-Object -First 1

if (-not $Chrome) {
    Write-Error "Chrome not found."
    exit 1
}

# Open UiPath extension details
$Url = "chrome://extensions/?id=$ExtensionId"

Start-Process -FilePath $Chrome -ArgumentList $Url

Write-Host "Chrome extension details opened."
Write-Host "Enable 'Allow in Incognito' manually."