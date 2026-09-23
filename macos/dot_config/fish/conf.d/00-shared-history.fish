# Restore the shared fish history when Orca has injected an isolated session id.
#
# Orca exports `fish_history=orca_<id>` into every terminal it spawns, which
# makes fish read/write `~/.local/share/fish/orca_*_history` (a small,
# per-terminal file) instead of the main `~/.local/share/fish/fish_history`.
# Clearing the injected value makes every fish session share one history.
#
# Remove this file to restore Orca's per-terminal history isolation.
if set -q fish_history; and string match -q 'orca_*' -- "$fish_history"
    set -e fish_history
end
