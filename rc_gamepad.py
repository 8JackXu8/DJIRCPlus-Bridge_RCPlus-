import subprocess
import os
import vgamepad as vg
import sys

# === 配置区域 ===
# 灵敏度设置
STICK_SCALE = 1.0      # 摇杆灵敏度 (X/Y)
WHEEL_SCALE = 1.0      # 波轮灵敏度 (Z/RZ)，数值越大波轮越灵敏

# 自动寻找 ADB
if os.path.exists("adb.exe"):
    ADB_PATH = "adb.exe"
else:
    ADB_PATH = "adb"

# 初始化虚拟手柄
try:
    gamepad = vg.VX360Gamepad()
    print("[成功] 虚拟手柄驱动已加载！")
except Exception as e:
    print(f"[错误] 无法加载虚拟手柄: {e}")
    sys.exit()

print(f"[提示] 使用 ADB: {ADB_PATH}")
print("[提示] 左波轮 -> LT (刹车/瞄准)")
print("[提示] 右波轮 -> RT (油门/射击)")
print("正在连接 RC Plus...")

# 启动监听
cmd = [ADB_PATH, 'shell', 'getevent', '-l']
try:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
except FileNotFoundError:
    print("\n[错误] 找不到 adb.exe，请把脚本放到 platform-tools 文件夹里！")
    sys.exit()

# 状态存储
state = {
    'LX': 0, 'LY': 0,
    'RX': 0, 'RY': 0,
    'LT': 0, 'RT': 0 # 波轮状态
}

def hex_to_int(hex_str):
    try:
        val = int(hex_str, 16)
        if val > 0x7FFFFFFF: val -= 0x100000000
        return val
    except: return 0

def update_gamepad():
    # 1. 处理摇杆 (限制在 -32768 到 32767)
    lx = int(max(-32768, min(32767, state['LX'] * STICK_SCALE)))
    ly = int(max(-32768, min(32767, -state['LY'] * STICK_SCALE))) # Y轴反转
    rx = int(max(-32768, min(32767, state['RX'] * STICK_SCALE)))
    ry = int(max(-32768, min(32767, -state['RY'] * STICK_SCALE))) # Y轴反转
    
    gamepad.left_joystick(x_value=lx, y_value=ly)
    gamepad.right_joystick(x_value=rx, y_value=ry)

    # 2. 处理波轮 -> 线性扳机 (LT/RT)
    # 大疆波轮通常中心是0，往一边拨是正数，往一边是负数
    # Xbox扳机只接受 0-255 (正数)
    # 逻辑：取绝对值，或者只取正向
    
    # 左波轮控制 LT
    lt_val = int(abs(state['LT']) * WHEEL_SCALE)
    lt_val = max(0, min(255, lt_val))
    
    # 右波轮控制 RT
    rt_val = int(abs(state['RT']) * WHEEL_SCALE)
    rt_val = max(0, min(255, rt_val))

    gamepad.left_trigger(value=lt_val)
    gamepad.right_trigger(value=rt_val)

    gamepad.update()

print("[成功] 开始监听，请操作...")

try:
    for line in process.stdout:
        line = line.strip()
        if not line: continue
        parts = line.split()
        if len(parts) < 4: continue

        device = parts[0].replace(":", "")
        ev_type = parts[1]
        code = parts[2]
        value_hex = parts[3]

        # === 处理摇杆与波轮 (Event 4) ===
        if "event4" in device and ev_type == "EV_ABS":
            val = hex_to_int(value_hex)
            
            # 摇杆
            if code == "ABS_X": state['LX'] = val
            elif code == "ABS_Y": state['LY'] = val
            elif code == "ABS_RX": state['RX'] = val
            elif code == "ABS_RY": state['RY'] = val
            
            # 波轮 (这里就是刚才缺少的代码)
            elif code == "ABS_Z": state['LT'] = val  # 左波轮
            elif code == "ABS_RZ": state['RT'] = val # 右波轮
            
            update_gamepad()

        # === 处理按键 (Event 3) ===
        elif "event3" in device:
            is_down = (value_hex != "00000000" and value_hex != "UP")
            
            # 这里定义按键映射，你可以自己改
            if code == "KEY_F1":   # 映射为 A 键
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            
            elif code == "KEY_F2": # 映射为 B 键
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            
            elif code == "KEY_F3": # 映射为 X 键
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

            elif code == "KEY_F4": # 映射为 Y 键
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

            elif code == "KEY_F5": # 映射为 LB (左肩键/L1)
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

            elif code == "KEY_F6": # 映射为 RB (右肩键/R1)
                if is_down: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                else:       gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            
            # 如果你想把某个键改成 R3 (右摇杆下压)，把上面某一段改成:
            # gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            
            gamepad.update()
            
            # 调试显示：按下未知的键时会显示代码
            if is_down:
                print(f"检测到按键: {code}")

except KeyboardInterrupt:
    print("\n已停止")
    process.terminate()
