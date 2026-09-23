# 使用教程

本仓库分工：**chezmoi 管配置，mpm 登记软件，Git 保存改动。** 软件安装仍由 Homebrew、npm、Cargo 等工具负责。

## 项目级 sync skill（可选）

在支持项目 Agent Skills 的 harness 中，可以调用本仓库的 `.agents/skills/sync/SKILL.md`。Pi 的明确调用方式是 `/skill:sync`（修改后在 Pi 中执行 `/reload`；首次使用项目 skill 需先信任项目）：

```text
/skill:sync push ghostty
/skill:sync ghostty
/skill:sync pull ~/.config/ghostty/config
/skill:sync push ~/.agents/AGENTS.md
```

省略方向时默认为 **push：本机配置 → 本仓库**；只有写明 `pull` 才会将仓库配置应用到本机。必须指定一个可识别的配置；名称指向多个文件时会先确认具体范围。`push` 和 `pull` **都不是 Git push/pull**，不会自动暂存、提交、访问 GitHub、安装软件或恢复软件清单。其他 harness 可用其支持的 skill 调用方式，不需要 Pi 专用转接命令。以下章节是手动操作时的对应命令和注意事项。

## 1. 选择配置源

已有本地仓库就直接进入它；新电脑上先 clone：

```sh
git clone https://github.com/virgiling/dotfiles.git
cd dotfiles
```

后面的命令都在**仓库根目录**执行，`$PWD` 表示这个目录。

Mac 和 Linux 都先查看共享配置：

```sh
chezmoi --source "$PWD/common" --working-tree "$PWD" diff
```

再查看所在系统的专用配置（只运行其中一个）：

```sh
# Mac
chezmoi --source "$PWD/macos" --working-tree "$PWD" diff
# Linux
chezmoi --source "$PWD/linux" --working-tree "$PWD" diff
```

`--source` **一次只选择一个**配置源，不会自动合并 `common/` 和系统目录；`--working-tree` 指向共同的 Git 仓库。`diff` 只显示差异，不修改配置。分别确认后按相同顺序选择性应用，不把同一目标文件放在两个 source 中。

仓库根目录不是 chezmoi source，不要使用 `chezmoi init --apply virgiling`。本教程不修改全局 chezmoi 设置，因此后续命令保留显式的 source 参数；不要假设裸 `chezmoi apply` 已指向这里。

## 2. 理解 add：保存副本，不是建立实时链接

在默认 file 模式下，对普通文件执行 `chezmoi add`，是把它当前的内容保存到 source 中：

```text
本机：~/.config/ghostty/config
            │
            │ chezmoi add：读取并保存
            ▼
仓库：macos/dot_config/ghostty/config
```

**原文件仍在原位置，不会被替换成符号链接。** 仓库中的副本和原文件不会自动互相更新。这不是 Git clone，也不是把整个家目录复制进来。

| 添加的目标 | 默认行为 |
| --- | --- |
| 一个普通文件 | 保存该文件的内容；已经受管则更新 source 副本 |
| 一个目录 | 递归收录该目录下未被忽略的内容，不包括无关目录 |
| 一个符号链接 | 保存链接目标信息，而不是自动复制链接所指的内容 |
| 符号链接加 `--follow` | 收录它指向的内容，原链接不因此变成普通文件 |

chezmoi 会用 `dot_` 等命名规则记录目标文件名和属性：

```text
macos/dot_gitconfig                  → ~/.gitconfig
macos/dot_config/fish/config.fish     → ~/.config/fish/config.fish
common/dot_agents/AGENTS.md           → ~/.agents/AGENTS.md
common/dot_agents/dot_skill-lock.json → ~/.agents/.skill-lock.json
```

### 保存已经改好的本机配置

例如你改好了 Ghostty 的实际配置：

```sh
chezmoi --source "$PWD/macos" --working-tree "$PWD" add --secrets=error ~/.config/ghostty/config
git status --short
git diff -- macos/dot_config/ghostty/config
```

这是“本机 → 仓库”，不需要再 apply。新增配置也用同样的方式添加。

