# 黄金盘前计划生成器 | Gold Pre-Market Planning Generator

一个自动化的黄金交易盘前分析工具，基于技术分析生成专业的盘前简报网页。

## 功能特点

- **仅使用真实市场数据** - 从 yfinance 获取真实黄金价格数据（GC=F，备选 XAUUSD=X）
- 计算关键技术指标：移动平均线、动能、波动率
- 生成多维度分析框架：趋势判断、触发条件、风险评估
- 输出专业的中文盘前简报网页

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python generate_premarket_plan.py
```

程序将生成一个 HTML 文件，文件名格式为：`gold_premarket_plan_YYYYMMDD.html`

## 重要说明

⚠️ **本工具仅使用真实市场数据**
- 程序将从 Yahoo Finance 获取最新的黄金价格数据
- 如果无法获取真实数据，程序将报错并退出
- 不会使用模拟数据或演示数据
- 需要稳定的互联网连接

## 报告内容

生成的盘前计划包含以下模块：

1. **今日核心判断** - 一句话总结当前市场状态
2. **趋势框架有效性** - 判断当前趋势是否延续
3. **盘中关键触发条件** - 三种情景（顺趋势/观望/结构失效）的具体条件
4. **主要风险与判断失效点** - 风险提示和止损参考
5. **今日参与强度** - 基于置信度的仓位建议
6. **盘前纪律** - 交易纪律提醒

## 技术说明

- 数据源：yfinance (Yahoo Finance) - **仅真实数据**
- 分析周期：近30个交易日
- 主要指标：MA5、MA10、MA20、动能、ATR
- 输出格式：HTML（响应式设计）

## 注意事项

⚠️ 本工具生成的分析报告仅供参考，不构成投资建议。请结合自身风险承受能力和其他信息源做出投资决策。

## 系统要求

- Python 3.7+
- **稳定的互联网连接**（必须能访问 Yahoo Finance）
- yfinance、pandas、numpy 等依赖包

## 故障排除

如果遇到 "无法获取真实市场数据" 错误：
1. 检查网络连接是否正常
2. 确认能否访问 Yahoo Finance (finance.yahoo.com)
3. 稍后重试
4. 检查 yfinance 包是否正确安装：`pip install --upgrade yfinance`

## License

MIT