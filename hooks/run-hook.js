#!/usr/bin/env node
/**
 * Hook dispatcher
 *
 * Resolves the correct hook script at runtime using a project-first strategy:
 *   1. Locate the git repository root from the current working directory.
 *   2. If <repo-root>/.claude/hooks/<name>.js exists, run it.
 *   3. Otherwise fall back to ~/.claude/hooks/<name>.js.
 *
 * Usage: node run-hook.js <hook-name>
 *   e.g. node run-hook.js session-start
 */

'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

/**
 * Resolve the git repository root for a given directory.
 *
 * @param {string} cwd - Directory to start the search from.
 * @returns {string|null} Absolute repo root path, or null if not inside a git repo.
 */
function getRepoRoot(cwd) {
  try {
    return execSync('git rev-parse --show-toplevel', {
      cwd,
      encoding: 'utf8',
      stdio: 'pipe',
    }).trim();
  } catch {
    return null;
  }
}

/**
 * Resolve the path to the hook script, preferring the project-level installation.
 *
 * @param {string} hookName - Hook filename without extension (e.g. "session-start").
 * @param {string} cwd - Current working directory used to locate the git root.
 * @returns {string} Absolute path to the hook script that should be executed.
 */
function resolveHookPath(hookName, cwd) {
  const fileName = `${hookName}.js`;
  const repoRoot = getRepoRoot(cwd);

  if (repoRoot) {
    const projectHook = path.join(repoRoot, '.claude', 'hooks', fileName);
    if (fs.existsSync(projectHook)) {
      return projectHook;
    }
  }

  return path.join(os.homedir(), '.claude', 'hooks', fileName);
}

const hookName = process.argv[2];

if (!hookName) {
  process.stderr.write('run-hook.js: hook name argument is required\n');
  process.exit(1);
}

const cwd = process.cwd();
const hookPath = resolveHookPath(hookName, cwd);

if (!fs.existsSync(hookPath)) {
  // Nothing to run – not an error, the hook may simply not be installed yet.
  process.exit(0);
}

execSync(`node ${JSON.stringify(hookPath)}`, { stdio: 'inherit' });

