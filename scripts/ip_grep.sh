#!/usr/bin/env bash
# Prohibited-term and authorship-trace scanner.
#
# Fails (exit 1) if any tracked file contains an internal codename, an entity/client name,
# or an AI/agent authorship trace, or if any commit is authored by a non-human identity.
# The pattern list is stored base64-encoded (scripts/prohibited_terms.b64) so this scanner
# never matches itself. Wire this as a required, blocking CI check.
set -euo pipefail

cd "$(dirname "$0")/.."

TERMS_B64="scripts/prohibited_terms.b64"
if [[ ! -f "$TERMS_B64" ]]; then
  echo "ip_grep: missing $TERMS_B64" >&2
  exit 2
fi

patterns="$(base64 -d "$TERMS_B64")"
status=0

# --- Content scan over tracked files (excluding the scanner and its encoded pattern list,
#     which necessarily contain the detection patterns themselves) ---
SELF="scripts/ip_grep.sh"
while IFS= read -r file; do
  [[ "$file" == "$TERMS_B64" || "$file" == "$SELF" ]] && continue
  [[ -f "$file" ]] || continue
  if grep -nEi -f <(printf '%s\n' "$patterns") -- "$file" >/tmp/ip_hit 2>/dev/null; then
    echo "ip_grep: prohibited term in $file" >&2
    cat /tmp/ip_hit >&2
    status=1
  fi
done < <(git ls-files)

# --- Authorship-trace scan over commit history (skipped if no history present) ---
if git rev-parse --git-dir >/dev/null 2>&1; then
  # Match AI/agent authorship emails (e.g. the model co-author trailer), not legitimate
  # platform addresses such as noreply@github.com.
  if git log --format='%ae|%ce' 2>/dev/null | grep -qiE '@anthropic\.|@users\.noreply\.anthropic'; then
    echo "ip_grep: an AI/agent authorship trace was found in commit authorship" >&2
    status=1
  fi
  if git log --format='%an|%cn' 2>/dev/null | grep -qiE 'metatron'; then
    echo "ip_grep: an internal agent identity was found in commit authorship" >&2
    status=1
  fi
fi

if [[ "$status" -eq 0 ]]; then
  echo "ip_grep: clean — no prohibited terms or authorship traces."
fi
rm -f /tmp/ip_hit
exit "$status"
