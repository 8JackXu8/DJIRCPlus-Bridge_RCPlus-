# DJI RC Plus Gamepad Bridge (RC Plus 虚拟手柄驱动)

本项目提供了一个 Python 脚本，通过 ADB (Android Debug Bridge) 读取大疆 **DJI RC Plus** 行业版遥控器的底层输入信号，并将其映射为 Windows 系统的 **虚拟 Xbox 360 手柄**。

你可以直接使用 RC Plus 玩 PC 游戏（如《微软模拟飞行》、《地平线》、《GTA》）或在模拟器中练飞，无需大疆官方 SDK 支持，也无需复杂的硬件改造。

## 功能特性

* **全按键映射**：支持左右摇杆、左右波轮、以及 6 个物理按键 (R1-R6)。
* **模拟扳机**：将遥控器顶部的两个波轮映射为 Xbox 的线性扳机 (LT/RT)，完美适配赛车油门或飞行方向舵。
* **低延迟**：通过 USB 有线 ADB 传输，延迟极低，优于蓝牙映射方案。
* **即插即用**：依赖 `ViGEmBus` 虚拟驱动，游戏自动识别为标准 Xbox 360 手柄。

## 前置准备

### 1. 硬件要求
* **DJI RC Plus** 遥控器
* Windows 电脑
* USB-C 数据线

### 2. 软件与驱动
1.  **安装 ViGEmBus 驱动** (必须)：
    * 这是 Windows 虚拟手柄的基础驱动。
    * [点击下载 ViGEmBus (GitHub)](https://github.com/ViGEm/ViGEmBus/releases/latest)
    * 下载 `.exe` 文件安装并**重启电脑**。
2.  **安装 Python 环境**：
    * 确保安装了 Python 3.x。
    * 打开CMD安装虚拟手柄依赖库：
      ```bash
      pip install vgamepad
      ```
3.  **ADB 工具**：
    * 下载 `platform-tools` 包 (包含 `adb.exe`)。
    * 建议将 `adb.exe` 放在本脚本的同一目录下。
4.  **DJI Assistant 2 (可选)**：
    * 如果电脑完全不识别 USB 设备，请安装 [DJI Assistant 2 (行业版)](https://www.dji.com/cn/downloads/softwares/dji-assistant-2-enterprise) 以获取底层 USB 驱动。

## 遥控器设置 (开启 ADB)

为了让脚本能读取数据，必须开启遥控器的 **USB 调试**：

1.  在 RC Plus 上进入 **设置** 。
2.  连续点击 **版本号** 多次，直到提示“您已处于开发者模式”。
3.  返回设置，进入 **系统** -> **开发者选项**。
4.  开启 **USB 调试**。
5.  连接电脑，在遥控器弹出的授权窗口中点击 **“允许”**。
6.  将下面的USB模式改文传输文件

## 使用方法

1.  将 `rc_gamepad.py` 放在刚刚下载并解压好的`platform-tools`文件根目录中。
2.  连接遥控器与电脑。
3.  在文件夹空白处按住 `Shift` 键并点击鼠标 **右键**，选择 **“在此处打开 PowerShell 窗口”**。
4.  运行脚本：
    ```bash
    python rc_gamepad.py
    ```
5.  当看到 `[系统] 虚拟手柄驱动加载成功！` 和 `[成功] 数据流已建立` 时，虚拟手柄即生效。
6.  **保持黑色窗口运行**，直接进入游戏即可。

## 按键映射表

| DJI RC Plus (硬件) | Xbox 360 (映射) | 游戏中的典型功能 |
| :--- | :--- | :--- |
| **左摇杆** | 左摇杆 (Left Stick) | 移动 / 偏航 (Yaw) |
| **右摇杆** | 右摇杆 (Right Stick) | 视角 / 俯仰横滚 (Pitch/Roll) |
| **左波轮** (顶部) | 左扳机 (LT) | 刹车 / 瞄准 / 下降 |
| **右波轮** (顶部) | 右扳机 (RT) | 油门 / 射击 / 上升 |
| **F1 键** | A 键 | 确认 / 跳跃 |
| **F2 键** | B 键 | 返回 / 蹲下 |
| **F3 键** | X 键 | 交互 / 换弹 |
| **F4 键** | Y 键 | 菜单 / 切换武器 |
| **F5 键** | LB (Left Bumper) | 左肩键 |
| **F6 键** | RB (Right Bumper) | 右肩键 |

## 测试手柄

请保持黑色窗口（PowerShell）运行不要关闭，然后进行以下操作：
1.  在键盘上按 Win + R，输入 joy.cpl 并回车。
2.  你会看到列表中有一个 "Controller (Xbox 360 For Windows)"（或者是 ViGEm 相关的名字）。
3.  点属性，进入测试界面。
4.  动一动大疆的摇杆：
• 左摇杆：屏幕上的十字光标应该会动。
• 右摇杆：屏幕上的右侧两个条（X旋转/Y旋转）应该会动。
• 按键：按下遥控器上的实体键（C1/C2等），屏幕上的红色按钮号应该会亮。

## 微调手柄

如果在测试中发现问题，请按 Ctrl + C 停止脚本，用记事本打开 'rc_gamepad.py' 文件修改对应参数，然后重新运行：
• 问题 A：摇杆动一点，电脑上就满了（太灵敏）
• 解决： 找到 SCALE_FACTOR = 1.0，把它改小（比如改到 2.0 或 1.5）。
• 问题 B：摇杆推到底，电脑上才走一半（太迟钝）
• 解决： 把 SCALE_FACTOR 改大（比如 2.0）。
• 问题 C：上下方向反了（推杆变成向后走）
• 解决： 找到 update_joystick 函数部分：
• 如果是左摇杆反了，把 gamepad.left_joystick 下面的 y_value 改一下符号（比如把 -joystick_state 改成 joystick_state，或者反过来）。
• 右摇杆同理。
> *注：可以在脚本代码中修改 `KEY_F1` 到 `KEY_F6` 的映射关系。*
> 其他版本遥控器正在适配中

## 常见问题
Q: 运行脚本后报错 FileNotFoundError?
A: 说明脚本没找到 adb.exe。请确保你下载了 ADB 工具包，并且把 adb.exe 放在了脚本旁边。
Q: 游戏里没反应？
A: 请打开 Windows 的“设置 USB 游戏控制器”或访问 Gamepad Tester 网站测试。如果网站上有反应，说明驱动工作正常，请在游戏设置里手动绑定手柄按键。


