---
name: sync
description: Sync one explicitly selected configuration between this dotfiles repository and the current machine. Use for requests such as "sync push ghostty", "sync fish config", or "sync pull ~/.agents/AGENTS.md" in this repository; default to push (machine to repository), and never treat push/pull as Git network commands.
---

# Sync a dotfile

Use this skill only in the `virgiling/dotfiles` working tree. Pi can invoke it as `/skill:sync push ghostty`; other harnesses may have different invocation syntax. Arguments after the skill command are the user request, not shell commands. Do not install a harness-specific command shim.

## Interpret the request

- `push <selector>`: copy the **current machine → repository**. `push` is the default if the first argument is a selector. `/skill:sync ghostty` means `push ghostty`.
- `pull <selector>`: copy **repository → current machine**. Never infer pull from an unrecognized argument.
- No selector, ambiguous name, multiple matching files, unsupported OS, or unclear desired version: ask which exact configuration to use before changing anything. Never sync all files implicitly.
- Neither direction means `git push`, `git pull`, commit, staging, publication, package installation, `mpm restore`, or `chezmoi update`. Do not run these as a side effect.

## Resolve the target before acting

1. Confirm the Git root is this project with `README.md`, `AGENTS.md`, `common/`, `macos/`, and `linux/`. Read [project rules](../../../AGENTS.md) and the relevant portions of the [usage guide](../../../docs/usage.md) and system guide ([macOS](../../../docs/macos.md), [Linux](../../../docs/linux.md)). Check `git status --short --untracked-files=all` and preserve unrelated work.
2. Detect the **actual** OS; use `common/` for shared `~/.agents/` targets, and `macos/` or `linux/` for system-specific targets. Each `chezmoi --source` accepts only one source. Do not run a Linux source on macOS or vice versa. Project-root `.agents/` and `AGENTS.md` are **project-only**, not aliases for the user's `~/.agents/`.
3. Resolve the selector to a **single exact destination file** under the current home and its source file. Accept an absolute/`~/` home target or a source-relative path such as `common/dot_agents/AGENTS.md` when it maps unambiguously. For app names (e.g. `ghostty`), inspect the source tree and guide to determine the intended file. For directories with several managed files (e.g. `fish`, `~/.agents/skills/`), list the candidates and request an explicit file or a reviewed set of files; never recursively `add` a broad directory by default. Only include newly discovered files after separate inspection and user scope confirmation.
4. Check `chezmoi --source "$ROOT/<chosen-source>" --working-tree "$ROOT" source-path "$target"` for managed targets; for new files explicitly verify the intended mapping. Reject path traversal, outside-home targets, symlink escapes, duplicate targets across sources, and mismatched source/target types. A symlink is stored as a symlink by default; `--follow` changes its meaning and requires an explicit choice. Don't alter global chezmoi configuration or bypass `.chezmoiignore` guards.
5. Root `macos.toml` and `linux.toml` are **package inventories, not chezmoi targets**. If explicitly requested to push a Mac inventory, use the mpm export procedure in the usage guide, confirm the `[uvx]` section was exported and recheck the project-only `[manual]` section before restoring it to the snapshot, and inspect the selected manager sections and diff before replacing it; never install or restore packages. `linux.toml` stays empty until an actual Linux inventory is available. Do not interpret `pull macos.toml` as permission to restore software. Other selectors that are not managed dotfiles need a clarified workflow.

## Push (default)

- Inspect the selected live file and destination source file, their types and any relevant diff. Do not read or copy an entire private app/agent directory. Screen for credentials, private model configuration, sessions, caches, generated files, personal data and machine-specific values; `--secrets=error` is only a helper, not a publication guarantee. Stop or ask for a safe subset if the file cannot be reviewed or contains sensitive material. Never turn off secret checks to make a push succeed.
- If the source has independent changes since the live file was last saved, compare both versions and stop to resolve the conflict rather than overwriting it. If the live file is missing, do not treat absence as a deletion request.
- For each approved regular target, use `chezmoi --source "$ROOT/<chosen-source>" --working-tree "$ROOT" add --secrets=error "$target"`. For a requested directory, handle the individually approved files, not `add ~/.config` or an unchecked recursive `add ~/.agents`. Avoid `--exact` and `--follow` unless explicitly reviewed.
- Inspect the changed source file and `git status` / `git diff` afterward. For untracked source files read them directly; `git diff` alone does not show their contents. Report which files changed. Do not stage, commit or push to a remote.

## Pull (explicit only)

- Ensure the exact selected source file exists and is the version the user wants. Preview with `chezmoi --source "$ROOT/<chosen-source>" --working-tree "$ROOT" diff "$target"`; check any existing live file, symlinks, secrets, permission changes and machine-specific values before overwriting it. Show the relevant changes and obtain confirmation when overwriting an existing differing file would discard local edits or other state. A request for `pull` authorizes only the selected target, never an entire source tree.
- Check that the target's parent directories exist; on a new machine a single-file `apply` can fail if they do not. After confirming the target path is safe, create only the required parent directories if needed. Do not resolve home-relative symlinks to destinations outside the requested scope.
- Apply only the approved target with `chezmoi --source "$ROOT/<chosen-source>" --working-tree "$ROOT" apply "$target"`. Do not use `--force` to silence conflicts; stop and ask how to resolve them. Never run software restore or reconfigure Git remotes as part of pull.
- Recheck the targeted diff and report what was written. Application behavior or Linux desktop compatibility must be verified separately; do not claim it works because chezmoi succeeded.

## Finish

State the direction, source, exact home target(s), and changes made. Report if nothing changed, if a selector was ambiguous, or if a conflict stopped the operation. Keep user/global and project agent configurations separate throughout.
