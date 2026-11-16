# Proposal

## Why

`config/settings.py` contains a fixed Django `SECRET_KEY`, which SimpleJWT uses to sign access tokens. After a database restoration, old long-lived tokens can still resolve to a different account if numeric user IDs are reused; changing the key only in `.env` currently has no effect.

## What Changes

- **BREAKING**: Require a non-empty `SECRET_KEY` from the environment when Django starts; remove the hard-coded fallback.
- Remove the fixed key from `deploy.sh` and ensure deployment supplies a secret without committing it to the repository.
- Document a production key rotation and restart that invalidates previously issued JWTs and requires users to sign in again.
- Verify startup behavior with and without the environment variable, and verify old JWTs fail after rotation.

## Capabilities

### New Capabilities

- `jwt-signing-key-configuration`: The application starts only with an externally supplied signing key and uses that key to validate JWTs.

### Modified Capabilities

None.

## Impact

- `config/settings.py`, `deploy.sh`, deployment documentation, and focused authentication/configuration tests.
- Deployment environments must set `SECRET_KEY` before starting Django. Rotating it ends all existing JWT sessions; users must sign in again.
- This change does not shorten the current 100-year JWT lifetimes or fix account-ID reuse by itself. Key rotation is required to invalidate tokens already issued with the old key.
