# WorkBuddy 开发对话上下文

## 项目名称
麦麦精算师 (McActuary)

## 开发工具
WorkBuddy AI

## 对话上下文摘要

### 阶段 1：需求分析

用户提供了麦当劳程序员创意开发大赛的比赛链接（https://github.com/M-China/mcd-developer-innovation-challenge），询问参赛创意方案。

WorkBuddy 分析了以下内容：
1. 比赛 README.md — 比赛规则、时间线、参与方式
2. activityGuidelines.md — 详细活动规则、排名依据（GitHub Star 数）、奖品信息
3. mcd-mcp-server README.md — 麦当劳 MCP Server 的 33 个可用工具

提出了 5 个创意方案，按创意独特性、实用价值、Star 吸引力综合排序：
- 方案一：麦麦减脂搭子（营养+点餐）
- 方案二：麦门薅羊毛大师（优惠券+最低价下单）
- 方案三：麦麦年度报告（消费可视化报告）
- 方案四：麦麦派对一键预约（主题活动全流程）
- 方案五：麦麦积分投资顾问（积分管理+抽奖决策）

### 阶段 2：方案组合

用户提出将方案二（省钱薅羊毛）和方案五（积分投资）组合。

WorkBuddy 确认可行性并设计了组合方案「麦麦精算师 (McActuary)」：
- 核心理念：把麦当劳数字资产当作"投资组合"管理
- 优惠券 = 现金等价物
- 积分 = 投资资本
- 抽奖 = 高风险投资
- 创新增量：跨模块"价值决策引擎" — 单独哪个方案都做不了的多方案对比

使用架构图展示了三大模块 + 决策引擎 + 报告输出的组合架构。

### 阶段 3：开发实现

WorkBuddy 在对话中完成了以下开发工作：

1. **SKILL.md** — 核心 Skill 定义文件（WorkBuddy 指令文件 = 项目源代码）
   - 定义了四大模块的完整工作流程
   - 详细描述了 18 个 MCP 工具的调用顺序和决策逻辑
   - 包含跨模块"价值决策引擎"的推荐规则
   - 包含用户对话示例和使用指南

2. **src/calculator.py** — 辅助算法模块
   - 优惠券组合优化器（Coupon Combination Optimizer）：遍历优惠券子集，调用 calculate-price 找最优组合
   - 抽奖期望值计算器（Lottery EV Calculator）：EV = Σ(Prize × P) - Cost
   - 积分性价比排行器（Points Value Ranker）：按 value/point 排序，星级评价
   - 跨模块决策引擎（Cross-Module Decision Engine）：综合优惠券、积分、抽奖给出推荐

3. **README.md** — 完整项目文档
   - 项目简介、核心功能、安装步骤、使用示例
   - 目标用户、技术架构、项目结构
   - MCP 工具覆盖统计（18/33 = 55%）

4. **MCP_INTEGRATION.md** — MCP 集成文档
   - 18 个工具的逐一说明（调用时机、输入输出、业务价值）
   - 三个核心调用流程图
   - 业务价值总结

5. **mcp-config.example.json** — 脱敏配置示例
6. **CONTEST_DECLARATION.md** — 官方参赛声明（不可修改）

### MCP 工具使用记录

开发过程中实际调用的 MCP 相关信息：
- MCP Server: mcd-mcp (https://mcp.mcd.cn)
- 协议: Streamable HTTP
- 使用工具数: 18 个（覆盖 55%）
- 涉及场景: 优惠券、点餐、积分商城、抽奖、历史订单、营养信息

## 开发环境

- 工具: WorkBuddy AI
- Python: 3.13.12 (managed)
- 验证: calculator.py demo 运行通过

## 备注

本项目使用 WorkBuddy AI 进行创意构思、方案设计、代码编写和文档生成。WorkBuddy 的 AI 对话能力贯穿了从需求分析到代码实现的完整流程。
