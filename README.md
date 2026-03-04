# AudioTranscriber - 离线录音转写工具

## 📦 项目结构

```
AudioTranscriber/
├── src/                          # 源代码
│   ├── main.py                   # 程序入口
│   ├── core/                     # 核心处理模块
│   │   ├── whisper_service.py    # 语音识别
│   │   ├── speaker_diarization.py # 说话人分离
│   │   ├── nlp_summary.py        # NLP摘要分析
│   │   └── pipeline.py           # 处理流水线
│   ├── ui/                       # 界面模块
│   │   └── main_window.py        # 主窗口
│   └── utils/                    # 工具模块
│       ├── config.py             # 配置文件
│       └── database.py           # 数据库操作
├── models/                       # AI模型存放（运行后生成）
├── data/                         # 用户数据（运行后生成）
│   ├── recordings/               # 音频文件
│   └── transcriber.db            # SQLite数据库
├── resources/                    # 资源文件
├── requirements.txt              # Python依赖
├── AudioTranscriber.spec         # PyInstaller打包配置
├── 启动.bat                      # Windows启动脚本
└── README.md                     # 说明文档
```

## 🚀 快速开始

### 方式1：直接运行Python

1. **安装Python 3.10+**
   - 从 https://www.python.org/downloads/ 下载安装
   - 安装时勾选 "Add Python to PATH"

2. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```cmd
   python src/main.py
   ```
   或双击 `启动.bat`

### 方式2：打包成EXE

1. **安装PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **打包**
   ```cmd
   pyinstaller AudioTranscriber.spec
   ```

3. **获取EXE**
   - 打包完成后在 `dist/AudioTranscriber/` 目录下
   - 双击 `AudioTranscriber.exe` 运行

## 📋 功能说明

### 1. 上传音频文件
- 支持格式：MP3, WAV, M4A, FLAC, OGG, AAC, WMA
- 支持时长：最长3小时
- 支持语言：中文、英文、日文、自动检测

### 2. 语音识别
- 本地运行，无需联网
- 基于OpenAI Whisper模型
- 自动断句，精确时间戳

### 3. 说话人分离
- 自动识别不同说话人
- 显示为 [说话人1] [说话人2]
- **支持重命名**：右键点击名称可修改为 [张三] [李四]

### 4. 智能分析
- **关键词提取**：自动提取会议关键词
- **待办事项**：识别"需要"、"安排"等关键词
- **情感分析**：统计积极/消极情绪
- **自动摘要**：生成会议摘要

### 5. 标记与收藏
- 双击段落可标记 ⭐ 收藏
- 添加笔记注释
- 支持仅导出收藏的内容

### 6. 导出功能
- **导出TXT**：纯文本格式，带时间戳
- **导出Word**：Word文档格式
- **导出收藏**：仅导出标记的内容

## ⚙️ 配置说明

### 模型选择
| 模型 | 大小 | 速度 | 准确率 |
|-----|------|------|--------|
| tiny | 39MB | 最快 | 一般 |
| base | 74MB | 快 | 良好 |
| small | 244MB | 中等 | 优秀 |

**建议**：普通会议用 base，重要会议用 small

### 首次运行
程序会自动下载AI模型到 `models/` 目录：
- Whisper模型：约 74MB (base)
- 总计约 100MB

如果自动下载失败，可手动下载放置到 models 目录。

## 🖥️ 界面截图

```
┌─────────────────────────────────────────────────────────────┐
│  AudioTranscriber v1.0.0                     [上传音频文件] │
├──────────────┬──────────────────────────────────────────────┤
│  📁 录音文件  │  语言: [中文▼]  模型: [base▼]               │
│              │  [导出TXT] [导出Word] [导出收藏]              │
│  ▶ 会议.m4a  │                                              │
│    已完成 ✓  │  转写结果                                     │
│              │  ─────────────────────────────────────────  │
│  ▶ 采访.m4a  │  [00:00:15] [张三] 大家好，今天...          │
│    处理中 ⏳ │  [00:01:30] [李四] 我觉得这个...            │
│              │  [00:02:45] [张三] 那我们就这样决定了 ⭐    │
│              │                                              │
├──────────────┴──────────────────────────────────────────────┤
│  🏷️ 关键词: 会议、预算、方案  │  ✅ 待办: 3项                │
└─────────────────────────────────────────────────────────────┘
```

## 📁 数据存储

- **音频文件**：`data/recordings/`
- **转写数据**：`data/transcriber.db` (SQLite)
- **AI模型**：`models/`

## 🔒 隐私说明

- ✅ 完全离线运行，不连接互联网
- ✅ 音频文件本地存储
- ✅ 不收集任何用户数据
- ✅ 支持处理敏感会议内容

## 🐛 常见问题

### 1. 启动失败，提示缺少DLL
- 安装 Visual C++ Redistributable
- 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe

### 2. 模型下载失败
- 检查网络连接
- 手动下载模型放置到 models/ 目录

### 3. 处理长音频内存不足
- 使用 base 或 tiny 模型
- 关闭其他占用内存的程序

### 4. 说话人识别不准确
- 确保音频质量良好
- 使用 small 模型提高准确率
- 说话人之间有明显停顿效果更好

## 📜 开源协议

本项目使用以下开源组件：
- OpenAI Whisper (MIT License)
- PyQt6 (GPL v3)
- PyTorch (BSD License)

## 📧 技术支持

如有问题，请提交 Issue 或联系开发者。

---

**版本**: v1.0.0  
**更新日期**: 2024-03-04
