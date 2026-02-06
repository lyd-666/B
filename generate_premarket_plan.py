#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金盘前计划生成器
Gold Pre-Market Planning Generator
"""

import json
from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd
import yfinance as yf


def fetch_gold_data(ticker="GC=F", days=30, allow_demo=False):
    """
    获取黄金价格数据（仅使用真实数据）
    Fetch gold price data from yfinance (real data only)
    
    Args:
        ticker: 数据代码 (GC=F for futures, XAUUSD=X for spot)
        days: 获取天数
        allow_demo: 是否允许演示模式（默认False，仅使用真实数据）
    
    Returns:
        DataFrame with real market data, or None if data cannot be fetched
    """
    print(f"正在从 Yahoo Finance 获取真实数据 ({ticker})...")
    
    try:
        gold = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        df = gold.history(start=start_date, end=end_date)
        
        if df.empty:
            # 尝试备选代码
            if ticker == "GC=F":
                print(f"GC=F 数据为空，尝试备选代码 XAUUSD=X...")
                gold = yf.Ticker("XAUUSD=X")
                df = gold.history(start=start_date, end=end_date)
            
        if not df.empty:
            # 验证数据时间范围
            latest_date = df.index[-1]
            print(f"✓ 成功获取真实数据")
            print(f"  数据范围: {df.index[0].strftime('%Y-%m-%d')} 至 {latest_date.strftime('%Y-%m-%d')}")
            print(f"  最新收盘价: ${df['Close'].iloc[-1]:.2f}")
            return df
        else:
            print(f"✗ {ticker} 返回空数据")
            return None
            
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        if allow_demo:
            print("⚠ 切换到演示模式，使用模拟数据...")
            return generate_sample_data(days)
        else:
            print("⚠ 无法获取真实数据，程序将退出")
            print("提示：请检查网络连接或稍后重试")
            return None


def generate_sample_data(days=30):
    """
    生成示例数据用于演示（仅在明确允许时使用）
    Generate sample data for demonstration (only when explicitly allowed)
    
    ⚠️ 警告：此函数仅用于演示目的，不应用于生产环境
    Warning: This function is for demonstration only, not for production use
    """
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # 模拟价格数据，基于合理的黄金价格区间
    base_price = 2650.0
    np.random.seed(42)
    
    # 生成带趋势的随机价格
    trend = np.linspace(0, 30, days)  # 轻微上升趋势
    noise = np.random.normal(0, 15, days)  # 随机波动
    close_prices = base_price + trend + noise
    
    # 生成其他OHLC数据
    data = {
        'Open': close_prices + np.random.uniform(-5, 5, days),
        'High': close_prices + np.random.uniform(5, 15, days),
        'Low': close_prices - np.random.uniform(5, 15, days),
        'Close': close_prices,
        'Volume': np.random.randint(50000, 200000, days)
    }
    
    df = pd.DataFrame(data, index=dates)
    print("⚠️ 注意：当前使用的是模拟数据，非真实市场数据！")
    return df


def calculate_technical_indicators(df):
    """
    计算技术指标
    Calculate technical indicators
    """
    if df is None or df.empty:
        return None
    
    # 计算移动平均线
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # 计算动能指标
    df['Momentum'] = df['Close'].diff(5)
    
    # 计算波动率
    df['Volatility'] = df['Close'].rolling(window=5).std()
    
    # 计算日内波动
    df['Daily_Range'] = df['High'] - df['Low']
    df['ATR'] = df['Daily_Range'].rolling(window=5).mean()
    
    # 计算 RSI (相对强弱指标)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 计算 MACD (指数平滑移动平均线)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    return df


def analyze_trend(df):
    """
    分析趋势和框架
    Analyze trend and framework
    """
    if df is None or df.empty or len(df) < 2:
        return {
            'trend': '数据不足',
            'confidence': 0,
            'analysis': {}
        }
    
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    # 近5日数据
    recent_5 = df.tail(5)
    
    # 趋势判断
    trend_direction = "上升" if latest['Close'] > latest['MA5'] else "下降"
    if abs(latest['Close'] - latest['MA5']) < latest['ATR'] * 0.3:
        trend_direction = "震荡"
    
    # 均线排列
    ma_alignment = ""
    if pd.notna(latest['MA5']) and pd.notna(latest['MA10']) and pd.notna(latest['MA20']):
        if latest['MA5'] > latest['MA10'] > latest['MA20']:
            ma_alignment = "多头排列"
        elif latest['MA5'] < latest['MA10'] < latest['MA20']:
            ma_alignment = "空头排列"
        else:
            ma_alignment = "混乱排列"
    
    # 动能分析
    momentum_strength = "强" if abs(latest['Momentum']) > latest['ATR'] else "弱"
    momentum_direction = "正" if latest['Momentum'] > 0 else "负"
    
    # 波动分析
    volatility_level = "高" if latest['Volatility'] > recent_5['Volatility'].mean() * 1.2 else "正常"
    
    # 价格位置
    price_position = ""
    if latest['Close'] > recent_5['High'].max() * 0.98:
        price_position = "接近区间高点"
    elif latest['Close'] < recent_5['Low'].min() * 1.02:
        price_position = "接近区间低点"
    else:
        price_position = "区间中部"
    
    # RSI 分析
    rsi_value = latest['RSI'] if pd.notna(latest['RSI']) else 50
    if rsi_value > 70:
        rsi_status = "超买"
    elif rsi_value < 30:
        rsi_status = "超卖"
    else:
        rsi_status = "中性"
    
    # MACD 分析
    macd_value = latest['MACD'] if pd.notna(latest['MACD']) else 0
    macd_signal = latest['MACD_Signal'] if pd.notna(latest['MACD_Signal']) else 0
    macd_hist = latest['MACD_Hist'] if pd.notna(latest['MACD_Hist']) else 0
    
    if macd_hist > 0:
        macd_status = "金叉" if previous['MACD_Hist'] <= 0 else "多头"
    else:
        macd_status = "死叉" if previous['MACD_Hist'] >= 0 else "空头"
    
    # 置信度计算 (0-100)
    confidence = 50
    if ma_alignment in ["多头排列", "空头排列"]:
        confidence += 20
    if momentum_strength == "强":
        confidence += 15
    if volatility_level == "正常":
        confidence += 10
    else:
        confidence -= 5
    if trend_direction != "震荡":
        confidence += 5
    
    # RSI 和 MACD 对置信度的影响
    if (rsi_status == "超买" and trend_direction == "上升") or (rsi_status == "超卖" and trend_direction == "下降"):
        confidence -= 10  # 趋势可能反转
    if macd_status in ["金叉", "多头"] and trend_direction == "上升":
        confidence += 5
    if macd_status in ["死叉", "空头"] and trend_direction == "下降":
        confidence += 5
    
    confidence = max(0, min(100, confidence))
    
    analysis = {
        'trend_direction': trend_direction,
        'ma_alignment': ma_alignment,
        'momentum_direction': momentum_direction,
        'momentum_strength': momentum_strength,
        'volatility_level': volatility_level,
        'price_position': price_position,
        'latest_close': latest['Close'],
        'previous_close': previous['Close'],
        'change_pct': ((latest['Close'] - previous['Close']) / previous['Close']) * 100,
        'ma5': latest['MA5'],
        'ma10': latest['MA10'],
        'ma20': latest['MA20'],
        'atr': latest['ATR'],
        'rsi': rsi_value,
        'rsi_status': rsi_status,
        'macd': macd_value,
        'macd_signal': macd_signal,
        'macd_hist': macd_hist,
        'macd_status': macd_status,
        'volume': latest['Volume'],
        'volume_prev': previous['Volume'],
        'high': latest['High'],
        'low': latest['Low'],
        'open': latest['Open']
    }
    
    return {
        'trend': trend_direction,
        'confidence': confidence,
        'analysis': analysis
    }


def generate_core_judgment(trend_data):
    """
    生成核心判断（一句话）
    Generate core judgment in one sentence
    """
    analysis = trend_data['analysis']
    trend = trend_data['trend']
    
    if trend == "上升":
        if analysis['ma_alignment'] == "多头排列":
            return f"黄金维持多头格局，收于{analysis['latest_close']:.2f}，短期均线支撑有效。"
        else:
            return f"黄金短期反弹至{analysis['latest_close']:.2f}，但结构尚未转强。"
    elif trend == "下降":
        if analysis['ma_alignment'] == "空头排列":
            return f"黄金空头格局延续，收于{analysis['latest_close']:.2f}，均线压制明显。"
        else:
            return f"黄金回调至{analysis['latest_close']:.2f}，需观察支撑是否有效。"
    else:
        return f"黄金于{analysis['latest_close']:.2f}附近震荡，方向尚不明确。"


def generate_trend_framework(trend_data):
    """
    判断趋势框架是否有效
    Check if trend framework is still valid
    """
    analysis = trend_data['analysis']
    
    if analysis['ma_alignment'] == "多头排列":
        if analysis['trend_direction'] == "上升" and analysis['momentum_direction'] == "正":
            return "有效 - 多头排列配合正动能，趋势延续性强。"
        else:
            return "弱化 - 虽保持多头排列，但动能或价格表现转弱。"
    elif analysis['ma_alignment'] == "空头排列":
        if analysis['trend_direction'] == "下降" and analysis['momentum_direction'] == "负":
            return "有效 - 空头排列配合负动能，下行压力延续。"
        else:
            return "弱化 - 虽保持空头排列，但出现反弹迹象。"
    else:
        return "无明确框架 - 均线混乱，处于方向选择阶段。"


def generate_trigger_conditions(trend_data):
    """
    生成关键触发条件（三情景）
    Generate key trigger conditions for three scenarios
    """
    analysis = trend_data['analysis']
    ma5 = analysis['ma5']
    ma10 = analysis['ma10']
    atr = analysis['atr']
    latest_close = analysis['latest_close']
    
    conditions = {
        'trend_following': [],
        'wait_and_see': [],
        'structure_failure': []
    }
    
    if analysis['trend_direction'] == "上升":
        # 顺趋势
        conditions['trend_following'].append(f"价格守住MA5（{ma5:.2f}）上方且创新高")
        conditions['trend_following'].append(f"成交量配合放大，动能保持正向")
        
        # 观望
        conditions['wait_and_see'].append(f"价格在MA5与MA10（{ma10:.2f}）之间震荡")
        conditions['wait_and_see'].append("波动收窄，等待方向选择")
        
        # 结构失效
        conditions['structure_failure'].append(f"有效跌破MA10（{ma10:.2f}），对应约{ma10-atr:.2f}")
        conditions['structure_failure'].append("连续两日收盘低于短期均线")
        
    elif analysis['trend_direction'] == "下降":
        # 顺趋势
        conditions['trend_following'].append(f"价格压制于MA5（{ma5:.2f}）下方且创新低")
        conditions['trend_following'].append("反弹无力，动能保持负向")
        
        # 观望
        conditions['wait_and_see'].append(f"价格在MA5与MA10（{ma10:.2f}）之间整理")
        conditions['wait_and_see'].append("下跌动能衰竭但尚未突破")
        
        # 结构失效
        conditions['structure_failure'].append(f"有效突破MA10（{ma10:.2f}），对应约{ma10+atr:.2f}")
        conditions['structure_failure'].append("连续两日收盘高于短期均线")
        
    else:  # 震荡
        # 顺趋势（此时为区间操作）
        conditions['trend_following'].append(f"区间高点{analysis['price_position']}附近做空")
        conditions['trend_following'].append(f"区间低点附近做多")
        
        # 观望
        conditions['wait_and_see'].append("价格位于区间中部，无明确方向")
        conditions['wait_and_see'].append("等待放量突破或跌破")
        
        # 结构失效
        conditions['structure_failure'].append(f"放量突破近期震荡区间")
        conditions['structure_failure'].append("均线开始发散，形成新趋势")
    
    return conditions


def generate_risks(trend_data):
    """
    生成主要风险与判断失效点
    Generate main risks and invalidation points
    """
    analysis = trend_data['analysis']
    
    risks = []
    invalidation_points = []
    
    # 波动风险
    if analysis['volatility_level'] == "高":
        risks.append("波动率处于高位，止损空间需相应扩大")
    
    # 均线排列风险
    if analysis['ma_alignment'] == "混乱排列":
        risks.append("均线混乱，假突破风险增加")
    
    # 动能风险
    if analysis['momentum_strength'] == "弱":
        risks.append("动能偏弱，趋势延续性存疑")
    
    # 外部因素
    risks.append("需关注美元指数、美债收益率等宏观因子")
    risks.append("地缘政治事件可能引发剧烈波动")
    
    # 失效点
    ma10 = analysis['ma10']
    if analysis['trend_direction'] == "上升":
        invalidation_points.append(f"多头判断失效点：有效跌破MA10（{ma10:.2f}）")
    elif analysis['trend_direction'] == "下降":
        invalidation_points.append(f"空头判断失效点：有效突破MA10（{ma10:.2f}）")
    else:
        invalidation_points.append(f"震荡判断失效点：突破区间边界并持续运行")
    
    return {
        'risks': risks,
        'invalidation_points': invalidation_points
    }


def generate_participation_intensity(confidence):
    """
    根据置信度生成参与强度建议
    Generate participation intensity based on confidence score
    """
    if confidence >= 80:
        return "积极参与 - 框架清晰，信号明确，可适度放大仓位"
    elif confidence >= 60:
        return "正常参与 - 趋势成立，按常规仓位操作"
    elif confidence >= 40:
        return "谨慎参与 - 信号有效性一般，降低仓位规模"
    else:
        return "观望为主 - 结构混乱或信号矛盾，等待更明确机会"


def generate_discipline():
    """
    生成一句话盘前纪律
    Generate one-sentence pre-market discipline
    """
    disciplines = [
        "计划你的交易，交易你的计划。",
        "严格止损，保护本金。",
        "顺势而为，不逆市场而动。",
        "耐心等待信号，不追涨杀跌。",
        "控制仓位，风险第一。"
    ]
    # 简单轮换或随机选择
    from datetime import datetime
    idx = datetime.now().day % len(disciplines)
    return disciplines[idx]


def generate_morning_summary(trend_data, df):
    """
    生成晨会级摘要 - 核心观点快速概览
    Generate morning briefing summary
    """
    analysis = trend_data['analysis']
    
    # 核心观点
    price = analysis['latest_close']
    trend = analysis['trend_direction']
    ma_align = analysis['ma_alignment']
    rsi = analysis['rsi']
    macd_status = analysis['macd_status']
    
    summary = f"黄金价格{price:.2f}美元，{trend}趋势，均线呈{ma_align}。"
    summary += f"RSI {rsi:.1f}（{analysis['rsi_status']}），MACD呈{macd_status}形态。"
    
    if trend_data['confidence'] >= 70:
        summary += f"框架清晰，置信度{trend_data['confidence']}%。"
    else:
        summary += f"信号存疑，置信度{trend_data['confidence']}%，建议谨慎。"
    
    return summary


def generate_trend_judgment(trend_data):
    """
    生成趋势判断 - 整体趋势、均线形态、RSI状态、MACD状态
    Generate comprehensive trend judgment
    """
    analysis = trend_data['analysis']
    
    judgment = {
        '整体趋势': analysis['trend_direction'],
        '均线形态': analysis['ma_alignment'],
        'RSI状态': f"{analysis['rsi']:.1f} - {analysis['rsi_status']}",
        'MACD状态': f"{analysis['macd_status']} (柱状:{analysis['macd_hist']:.2f})"
    }
    
    return judgment


def generate_technical_evidence(trend_data, df):
    """
    生成技术指标证据 - 详细指标数据与研判
    Generate technical indicator evidence
    """
    analysis = trend_data['analysis']
    latest = df.iloc[-1]
    
    evidence = {
        '移动平均线': {
            'MA5': f"{analysis['ma5']:.2f}",
            'MA10': f"{analysis['ma10']:.2f}",
            'MA20': f"{analysis['ma20']:.2f}",
            '排列': analysis['ma_alignment']
        },
        'RSI指标': {
            '数值': f"{analysis['rsi']:.2f}",
            '状态': analysis['rsi_status'],
            '研判': '超买区域，注意回调风险' if analysis['rsi'] > 70 else 
                   '超卖区域，关注反弹机会' if analysis['rsi'] < 30 else '中性区间，无明确信号'
        },
        'MACD指标': {
            'MACD': f"{analysis['macd']:.3f}",
            '信号线': f"{analysis['macd_signal']:.3f}",
            '柱状图': f"{analysis['macd_hist']:.3f}",
            '状态': analysis['macd_status']
        },
        '动能与波动': {
            '动能': f"{analysis['momentum_direction']}{analysis['momentum_strength']}",
            '波动率': analysis['volatility_level'],
            'ATR': f"{analysis['atr']:.2f}"
        }
    }
    
    return evidence


def generate_daily_commentary(trend_data):
    """
    生成每日盘面点评 - 当日交易特征分析
    Generate daily market commentary
    """
    analysis = trend_data['analysis']
    
    commentary = []
    
    # 价格走势
    change_pct = analysis['change_pct']
    if abs(change_pct) > 1:
        commentary.append(f"日内波动较大，涨跌幅达{change_pct:+.2f}%")
    else:
        commentary.append(f"日内波动平稳，涨跌幅{change_pct:+.2f}%")
    
    # 成交量分析
    vol_change = ((analysis['volume'] - analysis['volume_prev']) / analysis['volume_prev']) * 100
    if abs(vol_change) > 20:
        commentary.append(f"成交量{'放大' if vol_change > 0 else '萎缩'}{abs(vol_change):.1f}%，量价{'配合' if (change_pct > 0 and vol_change > 0) or (change_pct < 0 and vol_change < 0) else '背离'}")
    
    # 价格位置
    commentary.append(f"价格位于{analysis['price_position']}")
    
    # 技术形态
    if analysis['ma_alignment'] == "多头排列" and analysis['trend_direction'] == "上升":
        commentary.append("多头格局延续，上行动能充足")
    elif analysis['ma_alignment'] == "空头排列" and analysis['trend_direction'] == "下降":
        commentary.append("空头格局延续，下行压力明显")
    else:
        commentary.append("市场方向不明，等待突破")
    
    return commentary


def generate_today_vs_yesterday(trend_data):
    """
    生成今日vs昨日复盘 - 价格、成交量、波幅对比
    Generate today vs yesterday comparison
    """
    analysis = trend_data['analysis']
    
    comparison = {
        '收盘价对比': {
            '昨日': f"${analysis['previous_close']:.2f}",
            '今日': f"${analysis['latest_close']:.2f}",
            '涨跌': f"{analysis['change_pct']:+.2f}%"
        },
        '成交量对比': {
            '昨日': f"{analysis['volume_prev']:,.0f}",
            '今日': f"{analysis['volume']:,.0f}",
            '变化': f"{((analysis['volume'] - analysis['volume_prev']) / analysis['volume_prev'] * 100):+.1f}%"
        },
        '日内波幅': {
            '最高': f"${analysis['high']:.2f}",
            '最低': f"${analysis['low']:.2f}",
            '波幅': f"${analysis['high'] - analysis['low']:.2f} ({(analysis['high'] - analysis['low']) / analysis['low'] * 100:.2f}%)"
        }
    }
    
    return comparison


def generate_five_day_narrative(df):
    """
    生成近五日趋势叙事 - 短期走势回顾
    Generate five-day trend narrative
    """
    if len(df) < 5:
        return "数据不足，无法生成五日叙事"
    
    recent_5 = df.tail(5)
    
    # 计算五日统计
    high_5 = recent_5['High'].max()
    low_5 = recent_5['Low'].min()
    start_close = recent_5['Close'].iloc[0]
    end_close = recent_5['Close'].iloc[-1]
    change_5d = ((end_close - start_close) / start_close) * 100
    
    narrative = f"近五日黄金价格区间{low_5:.2f}-{high_5:.2f}美元，"
    
    if change_5d > 2:
        narrative += f"整体呈上升趋势，累计涨幅{change_5d:.2f}%。"
    elif change_5d < -2:
        narrative += f"整体呈下降趋势，累计跌幅{abs(change_5d):.2f}%。"
    else:
        narrative += f"整体呈震荡整理，涨跌幅{change_5d:+.2f}%。"
    
    # 判断走势特征
    closes = recent_5['Close'].values
    if all(closes[i] <= closes[i+1] for i in range(len(closes)-1)):
        narrative += "连续五日上涨，动能强劲。"
    elif all(closes[i] >= closes[i+1] for i in range(len(closes)-1)):
        narrative += "连续五日下跌，下行压力大。"
    else:
        narrative += "期间出现反复，方向不够明确。"
    
    return narrative


def generate_invalidation_conditions(trend_data):
    """
    生成判断失效条件 - 多空失效临界点
    Generate invalidation conditions for long/short positions
    """
    analysis = trend_data['analysis']
    
    conditions = {
        '多头失效': [],
        '空头失效': []
    }
    
    ma10 = analysis['ma10']
    ma20 = analysis['ma20']
    
    # 多头失效条件
    conditions['多头失效'].append(f"有效跌破MA10（{ma10:.2f}）")
    conditions['多头失效'].append(f"连续两日收盘低于MA20（{ma20:.2f}）")
    if analysis['rsi'] > 70:
        conditions['多头失效'].append("RSI从超买区回落至50以下")
    if analysis['macd_status'] in ["金叉", "多头"]:
        conditions['多头失效'].append("MACD死叉向下")
    
    # 空头失效条件
    conditions['空头失效'].append(f"有效突破MA10（{ma10:.2f}）")
    conditions['空头失效'].append(f"连续两日收盘高于MA20（{ma20:.2f}）")
    if analysis['rsi'] < 30:
        conditions['空头失效'].append("RSI从超卖区反弹至50以上")
    if analysis['macd_status'] in ["死叉", "空头"]:
        conditions['空头失效'].append("MACD金叉向上")
    
    return conditions


def generate_html_report(trend_data, conditions, risks, timestamp, df):
    """
    生成HTML盘前简报
    Generate HTML pre-market report
    """
    analysis = trend_data['analysis']
    confidence = trend_data['confidence']
    
    # 生成各模块内容
    core_judgment = generate_core_judgment(trend_data)
    framework_validity = generate_trend_framework(trend_data)
    participation = generate_participation_intensity(confidence)
    discipline = generate_discipline()
    
    # 新增模块内容
    morning_summary = generate_morning_summary(trend_data, df)
    trend_judgment = generate_trend_judgment(trend_data)
    tech_evidence = generate_technical_evidence(trend_data, df)
    daily_commentary = generate_daily_commentary(trend_data)
    today_vs_yesterday = generate_today_vs_yesterday(trend_data)
    five_day_narrative = generate_five_day_narrative(df)
    invalidation_conds = generate_invalidation_conditions(trend_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>黄金盘前计划 - {timestamp.strftime('%Y年%m月%d日')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header .date {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .section-title::before {{
            content: "▶";
            color: #667eea;
            margin-right: 8px;
            font-size: 14px;
        }}
        
        .section-content {{
            color: #4a5568;
            font-size: 15px;
        }}
        
        .highlight {{
            background: #fff5e1;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #ffa500;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 20px;
        }}
        
        .scenario {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        
        .scenario-title {{
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 15px;
        }}
        
        .scenario.bullish {{
            border-left: 4px solid #48bb78;
        }}
        
        .scenario.neutral {{
            border-left: 4px solid #ed8936;
        }}
        
        .scenario.bearish {{
            border-left: 4px solid #f56565;
        }}
        
        .condition-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .condition-list li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .condition-list li::before {{
            content: "•";
            position: absolute;
            left: 5px;
            color: #667eea;
            font-weight: bold;
        }}
        
        .risk-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .risk-list li {{
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .risk-list li::before {{
            content: "⚠";
            position: absolute;
            left: 0;
            color: #f56565;
        }}
        
        .confidence-bar {{
            width: 100%;
            height: 30px;
            background: #e2e8f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
            transition: width 1s ease;
        }}
        
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .data-item {{
            background: white;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        
        .data-label {{
            font-size: 13px;
            color: #718096;
            margin-bottom: 5px;
        }}
        
        .data-value {{
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .discipline {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            margin-top: 30px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #718096;
            font-size: 13px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .change-positive {{
            color: #48bb78;
        }}
        
        .change-negative {{
            color: #f56565;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>黄金（GC=F）盘前计划</h1>
            <div class="date">{timestamp.strftime('%Y年%m月%d日')} 生成</div>
        </div>
        
        <div class="content">
            <!-- 晨会级摘要 -->
            <div class="highlight" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
                🌅 <strong>晨会级摘要：</strong>{morning_summary}
            </div>
            
            <!-- 核心判断 -->
            <div class="highlight">
                📊 今日核心判断：{core_judgment}
            </div>
            
            <!-- 趋势判断 -->
            <div class="section">
                <div class="section-title">趋势判断</div>
                <div class="section-content">
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-label">整体趋势</div>
                            <div class="data-value" style="font-size: 16px;">{trend_judgment['整体趋势']}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">均线形态</div>
                            <div class="data-value" style="font-size: 16px;">{trend_judgment['均线形态']}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">RSI状态</div>
                            <div class="data-value" style="font-size: 14px;">{trend_judgment['RSI状态']}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">MACD状态</div>
                            <div class="data-value" style="font-size: 14px;">{trend_judgment['MACD状态']}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 技术指标证据 -->
            <div class="section">
                <div class="section-title">技术指标证据</div>
                <div class="section-content">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px;">
                        <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <strong style="color: #667eea;">移动平均线</strong>
                            <div style="margin-top: 8px; font-size: 13px;">
                                MA5: {tech_evidence['移动平均线']['MA5']}<br>
                                MA10: {tech_evidence['移动平均线']['MA10']}<br>
                                MA20: {tech_evidence['移动平均线']['MA20']}<br>
                                排列: {tech_evidence['移动平均线']['排列']}
                            </div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <strong style="color: #667eea;">RSI指标</strong>
                            <div style="margin-top: 8px; font-size: 13px;">
                                数值: {tech_evidence['RSI指标']['数值']}<br>
                                状态: {tech_evidence['RSI指标']['状态']}<br>
                                <em style="color: #718096;">{tech_evidence['RSI指标']['研判']}</em>
                            </div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <strong style="color: #667eea;">MACD指标</strong>
                            <div style="margin-top: 8px; font-size: 13px;">
                                MACD: {tech_evidence['MACD指标']['MACD']}<br>
                                信号线: {tech_evidence['MACD指标']['信号线']}<br>
                                柱状图: {tech_evidence['MACD指标']['柱状图']}<br>
                                状态: {tech_evidence['MACD指标']['状态']}
                            </div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0;">
                            <strong style="color: #667eea;">动能与波动</strong>
                            <div style="margin-top: 8px; font-size: 13px;">
                                动能: {tech_evidence['动能与波动']['动能']}<br>
                                波动率: {tech_evidence['动能与波动']['波动率']}<br>
                                ATR: {tech_evidence['动能与波动']['ATR']}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 每日盘面点评 -->
            <div class="section">
                <div class="section-title">每日盘面点评</div>
                <div class="section-content">
                    <ul class="condition-list">
                        {''.join([f'<li>{comment}</li>' for comment in daily_commentary])}
                    </ul>
                </div>
            </div>
            
            <!-- 今日vs昨日复盘 -->
            <div class="section">
                <div class="section-title">今日 vs 昨日复盘</div>
                <div class="section-content">
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-label">收盘价</div>
                            <div class="data-value" style="font-size: 14px;">
                                昨: {today_vs_yesterday['收盘价对比']['昨日']}<br>
                                今: {today_vs_yesterday['收盘价对比']['今日']}<br>
                                <span class="{'change-positive' if analysis['change_pct'] > 0 else 'change-negative'}">{today_vs_yesterday['收盘价对比']['涨跌']}</span>
                            </div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">成交量</div>
                            <div class="data-value" style="font-size: 14px;">
                                昨: {today_vs_yesterday['成交量对比']['昨日']}<br>
                                今: {today_vs_yesterday['成交量对比']['今日']}<br>
                                {today_vs_yesterday['成交量对比']['变化']}
                            </div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">日内波幅</div>
                            <div class="data-value" style="font-size: 14px;">
                                高: {today_vs_yesterday['日内波幅']['最高']}<br>
                                低: {today_vs_yesterday['日内波幅']['最低']}<br>
                                幅: {today_vs_yesterday['日内波幅']['波幅']}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 近五日趋势叙事 -->
            <div class="section">
                <div class="section-title">近五日趋势叙事</div>
                <div class="section-content">
                    <p>{five_day_narrative}</p>
                </div>
            </div>
            
            <!-- 趋势框架 -->
            <div class="section">
                <div class="section-title">趋势框架有效性</div>
                <div class="section-content">
                    {framework_validity}
                    
                    <div class="data-grid">
                        <div class="data-item">
                            <div class="data-label">最新收盘</div>
                            <div class="data-value">${analysis['latest_close']:.2f}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">日内涨跌</div>
                            <div class="data-value {'change-positive' if analysis['change_pct'] > 0 else 'change-negative'}">
                                {analysis['change_pct']:+.2f}%
                            </div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">均线排列</div>
                            <div class="data-value" style="font-size: 14px;">{analysis['ma_alignment']}</div>
                        </div>
                        <div class="data-item">
                            <div class="data-label">波动状态</div>
                            <div class="data-value" style="font-size: 14px;">{analysis['volatility_level']}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 盘中关键触发条件 -->
            <div class="section">
                <div class="section-title">盘中关键触发条件</div>
                <div class="section-content">
                    <div class="scenario bullish">
                        <div class="scenario-title">✓ 顺趋势情景</div>
                        <ul class="condition-list">
                            {''.join([f'<li>{cond}</li>' for cond in conditions['trend_following']])}
                        </ul>
                    </div>
                    
                    <div class="scenario neutral">
                        <div class="scenario-title">◐ 观望情景</div>
                        <ul class="condition-list">
                            {''.join([f'<li>{cond}</li>' for cond in conditions['wait_and_see']])}
                        </ul>
                    </div>
                    
                    <div class="scenario bearish">
                        <div class="scenario-title">✗ 结构失效情景</div>
                        <ul class="condition-list">
                            {''.join([f'<li>{cond}</li>' for cond in conditions['structure_failure']])}
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 风险与失效点 -->
            <div class="section">
                <div class="section-title">主要风险与判断失效点</div>
                <div class="section-content">
                    <div style="margin-bottom: 15px;">
                        <strong>主要风险：</strong>
                        <ul class="risk-list">
                            {''.join([f'<li>{risk}</li>' for risk in risks['risks']])}
                        </ul>
                    </div>
                    <div>
                        <strong>判断失效点：</strong>
                        <ul class="risk-list">
                            {''.join([f'<li>{point}</li>' for point in risks['invalidation_points']])}
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 判断失效条件详细 -->
            <div class="section">
                <div class="section-title">判断失效条件 - 多空临界点</div>
                <div class="section-content">
                    <div class="scenario bullish" style="margin-bottom: 15px;">
                        <div class="scenario-title">🔴 多头失效临界点</div>
                        <ul class="condition-list">
                            {''.join([f'<li>{cond}</li>' for cond in invalidation_conds['多头失效']])}
                        </ul>
                    </div>
                    <div class="scenario bearish">
                        <div class="scenario-title">🟢 空头失效临界点</div>
                        <ul class="condition-list">
                            {''.join([f'<li>{cond}</li>' for cond in invalidation_conds['空头失效']])}
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 参与强度 -->
            <div class="section">
                <div class="section-title">置信度评分与参与强度</div>
                <div class="section-content">
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {confidence}%;">
                            置信度 {confidence}%
                        </div>
                    </div>
                    <p style="margin-top: 10px;">{participation}</p>
                </div>
            </div>
            
            <!-- 盘前纪律 -->
            <div class="discipline">
                💡 盘前纪律：{discipline}
            </div>
        </div>
        
        <div class="footer">
            数据来源：yfinance (GC=F) | 仅供参考，不构成投资建议
        </div>
    </div>
</body>
</html>
"""
    
    return html_content


