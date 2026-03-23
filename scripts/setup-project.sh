#!/usr/bin/env bash
# Convenience entry point for project-level installation.
# Installs Claude Scholar components into <git-repo-root>/.claude/
# instead of the user-level ~/.claude/.
#
# Usage:
#   bash scripts/setup-project.sh
#
# Run from any directory inside the target git repository.
# Accepts the same extra flags as setup.sh (e.g. --help).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec bash "$SCRIPT_DIR/setup.sh" --project "$@"

