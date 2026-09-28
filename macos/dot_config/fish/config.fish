if status is-interactive
# Commands to run in interactive sessions can go here

# Launch Claude Code in ultracode mode by default (xhigh effort + standing
# dynamic-workflow orchestration). Ultracode is session-only in Claude Code and
# cannot be persisted in settings.json, so the alias re-injects the flag at
# every launch. `command` bypasses function lookup to avoid infinite recursion.
alias claude 'command claude --effort ultracode'
end

set -g fish_color_autosuggestion 555 --italic

# Pi
fish_add_path "/Users/virgil/.local/share/fnm/node-versions/v24.19.0/installation/bin"


test -f '/Users/virgil/.local/share/inshellisense/init/fish/init.fish' && source '/Users/virgil/.local/share/inshellisense/init/fish/init.fish'
