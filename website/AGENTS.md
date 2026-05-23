# Agent notes — whatispants.com

## Deployment

### Backend (AWS Lambda)
The backend lives in `app/` and is deployed via SAM:

```
cd app
AWS_PROFILE=<profile-name> sam build --cached --parallel
AWS_PROFILE=<profile-name> sam deploy --no-confirm-changeset
```

The `aws-sam-cli` Python package (>= 1.160) and a running Docker daemon are
required. Old SAM versions (< 1.160) fail with a misleading "Docker isn't
running" message — that's actually a docker-py API version mismatch; upgrade
SAM.

The deployed endpoint is a Lambda Function URL (no API Gateway). Function URL
handles CORS itself via `FunctionUrlConfig.Cors` in `app/template.yaml`. The
Lambda handler in `app/whatispants/app.py` MUST NOT add its own CORS headers —
duplicates make browsers reject the response with "Failed to fetch".

### Frontend (Cloudflare Pages)
The frontend at https://whatispants.com is hosted on **Cloudflare Pages** as a
static site. There's no CI: deploys are manual — you upload the `frontend/`
folder via the Cloudflare Pages dashboard.

After changing anything in `frontend/`, ask the human to drag-and-drop the
`frontend/` directory into Cloudflare Pages to publish. Don't try to automate
this.

`frontend/upload.js` contains a hardcoded `apiUrl` pointing at the deployed
Lambda Function URL. If you redeploy the backend in a way that changes the URL
(it shouldn't normally), update `apiUrl` and republish the frontend.

## Git

- **One kind of change per commit.** Do not mix unrelated changes — if a task
  produces several cohesive parts (e.g. a backend fix, a frontend tweak, a doc
  update, a build-tooling change), each goes in its own commit. Reviewers and
  `git bisect` both benefit; mixed commits make either impossible.
- Stage files by explicit path. Never use `git add -A`, `git add .`, or
  `git add -f` — they sweep in unrelated changes (or secrets, large binaries,
  scratch files) and defeat the purpose of the previous rule.
- The user may have multiple sessions open. Never claim changes are uncommitted
  without running `git status` first — another session may have already
  committed them.

## Local development

Frontend:
```
cd frontend
python3 -m http.server 8765
```
Open http://localhost:8765. The frontend hits the deployed Lambda via the
Function URL hardcoded in `upload.js` — there's no local backend in the loop by
default.

Backend (one-off invocation for testing changes without redeploying):
```
cd app
AWS_PROFILE=<profile-name> sam build --cached --parallel
echo '{"body": "warmup"}' > /tmp/event.json
sam local invoke WhatIsPantsFunction -e /tmp/event.json
```
`sam local start-api` no longer works — we replaced the API Gateway event with
a Function URL (see `template.yaml`), and `start-api` only serves
`Events: Api` resources. For browser-driven local testing you'd need to use
`sam local start-lambda` and proxy to it, which is more setup than it's worth
for this project; just deploy a dev image instead.
