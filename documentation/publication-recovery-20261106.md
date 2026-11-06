# Pages publication recovery, 6 November 2026

A Pages deployment timed out. A later build rerun left two artifacts with the same default name in the workflow run, so deployment could not select exactly one.

Each build attempt now uploads a Pages artifact named with its workflow run ID and attempt number. The build exports that name, and deployment uses the build output. A deploy-only rerun therefore selects the artifact produced by its retained build, rather than deriving a new name from the deploy attempt. Existing artifacts are retained.

This changes publication plumbing only; it does not change release content or Pages permissions. Successful CI, deployment, and live verification must be established by their respective workflow results.
