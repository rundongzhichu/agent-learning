# Claude Code 特性与使用指南

本指南旨在全面总结Claude Code的核心特性、使用技巧、最佳实践和官方示例，为开发者提供一份直观易懂的参考文档。

## 一、 核心特性

Claude Code 是一个由 AI 驱动的代理式编码助手，它能够深度理解您的整个代码库，并通过自主的“收集上下文 -> 采取行动 -> 
验证结果”循环来完成复杂的开发任务。其核心能力超越了传统的聊天机器人或内联代码补全工具。

### 1.1 代理式工作流 (Agentic Workflow)

与简单的问答不同，Claude Code 是一个**代理 (Agent)**。这意味着它可以主动执行操作，而不仅仅是被动地回应问题。其工作流程是一个持续的循环：

1.  **收集上下文**: 使用内置工具读取文件、搜索代码、运行命令以理解当前状态。

2.  **采取行动**: 基于理解，规划并执行操作，如编辑代码、创建新文件、运行测试等。

3.  **验证结果**: 执行后检查结果（例如，重新运行测试），根据反馈调整下一步行动。

这个循环会一直持续，直到任务完成。您可以在任何时刻中断并引导它，使其成为一个协作式的开发伙伴。

### 1.2 多环境与多界面支持

Claude Code 可以在多种环境中运行，每种环境都连接到同一个底层引擎，确保体验一致：

*   **本地终端 (CLI)**: 直接在终端中使用，功能最完整，适合喜欢命令行的用户。
*   **桌面应用 (Desktop App)**: 提供图形化界面，支持可视化差异审查、实时应用预览和计划任务。
*   **IDE 插件 (VS Code, JetBrains)**: 深度集成到主流 IDE 中，支持 `@-提及` 文件、查看内联差异等。
*   **网页版 (Web)**: 在浏览器中运行，无需本地安装，适合快速处理或在移动设备上继续工作。

### 1.3 内置工具集

Claude Code 的强大之处在于其丰富的内置工具，这些工具是其实现自动化能力的基础：

*   **文件操作**: 读取、编辑、创建、重命名文件。
*   **搜索**: 按模式查找文件、使用正则表达式搜索内容。
*   **执行**: 运行 shell 命令、启动服务器、运行测试套件、使用 git。
*   **网络访问**: 搜索网络、获取在线文档、查找错误信息。
*   **代码智能**: （需插件）实现“转到定义”、“查找引用”等功能。

### 1.4 扩展性与自定义

Claude Code 提供了强大的扩展机制，允许您对其进行深度定制：

*   **CLAUDE.md**: 项目根目录下的特殊文件，用于存储持久性的项目约定、编码标准、构建命令等。它在每个会话开始时被自动加载，是指导 Claude 行为的最重要文件。
*   **Skills (技能)**: 可重用的知识包和工作流。您可以创建自定义的 `/slash-command`，如 `/deploy` 或 `/review-pr`。Skills 可以包含详细的操作手册，让 Claude 自主编排复杂任务。
*   **Model Context Protocol (MCP)**: 一个开放标准，用于将 Claude 连接到外部服务（如 Jira, Slack, 数据库）。这使得 Claude 能够查询数据库、更新工单、发布消息，从而融入您的整个工作流。
*   **Subagents (子代理)**: 专门的 AI 助手，可以独立运行以处理特定任务（如代码审查、调试），并将结果汇总报告给主代理。这有助于隔离上下文，避免主对话窗口过快填满。

## 二、 使用技巧与最佳实践

为了最大化 Claude Code 的效能，遵循以下最佳实践至关重要。

### 2.1 提供明确的验证标准

这是提高 Claude 工作质量的最高杠杆动作。不要只说“修复这个 bug”，而是提供具体的成功标准，让 Claude 可以自行验证：

*   **对于代码实现**: “编写一个 `validateEmail` 函数。示例测试用例：[email protected] 为真，invalid 为假，[email protected] 为假。实现后运行测试。”
*   **对于 UI 更改**: “[粘贴设计图截图] 实现此设计。对结果进行截图并与原始设计进行比较。列出差异并修复它们。”
*   **对于错误修复**: “构建失败，出现此错误：[粘贴错误日志]。修复它并验证构建成功。解决根本原因，不要抑制错误。”


### 2.2 先探索，再规划，最后编码 (Explore, Plan, then Code)

对于不熟悉或复杂的任务，直接跳到编码可能会导致解决错误的问题。推荐使用 **Plan Mode** 将研究和执行分离：