`--secrets=error` 是辅助检查，不代替人工审查。只添加需要的文件或已检查的应用目录，不直接 `add ~`、`add ~/.config`，也不用 `--exact` 管理整个家目录。

新文件还未被 Git 跟踪时，普通 `git diff` 不显示其内容；先检查文件，暂存后再用 `git diff --cached` 查看。

## 3. 理解 apply：把仓库配置写回本机

如果你修改的是仓库里的 `macos/dot_config/ghostty/config`，先查看对应差异：

```sh
chezmoi --source "$PWD/macos" --working-tree "$PWD" diff ~/.config/ghostty/config
```

确认后才写回：

```sh
chezmoi --source "$PWD/macos" --working-tree "$PWD" apply ~/.config/ghostty/config
```

这是“仓库 → 本机”。本仓库按默认 file 模式使用，不会把普通配置文件自动改成指向仓库的链接。首次在新机器上单文件 apply 时，需先确认父目录（例如 `~/.config/ghostty`）存在；对共享 Agent 配置可应用 `~/.agents` 整个目录。应用后按软件要求重新加载配置。

不要在 apply 前无条件执行 add：如果仓库副本才是你想保留的新版本，add 可能把本机的旧内容重新覆盖回仓库。

出现两边都改过的情况，先检查和合并内容，再决定方向；必要时在仓库外临时保存冲突文件。

## 4. 管理 Agent 规则和 skills

先区分两种作用域：仓库根目录的 [AGENTS.md](../AGENTS.md) 和 `.agents/` 只服务本项目，不部署到家目录；`common/dot_agents/` 才部署到用户级 `~/.agents/`，供 Mac 与 Linux 的多个 harness 使用：

- `AGENTS.md`：通用工作约定。
- `skills/`：skills 及其脚本、引用和许可证。
- `.skill-lock.json`：来源记录，不代替本地定制的 skill 正文。

保存某个规则或 skill 的本机修改：

```sh
chezmoi --source "$PWD/common" --working-tree "$PWD" add --secrets=error ~/.agents/AGENTS.md
chezmoi --source "$PWD/common" --working-tree "$PWD" add --secrets=error ~/.agents/skills/research
```

安装器改变了来源记录时，检查后单独保存：

```sh
chezmoi --source "$PWD/common" --working-tree "$PWD" add --secrets=error ~/.agents/.skill-lock.json
```

反方向同步时使用 common source，先 `diff ~/.agents`，确认后才 `apply ~/.agents`。这是独立于系统 source 的第二次检查和应用；目标位置不变，现有 harness 的引用也不用改。

新机器需要确认各 harness 配置为读取 `~/.agents`；个别 skill（如 `skill-creator`）带 Pi/uv 用法，Linux 上使用前先检查依赖。同步目录不等于安装 harness、执行 skill 脚本或自动更新远端 skills。

`__pycache__` 等生成文件已有忽略规则；认证、私有模型配置、会话和私人数据不提交。

## 5. 更新软件清单

根目录只有两个清单：

- [macos.toml](../macos.toml)：Mac 软件登记；`[brew]`、`[cask]`、`[npm]`、`[cargo]`、`[uvx]` 由 mpm 导出，`[manual]` 手动登记所选的本机应用。`[manual]` 不是 mpm 管理器，mpm restore 会忽略它。Zoom 已列在 `[cask]`，不在 `[manual]` 重复登记。
- [linux.toml](../linux.toml)：暂留空，需要登记时再填写。

它们是软件现状登记，不是必须安装的清单，也不是保证完整复现环境的锁文件。

### Mac 上重新导出

使用 mpm 8.0.0+。先导出到 Git 忽略的临时目录，不直接覆盖当前清单：

```sh
mkdir -p tmp
mpm --no-config --stop-on-error --jobs 1 --timeout 30 \
  --brew --cask --npm --cargo --uvx dump --overwrite tmp/macos.toml
```

这只查询所选管理器，不安装或升级软件。`--uvx` 登记的是 `uv tool` 已安装的工具，不包括 uv 的项目依赖或临时执行命令。mpm 8.0.0 的 `uvx` 要求 uv >=0.10.10；如果新机器不满足，先用 `mpm --uvx managers` 检查，不要采用缺少该章节的不完整导出，更不要为了导出自动升级 uv。**只有本次导出成功后才继续**；失败时不要采用临时文件。

