# PromptCrafter

PromptCrafter 是一个跨平台的 Prompt 生成器原型，旨在通过解析模板占位符、调用 OpenAI 大模型生成动态参数，并将结果组合为完整的提示词内容，帮助开发者快速构建可复用的 Prompt 工作流。

## 项目结构
```
PromptCrafter/
├── main.py               # 项目入口，后续接入命令行启动流程
├── config.yaml           # 示例配置，包含模型参数与输出设置
├── prompts/
│   └── template.txt      # Prompt 模板示例，展示占位符写法
├── output/
│   └── result.txt        # 输出占位文件，待生成结果写入
├── generator.py          # 核心生成逻辑模块，将处理模板与模型交互
├── scheduler.py          # 定时调度模块，预留定时任务功能
├── utils/
│   └── io_helper.py      # I/O 工具模块，封装文件读写能力
├── requirements.txt      # 依赖占位文件，后续添加所需库
└── README.md             # 项目说明文档
```

## 运行平台
- ✅ Windows
- ✅ Linux

## 环境准备
- 运行项目前请确保安装 [PyYAML](https://pyyaml.org/)，可使用 `pip install pyyaml` 进行安装。

## 后续功能预告
- ⏱️ 支持定时任务调度，自动批量生成 Prompt。
- 🤖 集成 OpenAI API，实现模板参数的智能填充。
- 💾 完善文件管理与缓存策略，支持更多输出格式。
