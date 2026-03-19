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
Write-Host "  3. Open the browser Console:" -ForegroundColor Yellow
Write-Host "       - Press F12 then click the 'Console' tab"
Write-Host ""
Write-Host "  4. Paste this JavaScript code into the Console and press Enter:" -ForegroundColor Yellow
Write-Host ""
Write-Host '     (() => { const skip = /^(__GT_|_ga|_gid|_gat|__utm|analytics|gtm)/i; const found = []; const keys = Object.keys(localStorage); for (const k of keys) { if (skip.test(k)) continue; const v = localStorage.getItem(k); try { const obj = JSON.parse(v); if (obj && typeof obj === "object") { for (const [sk, sv] of Object.entries(obj)) { if (typeof sv === "string" && sv.length > 20) { if (/token/i.test(sk)) { found.push({key: k, sub: sk, val: sv, pri: 1}); } else if (/session/i.test(sk) && !skip.test(sk)) { found.push({key: k, sub: sk, val: sv, pri: 2}); } } } } } catch(e) {} if (typeof v === "string" && v.length > 20) { if (/token/i.test(k)) { found.push({key: k, val: v, pri: 1}); } else if (/session/i.test(k)) { found.push({key: k, val: v, pri: 2}); } } } if (found.length) { found.sort((a,b) => a.pri - b.pri); const t = found[0]; console.log("Key:", t.key, t.sub ? "-> " + t.sub : ""); copy(t.val); console.log("Token copied to clipboard!"); } else { console.log("No token found. Make sure you are logged in."); } })()'
Write-Host ""
Write-Host "  5. The token will be automatically copied to your clipboard."
Write-Host "     Come back here and paste it below."
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
