#
# setup_token.ps1 — Extract and validate a Diaflow session token from the browser.
#

$ErrorActionPreference = "Stop"
$ApiBase = "https://api.diaflow.io/api/v1"

Write-Host ""
Write-Host "=== Diaflow Token Setup ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script helps you get your authentication token from the browser."
Write-Host "Follow the steps below:"
Write-Host ""
Write-Host "  1. Open https://platform.diaflow.app in your browser"
Write-Host "  2. Log in with your account (if not already logged in)"
Write-Host "  3. Open Developer Tools: press F12 or Ctrl + Shift + I"
Write-Host ""
Write-Host "  Option A - From Network tab:" -ForegroundColor Yellow
Write-Host "    4. Click the 'Network' tab in DevTools"
Write-Host "    5. Refresh the page (F5)"
Write-Host "    6. Click any request to api.diaflow.io"
Write-Host "    7. In the 'Headers' section, find 'Authorization: Bearer ...'"
Write-Host "    8. Copy everything AFTER 'Bearer ' (the long token string)"
Write-Host ""
Write-Host "  Option B - From Application/Storage tab:" -ForegroundColor Yellow
Write-Host "    4. Click 'Application' (Chrome) or 'Storage' (Firefox)"
Write-Host "    5. Expand 'Local Storage' -> click https://platform.diaflow.app"
Write-Host "    6. Look for a key containing 'token' or 'session'"
Write-Host "    7. Copy the token value"
Write-Host ""

$Token = Read-Host "Paste your token here"

# Strip "Bearer " prefix if the user copied the whole header value
if ($Token.StartsWith("Bearer ")) {
    $Token = $Token.Substring(7)
}
$Token = $Token.Trim()

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host ""
    Write-Host "Error: No token provided. Please try again." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Validating token..."

try {
    $Response = Invoke-RestMethod -Uri "$ApiBase/users/me" `
        -Headers @{ "Authorization" = "Bearer $Token" } `
        -ErrorAction Stop

    $UserName = if ($Response.fullName) { $Response.fullName } else { "Unknown" }
    Write-Host ""
    Write-Host "Success! Authenticated as: $UserName" -ForegroundColor Green
    Write-Host ""
    Write-Host "--- Add this to your PowerShell profile (`$PROFILE): ---" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  `$env:DIAFLOW_TOKEN = `"$Token`""
    Write-Host ""
    Write-Host "--- Or set it permanently via System Environment Variables: ---" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [System.Environment]::SetEnvironmentVariable('DIAFLOW_TOKEN', '$Token', 'User')"
    Write-Host ""

    # Set for the current session
    $env:DIAFLOW_TOKEN = $Token
    Write-Host "Token has been set for the current session."
}
catch {
    $StatusCode = $_.Exception.Response.StatusCode.value__
    Write-Host ""
    Write-Host "Error: Token validation failed (HTTP $StatusCode)." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible causes:"
    Write-Host "  - The token has expired - log in again and copy a fresh token"
    Write-Host "  - The token was not copied correctly - make sure you got the full string"
    Write-Host "  - You copied the wrong value - look for the 'Authorization: Bearer ...' header"
    Write-Host ""
    Write-Host "Please try again."
    exit 1
}