def main():
    """
    主函数
    Main function
    """
    print("=" * 60)
    print("黄金盘前计划生成器")
    print("Gold Pre-Market Planning Generator")
    print(f"当前时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 获取数据（仅使用真实数据）
    print("正在获取黄金价格数据...")
    print("⚠️  要求：仅使用真实市场数据，不使用模拟数据")
    print()
    
    df = fetch_gold_data(allow_demo=False)
    
    if df is None or df.empty:
        print()
        print("=" * 60)
        print("✗ 错误：无法获取真实市场数据")
        print("=" * 60)
        print()
        print("可能的原因：")
        print("  1. 网络连接问题")
        print("  2. Yahoo Finance API 暂时不可用")
        print("  3. 数据代码不正确")
        print()
        print("建议：")
        print("  - 检查网络连接")
        print("  - 稍后重试")
        print("  - 确认 yfinance 包已正确安装")
        print()
        return 1  # 返回错误码
    
    print()
    print(f"✓ 成功获取 {len(df)} 条真实数据记录")
    
    # 计算技术指标
    print("正在计算技术指标...")
    df = calculate_technical_indicators(df)
    
    # 分析趋势
    print("正在分析趋势...")
    trend_data = analyze_trend(df)
    
    # 生成触发条件
    print("正在生成触发条件...")
    conditions = generate_trigger_conditions(trend_data)
    
    # 生成风险分析
    print("正在生成风险分析...")
    risks = generate_risks(trend_data)
    
    # 生成HTML报告
    print("正在生成HTML报告...")
    timestamp = datetime.now()
    html_content = generate_html_report(trend_data, conditions, risks, timestamp, df)
    
    # 保存文件
    output_file = f"gold_premarket_plan_{timestamp.strftime('%Y%m%d')}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print()
    print("=" * 60)
    print(f"✓ 报告生成成功！")
    print(f"文件位置：{output_file}")
    print("=" * 60)
    print()
    print("核心数据摘要：")
    print(f"  最新价格：${trend_data['analysis']['latest_close']:.2f}")
    print(f"  趋势方向：{trend_data['trend']}")
    print(f"  置信度：{trend_data['confidence']}%")
    print(f"  均线排列：{trend_data['analysis']['ma_alignment']}")
    print()
    
    return 0  # 返回成功码


if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code if exit_code is not None else 0)
