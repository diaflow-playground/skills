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
echo "  3. Open Developer Tools:"
echo "       - Mac: Cmd + Option + I"
echo "       - Windows/Linux: F12 or Ctrl + Shift + I"
echo ""
echo "  Option A — From Network tab:"
echo "    4. Click the 'Network' tab in DevTools"
echo "    5. Refresh the page (Cmd+R or F5)"
echo "    6. Click any request to api.diaflow.io"
echo "    7. In the 'Headers' section, find 'Authorization: Bearer ...'"
echo "    8. Copy everything AFTER 'Bearer ' (the long token string)"
echo ""
echo "  Option B — From Application/Storage tab:"
echo "    4. Click 'Application' (Chrome) or 'Storage' (Firefox)"
echo "    5. Expand 'Local Storage' → click https://platform.diaflow.app"
echo "    6. Look for a key containing 'token' or 'session'"
echo "    7. Copy the token value"
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
