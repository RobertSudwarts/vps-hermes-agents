#!/usr/bin/env bash

set -euo pipefail

step='initialising'
trap 'status=$?; printf "Backup failed while %s (exit status %d).\n" "$step" "$status" >&2' ERR

backup=/data/vps-agent-backups
remote_rsync='docker exec -i -u 988:988 hermes-hub-agent-1 rsync'

for agent in bramble eric; do
  step="creating local profile directory for $agent"
  mkdir -p "$backup/$agent/profile"

  step="copying $agent SOUL.md"
  rsync -aH --safe-links --rsync-path="$remote_rsync" \
    "netcup:/opt/data/profiles/$agent/SOUL.md" \
    "$backup/$agent/profile/"

  step="copying $agent memories"
  rsync -aH --safe-links --rsync-path="$remote_rsync" \
    --include='/MEMORY.md' \
    --include='/USER.md' \
    --exclude='*' \
    "netcup:/opt/data/profiles/$agent/memories/" \
    "$backup/$agent/profile/memories/"

  step="copying $agent skills"
  rsync -aH --safe-links --rsync-path="$remote_rsync" \
    --exclude='.usage.json*' \
    "netcup:/opt/data/profiles/$agent/skills/" \
    "$backup/$agent/profile/skills/"

  step="mirroring $agent vault"
  rsync -aH --safe-links --delete-delay --rsync-path="$remote_rsync" \
    "netcup:/vault/$agent/" \
    "$backup/$agent/vault/"
done

printf 'Backup completed for bramble and eric.\n'
