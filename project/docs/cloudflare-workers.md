# Cloudflare Workers setup

This document records the Cloudflare resources and decisions used by
ReportReady. It must not contain passwords, API tokens, account identifiers,
or other secrets.

## Architecture decision

ReportReady will use a small, serverless TypeScript stack:

- SvelteKit for the web interface.
- Hono for the HTTP API.
- Cloudflare Workers for application hosting.
- Cloudflare D1 for relational data.
- Zod for request and business-rule validation.
- Vitest for automated tests.
- Wrangler for local development, database migrations, and deployment.
- GitHub Actions for continuous integration.

This keeps the demonstration inexpensive and avoids operating a permanent
server. The project will stay within Cloudflare's free allowances during
development. Usage must still be monitored because free-plan limits can
change.

## Resource names

Use predictable names so the dashboard and configuration agree.

| Resource | Name | Status |
|---|---|---|
| Worker | `reportready` | Deployed on 3 September 2026 |
| Public Worker URL | `https://reportready.tmsnobrega.workers.dev` | Active in Cloudflare |
| D1 database | `reportready-db` | Not created yet |
| D1 binding | `DB` | Planned |

## Cloudflare dashboard setup

Account: the existing personal Cloudflare account.

1. Open **Workers & Pages** and select **Create application**.
2. Select **Start with Hello World**.
3. Set the Worker name to `reportready`.
4. Leave **Cloudflare Access** disabled for the public portfolio demo.
5. Deploy the starter Worker and verify that its public URL returns
   `Hello World!`.

The starter is only a connectivity check. It will later be replaced by code
from this repository. The Cloudflare dashboard reports a successful manual
deployment with Worker Logs enabled and Traces disabled.

The dashboard confirms the public route. Direct response verification from the
current workstation was blocked by its browser and Windows TLS client, so the
HTTP 200 and response-body checks remain open. This limitation must not be
reported as an application failure.

## Planned repository connection

Do not connect GitHub until the ReportReady application scaffold and build
commands exist. Connecting an empty project now would create a deployment that
cannot reproduce the dashboard-created starter.

When the scaffold is ready:

1. Connect Cloudflare to `tmsnobrega/ai-dev-zoomcamp-2026`.
2. Limit repository access to this repository if GitHub offers that choice.
3. Set the application root to `project`.
4. Configure the production branch as `main`.
5. Verify the detected build and deployment commands against `package.json`.
6. Confirm that a commit to `main` creates one successful production deploy.

## Planned D1 setup

Create the database only when the first schema migration exists. The expected
configuration will resemble:

```toml
[[d1_databases]]
binding = "DB"
database_name = "reportready-db"
database_id = "replace-with-cloudflare-generated-id"
migrations_dir = "migrations"
```

The generated database ID is configuration, not a secret. API tokens and
credentials must be stored in Cloudflare secrets or GitHub Actions secrets and
must never be committed.

## Security decisions

- Do not create or store an API token during the initial dashboard smoke test.
- Do not upload real employer, partner, or client data.
- Use synthetic CSV files in the public demonstration.
- Reject unexpected file types and enforce a small upload-size limit.
- Validate every uploaded row with deterministic code.
- Let AI explain verified results, but never let it approve a failed report.
- Keep production secrets out of `.dev.vars`, logs, screenshots, and commits.

## Validation checklist

Record evidence after each item is completed:

- [x] The Worker exists under the `reportready` name.
- [ ] The public URL returns an HTTP 200 response.
- [ ] The starter response contains only `Hello World!`.
- [x] No paid plan or billing step was used during Worker creation.
- [ ] No Cloudflare or GitHub credentials were committed.
- [ ] The application can run locally with Wrangler.
- [ ] D1 migrations work against the local database.
- [ ] D1 migrations work against the production database.
- [ ] GitHub Actions runs tests before deployment.
- [ ] The deployed application passes a basic smoke test.

## Useful commands

These commands are planned for the application scaffold:

```powershell
# Run the application locally.
npm run dev

# Run the automated checks.
npm test

# Apply database migrations locally before using production data.
npx wrangler d1 migrations apply reportready-db --local

# Deploy the current version after validation passes.
npm run deploy
```

Do not run a production migration or deployment without first reviewing the
target environment and the pending changes.
