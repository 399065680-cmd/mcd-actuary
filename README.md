# 麦麦精算师 (McActuary)

> 麦当劳资产管理顾问 — 一键领券省钱 + 积分投资决策 + 跨模块最优方案推荐

[![McDonald's MCP](https://img.shields.io/badge/McDonald's-MCP-d62828)](https://open.mcd.cn/mcp)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-534AB7)](https://www.workbuddy.cn)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 项目简介

「麦麦精算师」是一个基于麦当劳中国 MCP（Model Context Protocol）能力开发的 WorkBuddy Skill。

它把用户的麦当劳数字资产——**优惠券**（现金等价物）、**积分**（投资资本）、**抽奖机会**（高风险投资）——当作一个"投资组合"来管理，通过跨模块决策引擎，帮助用户在"用券买 vs 积分兑换 vs 抽奖搏一搏"之间做出最优选择。

### 为什么需要它？

大部分麦当劳用户只用了 MCP 能力的一小部分——要么只领券，要么只看积分。但优惠券和积分是交叉的：

> 你想吃一个巨无霸——
> - 用优惠券买，可能 25 元
> - 用积分兑换券，可能 0 元，但积分 3 天后过期
> - 抽奖搏一搏，万一中了呢？

**单独哪个方案都给不出最优解，麦麦精算师能。**

## 核心功能

### 模块一：省钱模块
- 一键领取所有可用优惠券
- 查询附近门店 + 门店可用优惠
- 智能匹配最优优惠券组合
- 最低价下单

### 模块二：积分投资模块
- 积分账户体检（余额、过期预警）
- 商城商品积分性价比排行
- 抽奖期望值（EV）分析
- 积分兑换 / 抽奖执行

### 模块三：价值决策引擎（跨模块创新）
- 同时计算"用券买""积分兑换""抽奖"三种方案
- 综合积分过期、优惠券折扣、抽奖 EV 给出最优推荐
- 这是本 Skill 区别于单一功能工具的核心创新点

### 模块四：消费报告模块
- 月度消费 + 省钱明细
- 积分收益率分析
- 下一步行动建议

## 安装

### 前置条件

1. 申请麦当劳 MCP Token：访问 https://open.mcd.cn/mcp
2. 安装 WorkBuddy：访问 https://www.workbuddy.cn

### 配置步骤

1. **配置麦当劳 MCP 连接器**

   打开 WorkBuddy -> 侧边栏「连接器」-> 右上角「自定义连接器」->「配置 MCP」

   填入以下 JSON（替换 `YOUR_MCP_TOKEN` 为你的实际 Token）：

   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": {
           "Authorization": "Bearer YOUR_MCP_TOKEN"
         }
       }
     }
   }
   ```

   点击「保存」，回到「自定义连接器」将 mcd-mcp「启用」。

2. **安装本 Skill**

   将本仓库的 `SKILL.md` 文件放入 WorkBuddy 用户级 Skills 目录：

   ```bash
   cp SKILL.md ~/.workbuddy-ai/skills/mcd-actuary/SKILL.md
   ```

   或在 WorkBuddy 中通过 Skill 管理界面导入。

3. **开始使用**

   在 WorkBuddy 对话框中直接输入需求即可，例如：
   - "帮我一键领券"
   - "我想吃巨无霸，怎么最划算"
   - "我的积分还有多少"

## 使用示例

### 示例 1：一键领券 + 省钱下单

```
用户：帮我领券，我想吃巨无霸套餐

麦麦精算师：
已为你领取 8 张优惠券，其中 2 张将在 3 天内过期。

附近门店：麦当劳(XX路店) - 距离 800m

巨无霸套餐最优方案：
  原价：¥39
  使用优惠券：巨无霸套餐立减10元券
  实付：¥29，省 ¥10

确认下单？
```

### 示例 2：跨模块价值决策

```
用户：我想吃巨无霸，怎么最划算？

麦麦精算师：
为你找到 3 种方案：

