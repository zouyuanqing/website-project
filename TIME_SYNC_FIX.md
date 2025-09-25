# Windows 时间同步修复脚本

## 方法1：手动同步时间（推荐）

### 步骤1：以管理员身份运行PowerShell
1. 右键点击"开始"按钮
2. 选择"Windows PowerShell (管理员)"
3. 在UAC提示中点击"是"

### 步骤2：启动时间服务并同步
```powershell
# 启动Windows时间服务
Start-Service w32time

# 强制立即同步时间
w32tm /resync /force

# 检查同步状态
w32tm /query /status
```

### 步骤3：设置时间服务器（如果需要）
```powershell
# 配置时间服务器为中国国家授时中心
w32tm /config /manualpeerlist:"ntp.ntsc.ac.cn,0x1" /syncfromflags:manual

# 重启时间服务
Restart-Service w32time

# 再次强制同步
w32tm /resync /force
```

## 方法2：通过设置界面同步

### 步骤1：打开时间设置
1. 右键点击任务栏右下角的时间
2. 选择"调整日期/时间"
3. 或者打开"设置" > "时间和语言" > "日期和时间"

### 步骤2：启用自动同步
1. 确保"自动设置时间"开关是开启的
2. 点击"立即同步"按钮
3. 如果需要，可以更改时间服务器

## 验证修复结果

修复完成后，运行以下命令验证：

```powershell
# 检查当前时间
Get-Date

# 检查时间服务状态
Get-Service w32time

# 检查时间同步状态
w32tm /query /status
```

## 常见时间服务器

如果默认服务器同步有问题，可以尝试以下服务器：

- 中国国家授时中心：`ntp.ntsc.ac.cn`
- 阿里云NTP：`ntp.aliyun.com`
- 腾讯NTP：`ntp.tencent.com`
- 百度NTP：`ntp.baidu.com`
- Windows默认：`time.windows.com`

## 预期结果

修复后，系统时间应该显示正确的当前时间（北京时间），例如：
- 正确时间：2025-01-20 17:xx:xx（根据实际当前时间）
- 而不是：2025-09-21 01:xx:xx

修复系统时间后，我们的应用时间显示也会自动变正确！