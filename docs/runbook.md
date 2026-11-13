# Hermes Hub runbook

## Scope

This runbook covers normal operational checks and safe management of the Hermes Hub deployment on the VPS.

Run VPS commands as `rob`, from:

```bash
cd /home/rob/hermes-hub
```

The Hub consists of one container, `hermes-hub-agent-1`, serving both named profiles: `bramble` and `eric`.

Do not expose credentials, Discord tokens, `.env` contents, `auth.json`, or raw logs containing sensitive material.

## Confirm the container is running

```bash
docker compose ps
```

Expected result: the `agent` service is running.

For a concise system-wide view:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}'
```

## Check resource use

```bash
docker stats --no-stream hermes-hub-agent-1
free -h
```

The Hub has a shared 3 GiB container memory limit. Bramble and Eric do not have separate container-level memory limits: their workloads share the Hub process and its limit.

High memory use during active research, browser work, document generation or long-running agent tasks can be normal. Investigate sustained growth or repeated process-limit failures before changing resource limits.

## Check profile status

```bash
docker compose exec -T -u 988:988 agent \
  hermes profile list
```

Expected named profiles:

```text
bramble
eric
```

For an individual profile:

```bash
docker compose exec -T -u 988:988 agent \
  hermes -p bramble profile show bramble

docker compose exec -T -u 988:988 agent \
  hermes -p eric profile show eric
```

## Check the shared gateway

The gateway runs inside the Hub container and is managed from the neutral default profile:

```bash
docker compose exec -T -u 988:988 agent \
  hermes gateway status
```

Check that each named profile is being served by the multiplexer:

```bash
docker compose exec -T -u 988:988 agent \
  hermes -p bramble gateway status

docker compose exec -T -u 988:988 agent \
  hermes -p eric gateway status
```

Expected result for each named profile:

```text
Gateway is running via the default-profile multiplexer
```

Do not start an independent gateway for Bramble or Eric. Do not use `--force`, `gateway.standalone`, or a separate per-profile gateway.

## Check container logs

Recent general logs:

```bash
docker compose logs --tail 100 agent
```

Follow logs while investigating a current problem:

```bash
docker compose logs -f --tail 100 agent
```

Do not paste raw logs into public channels. They may contain personal information, URLs, file paths or operational details.

## Restart the Hub

A normal restart preserves data under `/srv/hermes-hub`:

```bash
docker compose restart agent
```

If the container is absent or has been deliberately stopped:

```bash
docker compose up -d
```

Afterwards, verify:

```bash
docker compose ps
docker compose exec -T -u 988:988 agent hermes gateway status
```

Then send each agent a simple Discord message to confirm that it can respond and access its intended vault.

## Controlled stop

For maintenance requiring the agent to be offline:

```bash
docker compose stop agent
```

Bring it back afterwards:

```bash
docker compose start agent
```

A stopped gateway will not respond to Discord during the maintenance interval.

Avoid `docker compose down -v`. The `-v` option is unnecessary here and is inappropriate for a deployment with persistent agent data.

## Verify vault access

The intended vault locations are:

```text
Bramble: /vault/bramble
Eric:    /vault/eric
```

The most useful real-world check is to ask the relevant agent through Discord to confirm that it can read and write its own vault.

Do not treat `/vault/bramble` and `/vault/eric` as hard security isolation: both are mounted into the same container. They are separate organisational workspaces.

## LaTeX verification for Eric

The custom image includes a LaTeX toolchain for Eric’s CV workflow. To verify it after an image rebuild:

```bash
docker compose exec -T -u 988:988 agent \
  sh -lc 'command -v latexmk && latexmk --version | head -n 1'
```

Eric must write generated application outputs outside his protected factual source record.

## Backup

Run the local content backup from the development machine:

```bash
~/Documents/Codex/vps-hermes-agent-hub/scripts/vps-hermes-agent-backup.sh
```

Confirm that it prints `Backup completed for bramble and eric.`. If it reports
a failed step, treat the backup as incomplete even if earlier copies succeeded.

See `backup.md` for scope, exclusions, restoration principles and mirroring behaviour.

## Updating the Hermes image

Updating Hermes is a deliberate maintenance task, not a routine command.

Before an update:

1. Run the local backup successfully.
2. Review the intended Dockerfile or Compose changes.
3. Record the current container image and status.
4. Expect a short Discord interruption during replacement.

For the locally derived image:

```bash
cd /home/rob/hermes-hub
docker compose build --pull agent
docker compose up -d
```

Then verify the container, gateway, both profiles, Discord responses and Eric’s LaTeX toolchain.

Do not update the image solely because `latest` exists. Treat an upstream update as a change that needs verification.

## Escalation and safety

Before changing resource limits, network configuration, mounts, model configuration, Dockerfile contents, profile state or permissions:

- identify the exact target;
- inspect the current configuration;
- make one purposeful change at a time;
- verify both Bramble and Eric afterwards.

Never add the Docker socket, publish Hermes ports, attach Hermes to public application networks, or put credentials into documentation, source control or Discord messages.
