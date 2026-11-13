#!/usr/bin/env bash

set -euo pipefail

step='initialising'
trap 'status=$?; printf "Backup failed while %s (exit status %d).\n" "$step" "$status" >&2' ERR

backup=/data/vps-agent-backups

for agent in bramble eric; do
  step="creating local profile directory for $agent"
  mkdir -p "$backup/$agent/profile"

  step="copying $agent SOUL.md"
  rsync -aH --safe-links \
    "netcup:/srv/hermes-hub/state/profiles/$agent/SOUL.md" \
    "$backup/$agent/profile/"

  step="copying $agent skills"
  rsync -aH --safe-links \
    --exclude='.usage.json*' \
    "netcup:/srv/hermes-hub/state/profiles/$agent/skills/" \
    "$backup/$agent/profile/skills/"

  step="mirroring $agent vault"
  rsync -aH --safe-links --delete-delay \
    "netcup:/srv/hermes-hub/vault/$agent/" \
    "$backup/$agent/vault/"
done

printf 'Backup completed for bramble and eric.\n'