1.  **探索 (Explore)**: 进入 Plan Mode (`Shift+Tab`)，让 Claude 读取相关文件，回答关于架构和代码逻辑的问题，不进行任何更改。
2.  **规划 (Plan)**: 要求 Claude 创建一个详细的实施计划。您可以按 `Ctrl+G` 在编辑器中打开该计划并直接修改。
3.  **实现 (Implement)**: 切换回正常模式，让 Claude 根据批准的计划进行编码和验证。

### 2.3 在提示中提供具体上下文

指令越精确，需要的返工就越少。善用以下方法：

*   **使用 `@` 引用文件**: 不要描述文件位置，直接使用 `@src/auth/login.ts` 让 Claude 立即读取。
*   **指向来源**: “查看 `ExecutionFactory` 的 git 历史并总结其 API 是如何形成的”。
*   **参考现有模式**: “查看主页上 `HotDogWidget.php` 的实现方式。按照相同的模式实现一个新的日志小部件。”
*   **描述症状**: “用户报告登录失败。检查 `src/auth/` 中的身份验证流程，特别是 token 刷新。编写一个失败的测试来重现问题，然后修复它。”

### 2.4 编写有效的 CLAUDE.md

`CLAUDE.md` 是项目的灵魂，但应保持简洁。目标是 200 行以内。遵循 KISS 原则：

*   **✅ 应包括**: 无法从代码推断的 Bash 命令、与默认值不同的代码风格、测试指令、仓库礼仪（分支命名）、特定于项目的架构决策。
*   **❌ 应排除**: Claude 可以通过读取代码弄清楚的内容、标准语言约定、详细的 API 文档（应链接）、长篇大论的教程、自明的实践（如“编写干净的代码”）。

定期审查此文件，确保其精简有效，因为过长的 `CLAUDE.md` 会导致 Claude 忽视关键指令。

## 三、 官方示例与工作流程

### 3.1 常见工作流程示例

以下是利用 Claude Code 解决日常开发任务的典型场景：

#### 3.1.1 理解新的代码库

```bash
# 启动会话
claude

# 获取概览
give me an overview of this codebase

# 探索特定组件
how is authentication handled?
what are the key data models?
```

#### 3.1.2 修复错误

```bash
# 分享错误信息
I'm seeing an error when I run npm test

# 请求修复建议
suggest a few ways to fix the @ts-ignore in user.ts

# 应用修复
update user.ts to add the null check you suggested
```

#### 3.1.3 创建拉取请求 (Pull Request)

```bash
# 总结更改
summarize the changes I've made to the authentication module

# 创建 PR
craete a pr

# 增强描述
enhance the PR description with more context about the security improvements
```

### 3.2 捆绑 Skills 示例

Claude Code 自带了一些非常实用的捆绑技能 (Bundled Skills)：

*   **`/batch <instruction>`**: 并行编排大规模变更。例如 `/batch migrate src/ from Solid to React`，它会将工作分解为多个单元，分别处理并创建 PR。
*   **`/simplify [focus]`**: 审查最近更改的文件，寻找代码重用、质量和效率问题，并自动修复。
*   **`/debug [description]`**: 通过读取会话日志来排查当前会话中的问题。
*   **`/loop [interval] <prompt>`**: 按指定间隔重复运行某个提示，例如 `/loop 5m check if the deploy finished`。

### 3.3 CLI 使用示例

```bash
# 在管道中使用，例如监控日志
$ tail -f app.log | claude -p "Slack me if you see any anomalies"

# 在 CI 中自动化翻译
$ claude -p "translate new strings into French and raise a PR for review"

# 对一组文件批量进行安全审查
$ git diff main --name-only | claude -p "review these changed files for security issues"

# 从远程会话恢复
$ claude --teleport
```


## Claude模型系列

**Claude** 的模型系列：**Opus、Sonnet、Haiku**。  
这是 Anthropic 给不同能力等级的 Claude 模型起的名字，对应三种定位：

---

### 🧠 Opus（“杰作”）
- **最强大**、最聪明的模型
- 擅长复杂推理、高难度任务、长上下文深度理解
- 成本最高，速度相对较慢
- 适合：科研分析、复杂代码、高级决策等

### 📘 Sonnet（“十四行诗”）
- **平衡型**，能力与速度/成本的折中
- 大多数日常专业任务的首选
- 适合：代码编写、内容创作、数据分析、客服等

### 🍃 Haiku（“俳句”）
- **最快、最轻量**，响应速度极快
- 成本最低，适合高频调用
- 适合：实时对话、分类、简单问答、边缘场景

---

### 简单类比
如果把模型比作人：
- **Opus** = 资深专家  
- **Sonnet** = 经验丰富的工程师  
- **Haiku** = 反应敏捷的助理  

这些名字来自不同体裁的诗歌，用来暗示模型在“理解与生成语言”上的不同风格。