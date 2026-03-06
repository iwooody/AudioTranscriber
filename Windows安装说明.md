# AudioTranscriber Windows 安装指南

## ⚠️ 重要提示

你看到错误是因为：**Python没有安装**

## 🚀 方案一：安装Python后运行（推荐）

### 步骤1：下载Python
打开链接下载Python 3.10：
```
https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
```

### 步骤2：安装Python
1. 双击下载的 `python-3.10.11-amd64.exe`
2. **重要**：勾选 ☑️ **"Add Python to PATH"**
3. 点击 **"Install Now"**
4. 等待安装完成

### 步骤3：运行程序
1. 回到 AudioTranscriber 文件夹
2. 双击 `安装并运行.bat`
3. 等待自动安装依赖（约5分钟）
4. 程序自动启动

---

## 🚀 方案二：使用WinPython（无需安装Python）

如果你不想安装Python，可以用WinPython（绿色版）：

### 步骤1：下载WinPython
```
https://github.com/winpython/winpython/releases/download/6.4.20230625final/Winpython64-3.10.11.1.exe
```

### 步骤2：解压WinPython
1. 双击下载的文件
2. 解压到任意位置（如 `D:\WinPython`）

### 步骤3：运行程序
1. 打开解压后的 WinPython 文件夹
2. 双击 `WinPython Command Prompt.exe`
3. 在弹出的命令行中输入：
   ```cmd
   cd D:\AudioTranscriber
   pip install -r requirements.txt
   python src/main.py
   ```

---

## 🚀 方案三：使用Anaconda（适合数据科学用户）

如果你已有Anaconda：

```cmd
conda create -n audio python=3.10
conda activate audio
pip install -r requirements.txt
python src/main.py
```

---

## 📋 requirements.txt 内容

```
PyQt6==6.6.1
pyinstaller==6.3.0
librosa==0.10.1
soundfile==0.12.1
openai-whisper==20231117
torch==2.1.2
torchaudio==2.1.2
pyannote.audio==3.1.1
keybert==0.8.3
transformers==4.36.2
sentence-transformers==2.2.2
numpy==1.26.3
pandas==2.1.4
tqdm==4.66.1
python-docx==1.1.0
jieba
```

---

## ❓ 常见问题

### Q: 安装Python时忘记勾选"Add to PATH"怎么办？
**A:** 重新运行Python安装程序，选择"Modify"，然后勾选"Add to PATH"

### Q: pip install 很慢怎么办？
**A:** 使用清华镜像源：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 提示"Microsoft Visual C++ 14.0 is required"
**A:** 下载安装 Visual C++ Build Tools：
```
https://aka.ms/vs/17/release/vs_BuildTools.exe
```

---

**推荐：使用方案一，最简单直接！**
