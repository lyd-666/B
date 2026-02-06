# 使用示例 | Usage Examples

## ⚠️ 重要说明

**本工具仅使用真实市场数据，不使用模拟数据**

- 程序将从 Yahoo Finance 获取真实的黄金价格数据
- 如果无法获取真实数据（如网络问题），程序将报错并退出
- 请确保网络连接稳定且能访问 Yahoo Finance

---

## 快速开始 | Quick Start

### 1. 安装依赖 | Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 运行程序 | Run the Program

```bash
python generate_premarket_plan.py
```

**成功运行示例：**
```
============================================================
黄金盘前计划生成器
Gold Pre-Market Planning Generator
当前时间: 2026年02月06日 09:00:00
============================================================

正在获取黄金价格数据...
⚠️  要求：仅使用真实市场数据，不使用模拟数据

正在从 Yahoo Finance 获取真实数据 (GC=F)...
✓ 成功获取真实数据
  数据范围: 2026-01-07 至 2026-02-05
  最新收盘价: $2720.50

✓ 成功获取 30 条真实数据记录
...
```

**失败情况示例：**
```
============================================================
✗ 错误：无法获取真实市场数据
============================================================

可能的原因：
  1. 网络连接问题
  2. Yahoo Finance API 暂时不可用
  3. 数据代码不正确

建议：
  - 检查网络连接
  - 稍后重试
  - 确认 yfinance 包已正确安装
```

### 3. 查看结果 | View Results

程序会生成一个HTML文件，文件名格式为：`gold_premarket_plan_YYYYMMDD.html`

直接在浏览器中打开该文件即可查看盘前计划。

The program will generate an HTML file named: `gold_premarket_plan_YYYYMMDD.html`

Open it in your browser to view the pre-market plan.

---

## 输出示例 | Output Example

生成的HTML报告包含以下部分（基于真实市场数据）：

### 1. 今日核心判断
> 黄金维持多头格局，收于2720.50，短期均线支撑有效。

### 2. 趋势框架有效性
- 最新收盘：$2720.50 (真实数据)
- 日内涨跌：+0.35%
- 均线排列：多头排列
- 波动状态：正常

### 3. 盘中关键触发条件

**顺趋势情景：**
- 价格守住MA5上方且创新高
- 成交量配合放大，动能保持正向

**观望情景：**
- 价格在MA5与MA10之间震荡
- 波动收窄，等待方向选择

**结构失效情景：**
- 有效跌破MA10
- 连续两日收盘低于短期均线

### 4. 主要风险与判断失效点

**主要风险：**
- 需关注美元指数、美债收益率等宏观因子
- 地缘政治事件可能引发剧烈波动

**判断失效点：**
- 震荡判断失效点：突破区间边界并持续运行

### 5. 今日参与强度
- 置信度：80%
- 建议：积极参与 - 框架清晰，信号明确，可适度放大仓位

### 6. 盘前纪律
> 严格止损，保护本金。

---

## 自定义配置 | Customization

### 修改数据获取周期

在 `generate_premarket_plan.py` 中修改：

```python
# 默认获取30天数据
df = fetch_gold_data(days=30)

# 可以修改为其他天数，如60天
df = fetch_gold_data(days=60)
```

### 调整技术指标参数

```python
# 修改移动平均线周期
df['MA5'] = df['Close'].rolling(window=5).mean()   # 5日均线
df['MA10'] = df['Close'].rolling(window=10).mean() # 10日均线
df['MA20'] = df['Close'].rolling(window=20).mean() # 20日均线
```

---

## 故障排除 | Troubleshooting

### 无法获取真实数据

⚠️ **重要：本工具不使用模拟数据**

如果程序报错 "无法获取真实市场数据"，请按以下步骤排查：

1. **检查网络连接**
   ```bash
   # 测试是否能访问 Yahoo Finance
   curl -I https://finance.yahoo.com
   ```

2. **验证 yfinance 安装**
   ```bash
   pip install --upgrade yfinance
   ```

3. **测试数据获取**
   ```bash
   python3 -c "import yfinance as yf; print(yf.Ticker('GC=F').history(period='5d'))"
   ```

4. **查看详细错误**
   程序会输出详细的错误信息，帮助诊断问题

### 常见错误及解决方案

**错误 1: "Could not resolve host"**
- 原因：无法访问 Yahoo Finance 服务器
- 解决：检查网络连接、防火墙设置、代理配置

**错误 2: "返回空数据"**
- 原因：数据代码可能不正确或市场休市
- 解决：确认使用正确的数据代码（GC=F 或 XAUUSD=X）

**错误 3: "Module not found"**
- 原因：依赖包未安装
- 解决：运行 `pip install -r requirements.txt`

### Python版本要求

请确保使用 Python 3.7 或更高版本：

```bash
python --version
# 应该显示 Python 3.7.x 或更高
```

---

## 技术说明 | Technical Details

### 数据来源

⚠️ **仅使用真实市场数据**

- 主要数据源：GC=F (Gold Futures) - 黄金期货
- 备选数据源：XAUUSD=X (Gold Spot Price) - 黄金现货
- 数据提供商：Yahoo Finance via yfinance
- **不使用模拟数据或演示数据**

### 技术指标计算

1. **移动平均线 (Moving Average)**
   - MA5：5日移动平均
   - MA10：10日移动平均
   - MA20：20日移动平均

2. **动能指标 (Momentum)**
   - 5日价格变化量

3. **波动率 (Volatility)**
   - 5日收盘价标准差

4. **平均真实波幅 (ATR)**
   - 5日日内波动平均值

### 置信度评分逻辑

- 基础分：50分
- 均线多头/空头排列：+20分
- 动能强：+15分
- 波动正常：+10分
- 波动过高：-5分
- 趋势明确（非震荡）：+5分
- 最终分数范围：0-100分

---

## 免责声明 | Disclaimer

⚠️ **本工具仅使用真实市场数据进行分析**

本工具生成的分析报告仅供参考，不构成投资建议。

投资有风险，入市需谨慎。请结合自身风险承受能力和其他信息源做出投资决策。

This tool uses only real market data for analysis and is for reference only. It does not constitute investment advice.

Investment involves risks. Please make decisions based on your risk tolerance and other information sources.
