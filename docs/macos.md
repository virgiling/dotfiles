# macOS 软件与配置

Mac 以 Fish 为主要 Shell，Ghostty 为终端，Zellij 用于终端工作区。共享 Agent 配置在 `common/`，其他 Mac 配置在 `macos/`；按[使用教程](usage.md)分别预览和应用。软件登记见根目录的 [macos.toml](../macos.toml)：除 mpm 的包管理器快照外，还登记了 uv 工具 `lic-cli` 和手动登记的 IINA、Présentation；Zoom 已在 `[cask]` 中。这些应用不由 chezmoi 管理，也不会自动安装。

## 软件一览

| 软件 | 用途 | 本机配置位置 |
| --- | --- | --- |
| Fish | Shell、命令补全、缩写和提示符 | `~/.config/fish/` |
| Ghostty | 终端、分屏、字体和快捷键 | `~/.config/ghostty/config` |
| Zellij | 终端工作区和会话管理 | `~/.config/zellij/config.kdl` |
| Git、delta、git-branchless | 版本控制、差异显示和 Git 工作流 | `~/.gitconfig`、`~/.gitignore`、`~/.config/git/ignore` |
| Atuin | 命令历史搜索 | `~/.config/atuin/config.toml` |
| btop | 进程与资源监控 | `~/.config/btop/btop.conf` |
| Karabiner-Elements | 键盘设置 | `~/.config/karabiner/karabiner.json` |
| Agent 规则与 skills | 多个 harness 共用的工作约定与能力 | `~/.agents/` |

## Fish

启动 Fish：

```sh
fish
```

- `config.fish`：主要设置和 PATH。
- `conf.d/`：主题、命令缩写、代理、共享历史等独立配置。
- `functions/fish_prompt.fish`：提示符。
- `fish_plugins`：Fisher 插件列表，包括 fnm、done 和 zoxide 的集成。

常用缩写将 `ls`、`ll`、`la`、`tree` 转为 eza，将 `cat` 转为 bat。使用前需要相应命令可用。插件由 Fisher 管理；保存 `fish_plugins` 不会自动安装插件。

修改 Fish 配置后，重新打开终端或启动一个新的 Fish 会话。把满意的修改保存到仓库的方法见[使用教程](usage.md)。

## Ghostty

配置使用 MD IO 字体、半透明背景，并保留 macOS 的窗口行为。

| 快捷键 | 操作 |
| --- | --- |
| `Cmd+D` | 向右分屏 |
| `Cmd+Shift+D` | 向下分屏 |
| `Cmd+Shift+Enter` | 切换当前分屏放大 |
| `Cmd+Option+方向键` | 切换分屏焦点 |
| `Cmd+Enter` | 切换全屏 |
| `Cmd+Shift+,` | 重新加载配置 |

如果不使用 MD IO，修改 `font-family` 及相关字体样式。界面与快捷键都在 `~/.config/ghostty/config` 中配置。

## Zellij、Atuin 和 btop

```sh
zellij        # 打开终端工作区
atuin search  # 搜索命令历史
btop          # 查看进程与系统资源
```

Zellij 使用 Fish 作为默认 Shell；启动目录由 `config.kdl` 的 `default_cwd` 指定，可以按自己的工作目录调整。

Atuin 的配置文件与历史数据库是分开的：仓库只管理设置，不保存数据库、账号会话或加密密钥。需要 Shell 按键集成时，按 Atuin 的配置方式单独启用。

## Git 与键盘

Git 配置使用 delta 显示差异、SSH 提交签名和 macOS keychain 凭据助手。使用前设置自己的姓名、邮箱和签名公钥路径；密钥及 keychain 数据不放进仓库。

Karabiner-Elements 的设置可在应用中修改，再用 chezmoi 保存 `~/.config/karabiner/karabiner.json`。这不会替你授予 macOS 的输入监控或其他系统权限。

## 多个 harness 共用的 Agent 配置

`~/.agents/` 包括：

- `AGENTS.md`：通用工作约定。
- `skills/`：`code-review`、`diagnosing-bugs`、`grill-me`、`grilling`、`research`、`resolving-merge-conflicts`、`skill-creator`。
- `.skill-lock.json`：skill 安装来源等元数据。

仓库中的对应位置是 `common/dot_agents/`。它与 `macos/` 是独立 source，需要分别预览；各 harness 继续读取 `~/.agents`，不需要为每个工具维护一套副本。新安装的 harness 需要确认其读取路径。

规则、skills、引用、脚本和许可证一起保存。`skill-creator` 的说明中有 Pi/uv 相关用法，Linux 使用时需确认相应工具可用。缓存、认证、私有模型配置与会话不提交；同步方法见[教程的 Agent 配置章节](usage.md#4-管理-agent-规则和-skills)。

## 按机器调整的设置

- Fish 和 Git 的代理为 `127.0.0.1:7897`，按实际代理服务调整。
- Fish 的 PATH 包含 fnm 的具体 Node 安装路径，切换版本后检查它。
- Ghostty 字体、Zellij 启动目录、Git 身份及签名路径按本机设置。
- Shell 中的 eza、bat、gcopy、git-branchless 等命令需要单独安装。

软件怎么安装仍由你决定；chezmoi 只管理配置，`macos.toml` 只记录所选包管理器报告的软件。
