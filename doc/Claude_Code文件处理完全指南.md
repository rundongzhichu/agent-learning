# Claude Code 文件处理完全指南

## 目录
1. [核心特性概览](#核心特性概览)
2. [内置工具系统详解](#内置工具系统详解)
3. [文件操作实战技巧](#文件操作实战技巧)
4. [高级功能与最佳实践](#高级功能与最佳实践)
5. [性能优化与成本控制](#性能优化与成本控制)

---

## 核心特性概览

### 🎯 革命性突破：全文件系统原生访问

Claude Code 与传统 AI 助手的本质区别：

| 传统 Claude | Claude Code |
|------------|-------------|
| ❌ 手动上传单个/少量文件 | ✅ 全文件系统授权访问 |
| ❌ 有上传大小限制 | ✅ 无文件大小限制 |
| ❌ 有文件数量限制 | ✅ 无文件数量限制 |
| ❌ 格式支持有限 | ✅ 支持任意格式 |
| ❌ 只能读取内容 | ✅ 可读/写/编辑/整理 |

**核心价值**：
- **工程师场景**：几分钟内遍历并处理整个项目的上万个代码文件，批量重构、统一规范、生成文档、扫描漏洞
- **产品经理场景**：一键读取整个季度的客户访谈录音转写、用户反馈文档、竞品分析报告，自动提取需求、生成结构化需求池

---

## 内置工具系统详解

### 工具分类与使用场景

Claude Code 与外部世界交互的**唯一通道**是工具调用（Tool Use）。模型本身不能直接操作文件系统或执行命令，所有操作都必须通过工具完成。

#### 1️⃣ 文件读写工具

##### **Read** - 读取文件内容
```bash
# 基础用法
读取 src/components/Button.tsx 的内容

# 支持的文件类型
- 代码文件：.py, .ts, .js, .java, .go 等
- 配置文件：.json, .yaml, .toml, .xml
- 文档文件：.md, .txt, .pdf
- 图片文件：.png, .jpg, .webp（自动分析内容）
- Jupyter Notebook：.ipynb

# 实战示例
> 帮我查看 package.json 中的依赖配置
> 阅读 README.md 并总结项目结构
> 分析这张 UI 设计截图的布局特点
```

**技术细节**：
- 支持 PDF 理解能力（基础版）
- 限制：每请求最大 32 MB，最多 100 页
- 自动检测文件编码
- 智能识别文件类型并采用合适的解析策略

##### **Write** - 创建新文件或完整覆写
```bash
# 创建新文件
请在当前目录创建一个 index.html 文件

# 完整覆写
用新的实现替换整个 utils/format.ts 文件

# 实战示例
> 创建一个 React 组件文件 Button.tsx，包含以下功能...
> 在项目根目录生成 .gitignore 文件，针对 Node.js 项目
> 把分析结果写入 docs/analysis-report.md
```

**最佳实践**：
- 适用于创建全新文件或完全重写现有文件
- 对于部分修改，优先使用 `Edit` 工具更精确
- Write 操作会自动创建不存在的目录

##### **Edit** - 精准编辑文件的指定部分
```bash
# 基于字符串匹配替换
帮我把 utils/format.ts 里的日期格式从 YYYY-MM-DD 改成 DD/MM/YYYY

# 实际执行流程
1. Read (读取文件) → 
2. Edit (定位并替换格式字符串) → 
3. Bash (运行 pnpm test 确认测试通过)
整个过程在几秒内完成

# 实战示例
> 将 calculateTotal 函数的返回值乘以 1.1（添加 10% 的服务费）
> 把所有的 console.log 替换为 logger.info
> 更新 import 语句，从 'lodash' 改为 'lodash-es'
```

**技术优势**：
- 基于 AST（抽象语法树）精准定位
- 保持代码格式和注释不变
- 支持跨多行的复杂修改
- 自动检测潜在的冲突和风险

##### **MultiEdit** - 同时进行多次编辑
```bash
# 适用场景
- 需要在多个文件中修改相同的模式
- 一次性重构多个相关函数
- 批量更新配置项

# 实战示例
> 把所有组件中的 PropTypes 迁移到 TypeScript 类型定义
> 同时更新前端和后端的 API 端点路径
> 批量重命名变量：user_id → userId（跨 5 个文件）
```

**效率对比**：
- 单次 MultiEdit vs 多次单独 Edit：**节省 60-80% 时间**
- 减少上下文切换开销
- 保证多处修改的一致性

---

#### 2️⃣ 文件搜索工具

##### **Glob** - 按文件名模式匹配搜索
```bash
# 基础语法
查找所有 .tsx 文件
找到所有的配置文件（*.config.js）

# 高级模式
src/components/**/*.tsx          # 递归查找 tsx 文件
*.{test,spec}.ts                 # 匹配测试文件
.{env,.gitignore}                # 匹配多个特定文件名

# 实战示例
> 找出项目中所有的 TypeScript 接口定义文件（*.d.ts）
> 定位到所有的 Jest 测试配置文件
> 查找 docs 目录下所有的 Markdown 文档
```

**性能特点**：
- 基于 glob pattern 快速匹配
- 自动忽略 node_modules、.git 等排除目录
- 支持通配符和正则表达式组合

##### **Grep** - 基于正则表达式搜索文件内容
```bash
# 基础搜索
搜索所有包含 "authentication" 的文件
找到 handleUserLogin 函数的定义位置

# 正则表达式
function\s+\w+Async\b            # 查找所有异步函数
import.*from\s+['"]react['"]     # 查找 React 导入
console\.(log|error|warn)        # 查找控制台输出

# 实战示例
> 找出所有使用了 deprecated API 的地方
> 追踪 user 变量在整个代码库中的引用
> 查找所有 TODO 和 FIXME 注释
> 定位到所有发送 HTTP POST 请求的代码
```

**高级技巧**：
- 支持 PCRE（Perl 兼容正则表达式）
- 可指定文件类型过滤：`*.ts:searchPattern`
- 显示行号和上下文（默认前后各 2 行）
- 区分大小写选项

##### **LS** - 列出文件和目录
```bash
# 目录浏览
列出当前目录的所有文件
显示 src/components 下的结构

# 递归查看
以树形结构展示项目目录

# 实战示例
> 查看项目根目录有哪些主要文件夹
> 列出 tests 目录下所有的测试文件
> 显示 config 目录的完整结构
```

---

#### 3️⃣ 代码理解与分析工具

##### **Think** - 模型内部推理
```bash
# 不产生外部操作的纯思考
# 用于复杂逻辑规划、多方案权衡

# 触发场景
> 分析一下这个微服务架构的优缺点
> 对比一下使用 Redux 和 Zustand 的方案选择
> 评估这次重构可能带来的风险点
```

**价值**：
- 在执行高风险操作前先进行深度推理
- 生成多套方案并权衡利弊
- 避免盲目行动导致的破坏

##### **Agent** - 启动子代理处理子任务
```bash
# 并行处理独立任务
# 隔离上下文，避免污染主会话

# 实战示例
> 启动一个子代理来专门处理前端的样式优化
> 让子代理去调研第三方库的集成方案
> 委托子代理审查测试覆盖率报告
```

**适用场景**：
- 需要同时处理多个独立模块
- 避免不同任务的上下文相互干扰
- 长时间运行的后台任务

---

#### 4️⃣ 网络与外部集成工具

##### **WebSearch** - 搜索互联网
```bash
# 获取最新信息
查询 React 19 的最新特性
搜索 Next.js 15 的 breaking changes

# 实战示例
> 查找 Express.js 安全最佳实践（2026 年最新版）
> 搜索 Stripe API 最新的支付集成文档
> 找出解决 "TypeError: Cannot read property" 的 StackOverflow 方案
```

##### **WebFetch** - 获取指定 URL 内容
```bash
# 读取在线文档
获取 https://react.dev/reference/react 的内容
下载 https://example.com/api-schema.json

# 实战示例
> 从 GitHub 仓库拉取最新的配置模板
> 读取在线 API 文档并生成本地缓存
> 抓取竞品网站的功能列表做对比分析
```

---

#### 5️⃣ 任务管理工具

##### **TodoWrite** - 更新待办事项列表
```bash
# 创建任务清单
/ todo 实现用户认证功能
  - [ ] 设计数据库 schema
  - [ ] 实现 JWT token 生成
  - [ ] 添加 refresh token 逻辑
  - [ ] 编写单元测试
```

##### **TodoRead** - 读取待办事项
```bash
# 查看当前进度
/ todo show
```

**工作流整合**：
```bash
# 完整流程
1. 接收复杂任务 → TodoWrite 拆解步骤
2. 逐项执行 → 每完成一项打勾
3. 随时查看进度 → TodoRead
4. 任务完成 → 生成总结报告
```

---

## 文件操作实战技巧

### 技巧 1：智能文件发现与理解

#### 场景：快速理解陌生代码库

```bash
# 第一步：宏观了解项目结构
列出项目根目录的主要文件和文件夹，并解释每个的作用

# 第二步：识别技术栈
分析 package.json 和 tsconfig.json，总结这个项目使用的技术栈

# 第三步：找到核心业务逻辑
找出处理用户认证和授权的相关文件，并画出它们的调用关系图

# 第四步：理解数据流
追踪一个用户登录请求从前端到后端的完整数据流
```

**输出示例**：
```
📁 项目结构分析
├── src/
│   ├── controllers/    # 控制器层：处理 HTTP 请求
│   ├── services/       # 业务逻辑层：核心业务规则
│   ├── models/         # 数据模型层：数据库交互
│   └── middleware/     # 中间件：认证、日志等
├── tests/              # 单元测试和集成测试
├── docs/               # 项目文档
└── config/             # 配置文件

🔧 技术栈识别
- 运行时：Node.js 20 + TypeScript 5.3
- Web 框架：Express 4.18
- 数据库：PostgreSQL + Prisma ORM
- 认证：JWT + bcrypt
- 测试：Jest + Supertest

🔐 认证模块文件关系
user.controller.ts → auth.service.ts → jwt.util.ts → user.model.ts
```

---

### 技巧 2：批量文件操作与重构

#### 场景：大规模代码重构

```bash
# 任务：将所有 JavaScript 文件迁移到 TypeScript

# 步骤 1：评估工作量
统计项目中 .js 和 .jsx 文件的数量，列出来

# 步骤 2：制定迁移策略
基于文件依赖关系，给出一个合理的迁移顺序建议

# 步骤 3：渐进式迁移
先从 utils 目录开始，把每个 JS 文件转换为 TS 文件，添加类型注解

# 步骤 4：验证
运行 TypeScript 编译器，修复所有类型错误
```

**Claude Code 执行流程**：
```
1. Glob 查找所有 *.js 文件 → 发现 45 个
2. Read 读取关键文件理解结构
3. Think 分析依赖关系，制定迁移顺序
4. TodoWrite 创建迁移计划（分 5 批）
5. 循环执行：
   - Read(源文件) → 分析代码
   - Write(目标.ts 文件) → 添加类型
   - Bash(tsc --noEmit) → 检查类型
6. 完成后生成迁移报告
```

---

### 技巧 3：多文件格式转换

#### 场景：API 文档批量生成

```bash
# 任务：为所有 API 端点生成 OpenAPI 文档

# 指令
扫描 routes/ 目录下所有的路由文件，提取每个端点的：
- HTTP 方法
- URL 路径
- 请求参数
- 响应格式
然后生成符合 OpenAPI 3.0 规范的 YAML 文件
```

**自动化流程**：
```
1. Glob 查找 routes/**/*.ts
2. Grep 提取 router.get/post/put/delete 调用
3. Read 读取每个路由处理器，分析输入输出
4. Think 归纳出统一的 schema 结构
5. Write 生成 openapi.yaml
6. Bash 运行 swagger-cli validate 验证格式
```

---

### 技巧 4：智能错误诊断与修复

#### 场景：生产环境 Bug 紧急修复

```bash
# 提供错误日志
这是生产环境的错误日志：
TypeError: Cannot read property 'id' of undefined
    at UserService.getUserProfile (/app/services/user.service.ts:45)

# 指令
1. 定位到出错的文件和行号
2. 分析可能导致 undefined 的原因
3. 检查调用 getUserProfile 的所有地方
4. 给出修复方案并实施
5. 添加防御性代码避免类似问题
```

**诊断流程**：
```
1. Read user.service.ts:45 → 发现 `user.id`
2. Grep "getUserProfile(" → 找到 3 个调用点
3. Read 每个调用点 → 发现有一个没做 null 检查
4. Think 分析 → 可能是数据库查询返回 null
5. Edit 添加可选链和错误处理：`user?.id ?? throw Error`
6. Bash 运行相关测试验证修复
```

---

### 技巧 5：文件内容智能分析

#### 场景：日志文件分析

```bash
# 任务：分析生产日志找出性能瓶颈

# 指令
读取 logs/production-2026-03.log 文件（约 10 万行），找出：
1. 响应时间超过 1 秒的请求有哪些
2. 出现频率最高的错误类型
3. 每天的高峰时段
4. 可疑的异常模式
生成可视化报告
```

**分析方法**：
```
1. Read 分块读取大文件（避免内存溢出）
2. Bash 使用 awk/grep 预处理提取关键信息
3. Write Python 脚本进行统计分析
4. Bash 运行脚本生成图表
5. Write 生成分析报告 markdown
```

---

### 技巧 6：配置文件智能管理

#### 场景：多环境配置同步

```bash
# 任务：确保开发、测试、生产环境配置一致

# 指令
对比 .env.development、.env.test、.env.production 三个文件
找出缺失的配置项
识别出不一致的值
生成配置检查清单
```

**对比分析**：
```
1. Read 读取三个环境文件
2. Think 提取键值对并对比
3. 输出差异报告：
   ✅ 共有配置：DATABASE_URL, REDIS_HOST, API_KEY
   ⚠️  仅开发环境：DEBUG_MODE=true
   ❌ 生产环境缺失：FEATURE_FLAG_NEW_UI
   🔴 值不一致：LOG_LEVEL (dev: debug, prod: error)
```

---

## 高级功能与最佳实践

### 1. CLAUDE.md 文件：项目级知识库

#### 什么是 CLAUDE.md？

CLAUDE.md 是 Claude Code 的**项目记忆体**，存放在项目根目录，包含：
- 技术栈说明
- 代码规范
- 架构决策记录
- 关键规则
- 工作流触发器

#### 标准结构

```markdown
# 项目概述
这是一个基于 Next.js 15 + TypeScript 的电商平台

## 技术栈
- 前端：Next.js 15, React 19, Tailwind CSS
- 后端：Node.js 20, Express, PostgreSQL
- 部署：Vercel, Docker

## 代码规范
- 使用 ES2024 语法
- 所有函数必须有 JSDoc 注释
- 组件采用函数式编程风格
- 禁止使用 any 类型

## 关键规则
- 任何数据库修改必须先写 migration
- API 响应必须遵循 JSON:API 规范
- 不允许直接修改生产数据库

## 目录结构
/src
  /components  # 可复用 UI 组件
  /pages       # Next.js 页面
  /lib         # 工具函数
  /hooks       # 自定义 React Hooks
```

#### 使用技巧

**技巧 1：分层级 CLAUDE.md**
```bash
# 根目录 CLAUDE.md - 全局规则
# /src/components/CLAUDE.md - 组件特定规范
# /tests/CLAUDE.md - 测试编写规范
```

**技巧 2：让 Claude 自己更新**
```bash
> 根据我们刚才讨论的开发规范，更新 CLAUDE.md 添加新的代码审查 checklist
```

**技巧 3：工作流触发器**
```markdown
## 触发器
当提到"添加新功能"时，自动执行：
1. 检查是否有对应的测试
2. 确认是否符合目录结构规范
3. 验证是否更新了 API 文档
```

---

### 2. 斜杠命令系统：Agent 控制面板

#### 核心命令速查

```bash
# === 会话管理 ===
/clear          # 清除当前会话历史
/resume         # 恢复之前的会话
/compact        # 压缩上下文，保留关键信息

# === 模型与模式 ===
/model          # 切换模型（sonnet/opus/haiku）
/plan           # 进入计划模式（先规划再执行）
/act            # 从计划模式切换到执行模式

# === 项目与上下文 ===
/context        # 显示当前 token 用量和上下文信息
/init           # 初始化项目，生成 CLAUDE.md

# === 调试与信息 ===
/help           # 显示所有可用命令
/status         # 显示当前任务状态
/thinking       # 查看模型的思考过程

# === 扩展功能 ===
/mcp            # 显示 MCP 服务器状态
/skills         # 列出已安装的 Skills
/chrome         # 连接浏览器控制
```

#### 实战技巧

**技巧 1：立即运行 /init**
```bash
# 新项目第一件事
claude
/init

# 自动生成项目分析文档
```

**技巧 2：Shift+Tab 切换模式**
```bash
# 快速在 Plan Mode 和 Act Mode 之间切换
# Plan Mode：只给建议，不实际操作
# Act Mode：执行具体任务
```

**技巧 3：Escape 键中断**
```bash
# 单按 Escape：停止当前操作
# 双击 Escape：清除输入并回退
# 空行 + 双击 Escape：撤销上一步
```

**技巧 4：让自动压缩发挥作用**
```bash
# 长会话后
/context  # 查看 token 使用
# 如果接近限制，Claude 会自动压缩旧消息
```

---

### 3. 多 Agent 协作系统

#### Sub-Agent 使用场景

```bash
# 场景 1：并行处理独立任务
> 启动两个子代理，一个负责前端样式优化，一个负责后端 API 性能调优

# 场景 2：深度代码探索
> 让子代理深入分析第三方库的源码，总结使用注意事项

# 场景 3：代码审查
> 委托子代理审查这个 PR 的所有更改，给出详细报告
```

#### 任务依赖管理

```bash
# 任务可以相互依赖，存储在元数据中
/task create "实现用户认证"
  depends_on: ["数据库 schema 设计"]
  
# 多个子代理可以协同工作在同一任务列表
# 当一个会话更新任务状态时，所有会话都会收到通知
```

**存储位置**：
```
~/.claude/tasks/
├── project-a/
│   └── tasks.json
└── project-b/
    └── tasks.json
```

---

### 4. 扩展能力系统

#### MCP（Model Context Protocol）

MCP 允许 Claude 连接外部服务和数据源。

**安装示例**：
```bash
# 让 Claude 自己安装 MCP
/mcp install github      # GitHub 集成
/mcp install postgres    # 数据库连接
/mcp install playwright  # 浏览器控制
```

**应用场景**：
- 连接公司内部的 Wiki 系统
- 读取 Jira 任务信息
- 查询监控平台数据
- 操作 CI/CD 流水线

#### Skills（技能系统）

Skills 是自定义的工作流封装。

**创建 Skill**：
```bash
# 在 ~/.claude/skills/ 目录下创建
touch ~/claude/skills/refactor-component.sh
```

**Skill 示例**：
```bash
#!/bin/bash
# Skill: React 组件重构
# Description: 将 Class Component 转换为 Function Component with Hooks

# 自动执行的步骤
1. 读取 Class 组件
2. 提取 state 和 lifecycle methods
3. 转换为 useState/useEffect
4. 优化性能（useMemo/useCallback）
5. 运行测试验证
```

---

### 5. 安全机制与回滚

#### Checkpoint 系统

每次文件变更前自动创建检查点：

```bash
# 查看所有 checkpoint
/git log --oneline

# 回滚到某个版本
/git checkout <commit-hash>

# 或使用 /resume 恢复到会话的某个状态
/resume <session-id>
```

#### Git集成最佳实践

```bash
# 技巧 1：Git 是你的安全保障
# 每次大改动前先 commit
git add .
git commit -m "feat: before major refactoring"

# 技巧 2：小步快跑
# 每完成一个小功能就 commit
# 便于回滚和 code review

# 技巧 3：让 Claude 帮你写 commit message
> 根据 git diff，生成一个符合 Conventional Commits 规范的 commit message
```

#### 危险操作拦截

```bash
# 配置白名单
# 在 ~/.claude/config.json 中设置

{
  "dangerously_allow": [
    "npm install",
    "pnpm test",
    "git status"
  ],
  "block_commands": [
    "rm -rf",
    "DROP TABLE",
    "DELETE FROM"
  ]
}
```

---

## 性能优化与成本控制

### Token 计费模式

Claude Code 的 token 消耗 ≠ 普通聊天

**消耗特点**：
```
普通对话：输入 1k tokens → 输出 1k tokens = 2k tokens

Claude Code 任务：
1. 读取相关文件：50k tokens（上下文）
2. 多轮内部推理：100k tokens（思考过程）
3. 最终输出：5k tokens（修改结果）
总计：155k tokens
```

**典型任务消耗**：
- 简单修改：5k-20k tokens
- 中等功能：50k-150k tokens
- 复杂重构：200k-500k tokens

---

### 省钱技巧

#### 1. Prompt Caching（提示缓存）

Anthropic 官方支持，缓存命中部分**只收 1/10 价格**。

```bash
# Claude Code CLI 自动启用
# 同一文件被反复读取时，自动标记为可缓存

# 验证缓存效果
/context  # 查看 cached tokens 比例
```

#### 2. 善用 CLAUDE.md

```bash
# 在项目根目录放 CLAUDE.md
# 写清楚：
- 技术栈
- 代码规范
- 目录结构
- 常用命令

# 好处：
- 减少重复解释的 token
- 提高第一次回答的准确率
- 避免走弯路
```

#### 3. 选择合适的模型

```bash
# 简单任务 → Haiku（最便宜）
/model haiku
> 帮我格式化这个文件

# 中等复杂度 → Sonnet（性价比最高）
/model sonnet
> 实现一个用户登录功能

# 复杂架构设计 → Opus（最强大）
/model opus
> 设计一个微服务架构，包含服务发现、负载均衡、熔断机制
```

**价格对比**（每 1M tokens）：
- Haiku: $0.25 (输入) / $1.25 (输出)
- Sonnet: $3.00 (输入) / $15.00 (输出)
- Opus: $15.00 (输入) / $75.00 (输出)

#### 4. 懒加载上下文

```bash
# 不要一开始就加载所有文件
# 而是按需加载

❌ 坏做法：
> 读取整个 src 目录的所有文件，然后帮我优化

✅ 好做法：
> 先帮我看看 performance bottlenecks 在哪里
> （等 Claude 指出具体文件后再深入）
> 好的，现在读取你提到的这 3 个文件，详细分析
```

#### 5. 新鲜上下文胜过臃肿上下文

```bash
# 定期清理旧会话
/clear  # 开始新话题时清空历史

# 结束会话前持久化保存
> 把我们今天讨论的关键决策和代码片段总结到 docs/session-notes.md
```

#### 6. 提供验证命令

```bash
# 明确告诉 Claude 如何验证结果
> 修改完后运行 pnpm test 确认测试通过
> 用 Lighthouse 跑一下，确保性能分数不低于 90

# 避免因验证不充分导致的返工（浪费 token）
```

---

### 并发处理：同时运行多个实例

```bash
# 终端 1
cd project-frontend
claude
> 优化首页加载速度

# 终端 2
cd project-backend
claude
> 优化数据库查询性能

# 终端 3
cd project-mobile
claude
> 重构 RN 组件

# 每周产出 50-100 个 PR（Meta 工程师实践）
```

**效率提升**：
- 避免上下文切换成本
- 并行处理独立模块
- 充分利用 Claude 的多线程能力

---

### 监控 Token 使用

```bash
# 实时查看
/context

# 输出示例
当前会话 Token 使用:
- 输入：125,430 tokens
- 输出：18,250 tokens
- 缓存命中：45,200 tokens (节省 $0.45)
- 估算成本：$2.34
```

---

## 常见陷阱与解决方案

### 陷阱 1：指令过载

```bash
❌ 错误示范：
> 帮我重构整个项目，包括：
> 1. 把所有 JS 转 TS
> 2. 添加单元测试
> 3. 优化性能
> 4. 更新文档
> 5. 修复已知 bug
> 6. 部署到生产环境

✅ 正确做法：
> 我们先从第一步开始：把 utils 目录的 JS 文件转为 TS
> （完成后）
> 很好，现在继续处理 services 目录
```

**原则**：
- 一次只做一件事
- 复杂任务拆分成多个子任务
- 每完成一步验证结果

---

### 陷阱 2：缺乏验证

```bash
❌ 错误做法：
> 改完了吗？好的，谢谢

✅ 正确做法：
> 改完后请运行测试套件
> 用 linter 检查一下代码质量
> 在开发环境启动应用验证功能正常
```

---

### 陷阱 3：忽略 Git

```bash
❌ 危险行为：
直接让 Claude 修改生产代码，没有版本控制

✅ 安全实践：
1. 创建 feature branch
   git checkout -b feature/ai-refactoring
2. 每步修改后 commit
3. 运行测试
4. 推送到远程
5. 创建 PR 人工审查
```

---

### 陷阱 4：过度依赖

```bash
❌ 盲目信任：
Claude 生成的代码直接用，不审查

✅ 批判性使用：
- 审查关键逻辑
- 理解实现原理
- 评估安全风险
- 补充边界 case 测试
```

---

## 总结：六大核心工作流

### 1. Code Onboarding（快速上手）
```bash
> 花 3 分钟介绍这个代码库的架构
> 画出核心模块的依赖关系图
> 告诉我重要的脚本和命令
```

### 2. Bug Triage（Bug 分类修复）
```bash
> 这是 Issue 链接：[URL]
> 定位相关文件，写测试复现，生成修复补丁
> 确认测试通过后提交 PR
```

### 3. 大规模重构
```bash
> 我们要迁移到 TypeScript
> 制定分阶段计划，每阶段都可独立验证
> 逐文件修改，跑本地测试
> 更新类型定义直到零错误
```

### 4. 功能开发
```bash
> 需求：添加用户收藏功能
> 1. 设计数据库 schema
> 2. 实现 API 端点
> 3. 编写前端组件
> 4. 添加端到端测试
> 5. 更新文档
```

### 5. 代码审查
```bash
> 审查这个 PR 的所有更改
> 关注：代码质量、性能影响、安全隐患、测试覆盖
> 给出具体改进建议和评分
```

### 6. 数据分析
```bash
> 读取本季度所有用户反馈文档
> 提取高频痛点和需求
> 聚类分析，生成需求池优先级列表
> 输出结构化报告
```

---

## 参考资源

- **官方文档**: https://platform.claude.com/docs
- **GitHub 仓库**: https://github.com/anthropics/claude-code
- **社区教程**: https://waytoagi.feishu.cn/wiki/LJbiwATadi72LUklHpgcexeSnNh
- **最佳实践**: Meta Staff Engineer John Kim 的 50 个技巧

---

*文档版本：v1.0*  
*最后更新：2026 年 3 月*  
*基于 Claude Code v2.1.76 整理*
