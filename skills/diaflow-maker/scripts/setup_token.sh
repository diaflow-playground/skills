#!/usr/bin/env bash
#
# setup_token.sh — Extract and validate a Diaflow session token from the browser.
#
set -euo pipefail

API_BASE="https://api.diaflow.io/api/v1"

echo ""
echo "=== Diaflow Token Setup ==="
echo ""
echo "This script helps you get your authentication token from the browser."
echo "Follow the steps below:"
echo ""
echo "  1. Open https://platform.diaflow.app in your browser"
echo "  2. Log in with your account (if not already logged in)"
echo "  3. Open the browser Console:"
echo "       - Mac: Cmd + Option + J (Chrome) or Cmd + Option + K (Firefox)"
echo "       - Windows/Linux: F12 then click 'Console' tab"
echo ""
echo "  4. Paste this JavaScript code into the Console and press Enter:"
echo ""
echo '     (() => { const skip = /^(__GT_|_ga|_gid|_gat|__utm|analytics|gtm)/i; const found = []; const keys = Object.keys(localStorage); for (const k of keys) { if (skip.test(k)) continue; const v = localStorage.getItem(k); try { const obj = JSON.parse(v); if (obj && typeof obj === "object") { for (const [sk, sv] of Object.entries(obj)) { if (typeof sv === "string" && sv.length > 20) { if (/token/i.test(sk)) { found.push({key: k, sub: sk, val: sv, pri: 1}); } else if (/session/i.test(sk) && !skip.test(sk)) { found.push({key: k, sub: sk, val: sv, pri: 2}); } } } } } catch(e) {} if (typeof v === "string" && v.length > 20) { if (/token/i.test(k)) { found.push({key: k, val: v, pri: 1}); } else if (/session/i.test(k)) { found.push({key: k, val: v, pri: 2}); } } } if (found.length) { found.sort((a,b) => a.pri - b.pri); const t = found[0]; console.log("Key:", t.key, t.sub ? "-> " + t.sub : ""); copy(t.val); console.log("Token copied to clipboard!"); } else { console.log("No token found. Make sure you are logged in."); } })()'
echo ""
echo "  5. The token will be automatically copied to your clipboard."
echo "     Come back here and paste it below."
echo ""

read -rp "Paste your token here: " TOKEN

# Strip "Bearer " prefix if the user copied the whole header value
TOKEN="${TOKEN#Bearer }"
# Trim whitespace
TOKEN="$(echo -n "$TOKEN" | xargs)"

if [ -z "$TOKEN" ]; then
  echo ""
  echo "Error: No token provided. Please try again."
  exit 1
fi

echo ""
echo "Validating token..."

HTTP_CODE=$(curl -s -o /tmp/diaflow_user.json -w "%{http_code}" \
  "$API_BASE/users/me" \
  -H "Authorization: Bearer $TOKEN")

if [ "$HTTP_CODE" = "200" ]; then
  USER_NAME=$(python3 -c "import json; print(json.load(open('/tmp/diaflow_user.json')).get('fullName', 'Unknown'))" 2>/dev/null || echo "Unknown")
  echo "Success! Authenticated as: $USER_NAME"
  echo ""
  echo "--- Add this to your shell profile (~/.zshrc or ~/.bashrc): ---"
  echo ""
  echo "  export DIAFLOW_TOKEN=\"$TOKEN\""
  echo ""
  echo "--- Or run this to set it for the current session: ---"
  echo ""
  echo "  export DIAFLOW_TOKEN=\"$TOKEN\""
  echo ""
  export DIAFLOW_TOKEN="$TOKEN"
  echo "Token has been exported for the current session."
  rm -f /tmp/diaflow_user.json
else
  echo ""
  echo "Error: Token validation failed (HTTP $HTTP_CODE)."
  echo ""
  echo "Possible causes:"
  echo "  - The token has expired — log in again and copy a fresh token"
  echo "  - The token was not copied correctly — make sure you got the full string"
  echo "  - You copied the wrong value — look for the 'Authorization: Bearer ...' header"
  echo ""
  echo "Please try again."
  rm -f /tmp/diaflow_user.json
  exit 1
fi
