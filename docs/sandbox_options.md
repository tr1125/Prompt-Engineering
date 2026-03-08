Sandbox options and safety notes

This document describes the sandbox approaches considered for executing generated CLI commands safely.

1) Dry-run (default)
   - The code returns what would be executed without running it.
   - Safe for development and initial testing.

2) Docker sandbox (recommended for real testing)
   - Requires Docker installed and available to the user.
   - The provided runner uses `docker run --rm --network=none --memory=128m --cpus=0.5 ...`.
   - Before enabling, review the command and ensure the Docker image used is minimal and unprivileged.
   - Enable by setting environment variable `ENABLE_DOCKER=1`.

3) Host execution (not recommended)
   - Running commands directly on the host is dangerous and is not implemented.

Security checklist before enabling Docker execution
-------------------------------------------------
- Use a minimal image (e.g., `alpine` or `ubuntu` trimmed to required tools).
- Mount no host volumes by default.
- Disable network access (`--network=none`) unless required and reviewed.
- Limit CPU and memory.
- Consider running inside a VM for additional isolation.