查看新旧清单的差异：

```sh
git diff --no-index -- macos.toml tmp/macos.toml
```

这个比较命令返回 `1` 表示存在差异，不是导出失败。检查五个 mpm 管理器章节（包括 `[uvx]`）和包条目，确认没有因环境变化而意外遗漏。完整导出不会产生项目专用的 `[manual]`，**不要直接用临时文件覆盖**：先检查实际应用与当前清单，按需将 `[manual]` 的 bundle ID 和版本补回临时文件。Zoom 已由 Cask 管理，不能因为它的应用版本与 Homebrew 记录不同就改写 `[cask].zoom` 或复制到 `[manual]`。检查临时文件的 TOML 和最终差异后再替换：

```sh
mv tmp/macos.toml macos.toml
git diff -- macos.toml
```

注意：

- npm 反映当前 Node/npm 环境，切换 fnm 版本后全局包集合可能变化。
- `[manual]` 仅包含选定的 IINA 与 Présentation；版本来自 `/Applications/` 中应用的 Info.plist，安装来源不确定，不冒充 Cask 安装。mpm restore 会忽略这个项目专用章节，也不能用它安装这两个应用。
- `[uvx]` 是 uv 的已安装工具清单；当前条目已用 `mpm --uvx dump` 核对，可与其他选定管理器一同自动导出。
- 清单并不覆盖所有手动安装软件或项目依赖。
- 完整重新导出会反映卸载；不把仅增加条目的 `--merge` 当作完整刷新。
- 更新清单不执行 `mpm restore`，也不会触发 `chezmoi apply`。

软件继续按原来的方式安装；需要恢复时，再单独选择所需项目和安装方式。

## 6. 使用 Git 保存和同步

以修改一个 Ghostty 配置为例：

```sh
git add -- macos/dot_config/ghostty/config
git diff --cached
```

检查暂存区中的所有内容，确认没有凭据或无关改动后再提交：

```sh
git commit -m "Update Ghostty config"
git push
```

首次推送需要设置上游，例如当前分支为 `master` 时使用 `git push -u origin master`。清单改动也一样，暂存对应的 `macos.toml` 即可。

从远端同步前先处理本地修改，包括家目录里尚未 add 的配置。然后拉取并检查：

```sh
git pull --ff-only
chezmoi --source "$PWD/common" --working-tree "$PWD" diff
chezmoi --source "$PWD/macos" --working-tree "$PWD" diff  # Linux 换成 linux
```

确认后选择性 apply。Git pull 不部署配置；chezmoi diff 也不等于 git diff。前者比较本机与 source，后者比较仓库工作区与 Git 中的版本。

如果 Git 提示分支分叉，先处理分支关系，不用强制重置跳过问题。

## 7. 停止管理一个配置

决定不再管理某个文件时使用 `forget`，下面仅为示例：

```sh
chezmoi --source "$PWD/macos" --working-tree "$PWD" forget ~/.config/ghostty/config
```

它从 source 中移除条目，**不删除本机实际文件，也不卸载软件**。审查并提交仓库中的删除即可。需要删除本机文件时，再单独处理。

## 8. 在另一台电脑使用

1. Clone 本仓库，独立安装 chezmoi 和需要的软件。
2. 阅读 [macOS](macos.md) 或 [Linux](linux.md) 软件说明。
3. 先用 `common/`，再用对应的 `macos/` 或 `linux/` source，分别 diff，不一次性盲目覆盖。
4. 检查本机路径、Git 身份、代理、字体、显示器等设置。
5. 选择性 apply，启动应用确认效果。

软件安装与配置同步始终分开，不默认 restore 整份软件清单。

## 官方参考

- [chezmoi add](https://www.chezmoi.io/reference/commands/add/)
- [chezmoi apply](https://www.chezmoi.io/reference/commands/apply/)
- [chezmoi forget](https://www.chezmoi.io/reference/commands/forget/)
- [mpm 软件清单导出](https://github.com/kdeldycke/meta-package-manager/blob/main/docs/dump.md)
