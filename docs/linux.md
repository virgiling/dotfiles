# Arch Linux 软件与配置

桌面使用 Hyprland，终端使用 Kitty，Shell 使用 Fish 和 Starship。共享 Agent 规则和 skills 保存在 `common/`，部署到 `~/.agents/`；Linux 桌面配置保存在 `linux/`，部署到 `~/.config/`。两套 source 分别预览和应用。

## 软件一览

| 软件 | 用途 | 本机配置位置 |
| --- | --- | --- |
| Hyprland | 平铺桌面、窗口、工作区和快捷键 | `~/.config/hypr/` |
| Waybar | 桌面状态栏 | `~/.config/waybar/` |
| Rofi | 应用启动器 | `~/.config/rofi/` |
| Kitty | 终端、配色和字体 | `~/.config/kitty/kitty.conf` |
| Fish | Shell | `~/.config/fish/config.fish` |
| Starship | Shell 提示符 | `~/.config/starship.toml` |
| Mako | 桌面通知 | `~/.config/mako/config` |
| swaylock | 锁屏 | `~/.config/swaylock/config` |
| Fusuma | 触控板手势 | `~/.config/fusuma/config.yml` |
| hyprpaper、Waypaper | 壁纸配置与选择 | `~/.config/hypr/hyprpaper.conf`；Waypaper 负责选择壁纸 |
| Fastfetch、Neofetch | 终端系统信息展示 | `~/.config/fastfetch/`、`~/.config/neofetch/` |

Hyprland 配置还会调用 Nautilus、CopyQ、fcitx5、网络/蓝牙 applet 等程序。按实际使用需求安装这些组件，或调整对应的自启动项。

## Hyprland

主要文件：

- `hyprland.conf`：窗口行为、快捷键、环境变量与自启动程序。
- `monitors.conf`：显示器参数。
- `workspaces.conf`：工作区设置。
- `hyprpaper.conf`：壁纸路径。

在 Hyprland 会话中查看显示器、重新加载主配置：

```sh
hyprctl monitors
hyprctl reload
```

修改显示器、分辨率和缩放前，先用 `hyprctl monitors` 确认实际设备；壁纸和截图目录也要指向本机存在的位置。配置项以所用 Hyprland 版本支持的语法为准。

### 常用快捷键

这里的 `Super` 通常是键盘上的 Windows 键。

| 快捷键 | 操作 |
| --- | --- |
| `Super+Enter` | 打开 Kitty |
| `Super+R` | 打开 Rofi 应用启动器 |
| `Super+E` | 打开 Nautilus |
| `Super+C` | 关闭当前窗口 |
| `Super+F` | 切换全屏 |
| `Super+Space` | 切换浮动窗口 |
| `Super+方向键` | 移动焦点 |
| `Super+数字` | 切换工作区 |
| `Super+Shift+数字` | 把窗口移动到工作区 |
| `Super+X` | 调用截图工具 |

## 终端、状态栏和桌面工具

```sh
kitty             # 打开终端
fish              # 启动 Shell
rofi -show drun   # 打开应用启动器
fastfetch         # 显示系统信息
swaylock          # 锁屏
```

Fish 配置初始化 Starship。字体在 Kitty 配置中选择，使用前确认对应字体已安装。

Waybar 的内容在 `config` 中定义，外观在 `style.css` 中定义。Mako 管理通知样式，Fusuma 管理触控板手势。调整这些配置后，按对应程序的方式重新加载或重启组件。

## 使用仓库配置

在 Linux 上进入仓库根目录，分别查看共用配置与 Linux 专用配置的差异：

```sh
chezmoi --source "$PWD/common" --working-tree "$PWD" diff
chezmoi --source "$PWD/linux" --working-tree "$PWD" diff
```

确认后可逐项应用。例如，共用 Agent 规则和 Linux 专用的 Kitty 配置要分别选择 source；共享 skills 的脚本和依赖需在目标机器自行核对。

例如应用共享的 Agent 目录，并选择性应用 Kitty 配置：

```sh
chezmoi --source "$PWD/common" --working-tree "$PWD" apply ~/.agents
chezmoi --source "$PWD/linux" --working-tree "$PWD" apply ~/.config/kitty/kitty.conf
```

若是新电脑，单文件 apply 前要确认其父目录（如 `~/.config/kitty`）已存在；否则先创建父目录，再按文件应用。保存本机修改、Git 同步及目录命名见[使用教程](usage.md)。软件单独安装，不由 apply 自动安装。

根目录的 [linux.toml](../linux.toml) 暂留空，需要登记 Linux 软件时再填写；它与 `linux/` 中的配置文件是两回事。
