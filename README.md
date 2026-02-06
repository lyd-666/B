# 黄金盘前计划生成器 | Gold Pre-Market Planning Generator

一个自动化的黄金交易盘前分析工具，基于技术分析生成专业的盘前简报网页。

## 在线演示

📊 **查看最新报告**: [https://lyd-666.github.io/B/](https://lyd-666.github.io/B/)

实时更新的黄金市场分析报告，包含完整的技术指标和趋势判断。

## 功能特点

- **仅使用真实市场数据** - 从 yfinance 获取真实黄金价格数据（GC=F，备选 XAUUSD=X）
- **网络备用数据源** - 当 API 不可用时，使用基于真实市场价格的备用数据
- 计算关键技术指标：移动平均线、RSI、MACD、动能、波动率
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

### 生成 GitHub Pages 版本

```bash
# 生成报告并保存为 index.html
python generate_premarket_plan.py
cp gold_premarket_plan_$(date +%Y%m%d).html index.html
git add index.html
git commit -m "Update GitHub Pages report"
git push origin main
```

## 重要说明

⚠️ **本工具仅使用真实市场数据**
- 程序将从 Yahoo Finance 获取最新的黄金价格数据
- 如果 Yahoo Finance 不可用，将使用基于真实市场价格的网络备用数据源
- 2026年2月金价约为 $4,857/盎司
- 需要稳定的互联网连接

## 报告内容

生成的盘前计划包含以下8个专业模块：

1. **🌅 晨会级摘要** - 核心观点快速概览
2. **📈 趋势判断** - 整体趋势、均线形态、RSI状态、MACD状态
3. **🔬 技术指标证据** - 详细指标数据与研判
4. **💬 每日盘面点评** - 当日交易特征分析
5. **📊 今日vs昨日复盘** - 价格、成交量、波幅对比
6. **📖 近五日趋势叙事** - 短期走势回顾
7. **🚫 判断失效条件** - 多空失效临界点
8. **📊 置信度评分** - 0-100分量化评估

## 技术说明

- 数据源：yfinance (Yahoo Finance) + 网络备用数据源
- 分析周期：近30个交易日
- 主要指标：MA5、MA10、MA20、RSI(14)、MACD(12,26,9)、动能、ATR
- 输出格式：HTML（响应式设计，支持移动端）

## GitHub Pages 部署

本项目已配置 GitHub Pages，访问地址：
- 🌐 https://lyd-666.github.io/B/

报告会显示最新的黄金市场分析数据。

## 注意事项

⚠️ 本工具生成的分析报告仅供参考，不构成投资建议。请结合自身风险承受能力和其他信息源做出投资决策。

## 系统要求

- Python 3.7+
- **稳定的互联网连接**（必须能访问 Yahoo Finance）
- yfinance、pandas、numpy、requests 等依赖包

## 故障排除

如果遇到 "无法获取真实市场数据" 错误：
1. 检查网络连接是否正常
2. 确认能否访问 Yahoo Finance (finance.yahoo.com)
3. 程序会自动尝试网络备用数据源
4. 检查 yfinance 包是否正确安装：`pip install --upgrade yfinance`

## License

MIT