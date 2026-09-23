# dotfiles 项目约定

本文件只约束本仓库的维护。先读 `README.md`，按任务查阅 `docs/usage.md`、`docs/macos.md` 或 `docs/linux.md`。

## 范围与结构

- `common/`、`macos/`、`linux/` 是独立的 chezmoi source。`common/` 管跨系统的 `~/.agents`，系统目录只管各自专用配置；不把同一目标文件重复放进不同 source。
- 根目录 `AGENTS.md` 和 `.agents/` 仅用于维护本项目，不部署到家目录，不安装或链接到全局 agent 目录。
- `common/dot_agents/` 是要部署到 `~/.agents/` 的用户配置，和项目 `.agents/` 用途不同。不要因名称相似而同步两者，也不要自动执行其中的 skills 或脚本。
- 软件登记只使用根目录的 `macos.toml`、`linux.toml`。Linux 清单未登记时保持空白，不猜测已安装包或版本。
- 按实际使用需求选择配置，不因某个文件存在就收录。Mac 以 Fish 为主，不默认加入 zsh 或 tmux。

## 修改边界

- 维护仓库的请求允许修改仓库文件和运行隔离验证，不等于允许覆盖 `~/.config`、`~/.agents` 等实际配置。执行 apply 或其他本机部署须有对应授权。
- 显式指定 chezmoi 的 source 与 working-tree；先检查 common，再检查当前系统目录。`--source` 不会自动合并多个目录，不把仓库根目录当 source，不移除防误用检查。
- 安装、升级、卸载软件和 `mpm restore` 属于独立操作，不挂到配置同步或 Git hooks。登记软件使用 mpm 的查询/导出功能。
- 提交、推送、发布、删除远端仓库或重写历史只在获得相应授权后执行。保留与当前任务无关的工作区改动。
- 不收录密钥、认证、私有模型配置、会话、历史数据库和缓存。秘密扫描只是辅助检查；不要用整目录复制替代内容审查。
- 修改受管的 agent 规则或 skill 时，保留必要的引用、脚本和许可证；不要把项目维护规则写入用户全局规则。

## 保持简单

- 使用现有 chezmoi、mpm、Git 和 Python unittest；没有实际需要不加包装脚本、安装框架或新的配置层。
- 淘汰的文件直接删除，并更新实际引用、测试和文档，不保留备份目录、兼容别名或迁移记录。
- 用户文档只说明当前软件、配置位置和使用方法，不写工作日志。操作步骤维护在 `docs/usage.md`，避免多处重复。

## 验证

配置布局或测试发生变化时，在仓库根目录运行：

```sh
mkdir -p tmp
TMPDIR="$PWD/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

测试使用临时 home、source、配置、缓存和状态文件；不要指向实际家目录。文档修改检查链接和命令，软件清单修改检查 TOML 及管理器范围。按改动风险选择检查，不为验证重新安装软件或执行压力测试。

报告实际修改、已运行的检查及尚未验证的行为，不把渲染通过当成应用运行正常。

## 项目 skill

处理配置、清单、布局或文档维护时，使用 [maintain-dotfiles](.agents/skills/maintain-dotfiles/SKILL.md)。用户明确要求同步某个配置时，使用项目级 [sync](.agents/skills/sync/SKILL.md)：默认 push 为本机到仓库，pull 为仓库到本机；两者都不是 Git 网络命令，缺少明确目标时不操作。通用 research、review 等 skills 不在此复制第二份。
