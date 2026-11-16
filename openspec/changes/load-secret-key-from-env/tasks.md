# Tasks

## 1. Configuration

- [x] 1.1 Read `SECRET_KEY` from the environment in `config/settings.py`, fail clearly for missing or empty values, and verify in an isolated startup check that the configured value is used without printing it.
- [x] 1.2 Add focused tests for configured and missing/empty keys and for rejection of an access token after key rotation; verify the tests pass.

## 2. Deployment

- [x] 2.1 Remove the fixed key from `deploy.sh`, preserve an existing `.env`, generate a unique secret only for a new installation, and verify the script's syntax plus both existing/new `.env` paths without exposing the secret.
- [x] 2.2 Update `docs/manual_deploy.md` with required `SECRET_KEY` setup and a production rotation procedure; verify the documented steps cover restart, old-token rejection, and repeat login.

## 3. Verification

- [x] 3.1 Run focused authentication tests and `openspec validate load-secret-key-from-env --strict`, then inspect the diff to confirm no key literal or secret value is introduced in tracked files.