方案A（推荐）：积分兑换
  巨无霸兑换券 — 需 2000 积分
  你的积分余额：3500，其中 500 积分 3 天后过期
  积分性价比：★★★★☆

方案B：优惠券购买
  巨无霸套餐 — 原价 ¥39 → 用券后 ¥25，省 ¥14

方案C：抽奖
  消耗 500 积分/次，EV = ¥1.2（不划算）

建议：选择方案A，积分即将过期，兑换最划算。
```

### 示例 3：积分报告

```
用户：帮我看看这个月消费报告

麦麦精算师：
=== 麦麦精算师 月度报告 ===

本月消费：6 单，总计 ¥186
优惠券节省：¥52（使用 4 张券）
积分变动：+820 获取，-2000 兑换，余额 1500
即将过期：300 积分（5 天后）

行动建议：
1. 有 2 张优惠券即将过期，建议本周使用
2. 积分余额偏低，近期消费可累积
3. 当前抽奖 EV 为负，不建议抽奖
```

## 目标用户

- 麦当劳高频消费者（每周 2 次以上）
- 关注积分和优惠券价值最大化的人群
- 想用 AI 简化点餐决策的程序员和上班族
- 对"薅羊毛"有执念的价格敏感型用户

## 技术架构

```
用户对话
   |
   v
WorkBuddy AI (Skill 引擎)
   |
   +---> 省钱模块 (8 个 MCP Tools)
   +---> 积分投资模块 (9 个 MCP Tools)
   +---> 价值决策引擎 (跨模块编排)
   +---> 消费报告模块 (5 个 MCP Tools)
   +---> 营养信息辅助 (1 个 MCP Tool)
   |
   v
麦当劳 MCP Server (https://mcp.mcd.cn)
```

共使用 **18 个** 麦当劳 MCP 工具，覆盖 33 个可用工具的 55%。

详细 MCP 工具调用流程见 [MCP_INTEGRATION.md](MCP_INTEGRATION.md)。

## 项目结构

```
mcd-actuary/
├── SKILL.md                    # 核心 Skill 定义（WorkBuddy 指令文件 = 源代码）
├── README.md                   # 项目说明（本文件）
├── CONTEST_DECLARATION.md      # 参赛声明
├── MCP_INTEGRATION.md          # MCP 工具集成文档
├── mcp-config.example.json     # 脱敏 MCP 配置示例
├── workbuddy.md                # WorkBuddy 开发对话上下文
└── src/
    └── calculator.py           # 辅助算法：优惠券组合优化、抽奖 EV 计算、积分性价比排行
```

## MCP 工具覆盖

| 模块 | 工具数 | 工具列表 |
|------|--------|----------|
| 省钱模块 | 13 | auto-bind-coupons, available-coupons, query-my-coupons, query-store-coupons, query-nearby-stores, delivery-query-addresses, delivery-query-stores, query-meals, query-meal-detail, calculate-price, create-order, cancel-order, query-order |
| 积分投资 | 9 | query-my-account, mall-points-products, mall-product-detail, mall-create-order, query-lottery-info, draw-lottery, query-my-prizes, mall-order-list, mall-order-detail |
| 消费报告 | 5 | order-list, query-my-account, query-my-coupons, mall-order-list, now-time-info |
| 营养辅助 | 1 | list-nutrition-foods |
| **去重后** | **18** | |

## 竞赛信息

本项目为「麦当劳程序员节创意开发大赛」参赛作品。

- 活动仓库：https://github.com/M-China/mcd-developer-innovation-challenge
- MCP Server 文档：https://github.com/M-China/mcd-mcp-server
- 使用 WorkBuddy 开发

## 声明

本项目由参赛者独立开发，非麦当劳官方产品。项目输出仅供参考，餐品信息、价格及供应状态以麦当劳官方渠道的实时结果为准。MCP Token 请妥善保管，配置文件中仅使用环境变量占位符。

## License

MIT
