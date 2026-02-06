# 使用示例 | Usage Examples

## 快速开始 | Quick Start

### 1. 安装依赖 | Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 运行程序 | Run the Program

```bash
python generate_premarket_plan.py
```

### 3. 查看结果 | View Results

程序会生成一个HTML文件，文件名格式为：`gold_premarket_plan_YYYYMMDD.html`

直接在浏览器中打开该文件即可查看盘前计划。

The program will generate an HTML file named: `gold_premarket_plan_YYYYMMDD.html`

Open it in your browser to view the pre-market plan.

---

## 输出示例 | Output Example

生成的HTML报告包含以下部分：

### 1. 今日核心判断
> 黄金于2675.62附近震荡，方向尚不明确。

### 2. 趋势框架有效性
- 最新收盘：$2675.62
- 日内涨跌：+0.21%
- 均线排列：多头排列
- 波动状态：正常

### 3. 盘中关键触发条件

**顺趋势情景：**
- 区间高点接近区间高点附近做空
- 区间低点附近做多

**观望情景：**
- 价格位于区间中部，无明确方向
- 等待放量突破或跌破

**结构失效情景：**
- 放量突破近期震荡区间
- 均线开始发散，形成新趋势

### 4. 主要风险与判断失效点

**主要风险：**
- 动能偏弱，趋势延续性存疑
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

### 网络连接问题

如果无法连接到 Yahoo Finance 获取数据，程序会自动切换到演示模式，使用模拟数据生成报告。

```
正在获取黄金价格数据...
获取数据失败: ...
切换到演示模式，使用模拟数据...
```

### Python版本要求

请确保使用 Python 3.7 或更高版本：

```bash
python --version
# 应该显示 Python 3.7.x 或更高
```

---

## 技术说明 | Technical Details

### 数据来源
- 主要数据源：GC=F (Gold Futures)
- 备选数据源：XAUUSD=X (Gold Spot Price)
- 数据提供商：Yahoo Finance via yfinance

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

本工具生成的分析报告仅供参考，不构成投资建议。

投资有风险，入市需谨慎。请结合自身风险承受能力和其他信息源做出投资决策。

This tool's analysis is for reference only and does not constitute investment advice.

Investment involves risks. Please make decisions based on your risk tolerance and other information sources.
