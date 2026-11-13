# Updating the Hermes Hub image

## Update policy

Hermes runs here in a locally built image derived from
`nousresearch/hermes-agent:latest`. The local layer adds LaTeX for Eric's CV
workflow. Both agents share this image and one gateway, so an image replacement
briefly interrupts both Discord bots.

Check upstream stable releases every few weeks, and sooner for a relevant fix.
Read the release notes and upgrade notes before choosing an update. Upstream's
`latest` and `stable` tags track its tested stable releases; `main` tracks
development builds. Stay on the stable channel for this persistent Hub. A
version tag or digest can be used later if exact release pinning becomes useful,
but changing the Dockerfile's base image is a separate, reviewed change.

Do not run `/update` or `hermes update` inside the container. Docker-managed
Hermes is updated by rebuilding the derived image from a newer upstream image
and recreating the container. Do not enable unattended image replacement.

Upstream references:

- [Hermes releases](https://github.com/NousResearch/hermes-agent/releases)
- [Hermes Docker image channels and upgrades](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/docker.md)
- [Hermes updating guidance](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/updating.md)

## Before an update

1. Run the [routine content backup](backup.md) locally and confirm its success
   message. It covers the two agents' SOUL files, selected memories, skills and
   vaults; it is not a full backup of the persistent runtime state.
2. Review the target release notes, including migration and compatibility
   warnings, and review any intended Dockerfile or Compose changes.
3. On the VPS, record the current image ID and container status. Keep the old
   image until the replacement has been verified; do not prune images as part
   of the update.
4. For an update that may migrate persisted configuration or state, arrange a
   separate, access-controlled pre-upgrade snapshot of the relevant host data
   under `/srv/hermes-hub/state`. It may contain credentials and private
   sessions. Do not add it to the routine content-backup script or put it in
   this repository. A snapshot procedure and retention location have not yet
   been established; settle those before relying on rollback after a migration.
5. Choose a short maintenance window. Both agents may be unavailable on
   Discord while the container is replaced.

From the VPS Compose project directory, the read-only status checks are:

```bash
cd /home/rob/hermes-hub
docker compose ps
docker inspect --format '{{.Image}}' hermes-hub-agent-1
```

The recorded ID identifies the image the *running container* actually uses.
The tag `latest` alone does not establish which release is deployed.

## Rebuild and replace

Run these commands on the VPS as `rob` after the pre-update checks:

```bash
cd /home/rob/hermes-hub
docker compose build --pull agent
docker compose up -d
```

`--pull` asks Docker to fetch a newer upstream base image. Building is needed
because the LaTeX-enabled Hub image is derived from that base. `up -d` recreates
the service when its image changes while preserving the configured host mounts.
A plain `docker compose pull` is not a substitute for rebuilding this derived
image. Do not use `docker compose down -v`.

## Verify before closing maintenance

Use the checks in the [runbook](runbook.md) to confirm:

- the container is running and its logs show no new startup or migration error;
- the default-profile gateway serves both named profiles, without starting
  separate gateways;
- Bramble and Eric each respond through Discord and can access their vault;
- Eric's LaTeX toolchain remains available;
- the container is using the newly built image ID.

The LaTeX check is:

```bash
docker compose exec -T -u 988:988 agent \
  sh -lc 'command -v latexmk && latexmk --version | head -n 1'
```

If verification fails, preserve the logs and the previous image. Do not assume
that restoring the old image alone reverses a configuration or data migration;
inspect what changed before attempting rollback. Rob performs VPS commands and
decides on any restore or migration action.
