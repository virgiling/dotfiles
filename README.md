# dotfiles

个人 macOS / Arch Linux 配置。**chezmoi 管理配置，mpm 登记软件，Git 保存两者。** 两个系统分别维护，不自动安装软件或同步配置。

## 目录

```text
dotfiles/
├── AGENTS.md       # 仅本项目的 agent 工作约定
├── .agents/        # 仅本项目的维护与配置同步 skills
├── common/         # Mac 和 Linux 共用的 ~/.agents 规则与 skills
├── macos/          # Mac 专用配置，包括 Fish、Ghostty
├── linux/          # Arch Linux / Hyprland 专用配置
├── macos.toml      # Mac 软件清单，mpm TOML 格式
├── linux.toml      # Linux 软件清单，目前留空
├── docs/
│   ├── usage.md    # 配置管理、软件登记和 Git 同步教程
│   ├── macos.md    # Mac 软件及用法
│   └── linux.md    # Linux 软件及用法
└── tests/          # 配置布局和清单检查
```

- [使用教程](docs/usage.md)
- [macOS 软件与配置](docs/macos.md)
- [Linux 软件与配置](docs/linux.md)

`common/`、`macos/` 和 `linux/` 是同一个 Git 仓库里的三个独立 chezmoi source：先处理 `common/`，再处理当前系统的 source。`dot_config` 对应 `~/.config`，`common/dot_agents` 对应 `~/.agents`。根目录的 TOML 清单、文档和项目 agent 文件不会部署到家目录。

项目级 [AGENTS.md](AGENTS.md) 和 `.agents/` 只用于维护本仓库，不会写入 `~/.agents`。它们与 `common/dot_agents/` 中的全局用户配置是两套独立内容；各 harness 是否自动加载项目 skills 取决于其支持，也可以从项目约定中的链接读取。

## 常用操作

先进入仓库根目录。下面以 Mac 的 Ghostty 配置为例：

```sh
cd /path/to/dotfiles

# 保存本机配置到仓库副本
chezmoi --source "$PWD/macos" --working-tree "$PWD" add --secrets=error ~/.config/ghostty/config

# 分别预览共用配置和 Mac 专用配置
chezmoi --source "$PWD/common" --working-tree "$PWD" diff
chezmoi --source "$PWD/macos" --working-tree "$PWD" diff
```

需要把仓库里的配置写回本机时，确认差异后再执行：

```sh
chezmoi --source "$PWD/macos" --working-tree "$PWD" apply ~/.config/ghostty/config
```

Linux 上同样先处理 `common/`，再选择 `--source "$PWD/linux"`。`--source` 一次只接收一个目录；不要把同一目标文件放进两个 source。不要使用仓库根目录作为 source，也不要用 `chezmoi init --apply virgiling` 自动应用整个仓库。

**`add` 默认保存文件副本，不建立实时符号链接；`apply` 才把仓库配置写到目标位置。** 文件不会在这两份之间自动同步。在 Pi 中可用 `/skill:sync push ghostty`（默认 push）或 `/skill:sync pull ~/.config/ghostty/config` 对指定配置执行这两个方向；这里的 push/pull 都不操作 Git 远端。详见[教程](docs/usage.md)。

软件继续由 Homebrew、npm、Cargo 等工具安装。更新根目录清单时使用 [mpm 导出步骤](docs/usage.md#5-更新软件清单)，不把软件安装挂到 chezmoi apply 上。

## 检查

需要 Python 3.11+、chezmoi 和 Git：

```sh
mkdir -p tmp
TMPDIR="$PWD/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

测试使用本仓库 `tmp/` 下的隔离目录，不修改实际配置、不查询或安装软件。`tmp/` 不提交 Git。

提交前检查差异，不纳入密钥、认证、私有模型配置、会话和缓存。Agent 的规则、skills、引用与脚本可以管理，但部署配置不等于执行脚本或安装 harness。
