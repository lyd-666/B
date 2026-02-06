#!/usr/bin/env python3
"""
yfinance连接测试脚本
用于诊断Yahoo Finance API的可用性
"""

import sys

def test_yfinance_connection():
    """测试Yahoo Finance连接"""
    print("=" * 60)
    print("测试Yahoo Finance连接")
    print("=" * 60)
    
    # 测试导入
    print("\n1. 测试模块导入...")
    try:
        import yfinance as yf
        print(f"   ✓ yfinance 版本: {yf.__version__}")
    except ImportError as e:
        print(f"   ✗ 无法导入yfinance: {e}")
        print("\n   解决方法：")
        print("   pip install yfinance")
        return False
    
    # 测试网络连接
    print("\n2. 测试网络连接...")
    try:
        import socket
        socket.setdefaulttimeout(5)
        socket.create_connection(("finance.yahoo.com", 80))
        print("   ✓ 可以连接到 finance.yahoo.com")
        network_ok = True
    except Exception as e:
        print(f"   ✗ 无法连接到 finance.yahoo.com: {type(e).__name__}")
        network_ok = False
    
    # 测试数据获取
    print("\n3. 测试数据获取 (GC=F)...")
    try:
        ticker = yf.Ticker("GC=F")
        print("   - 正在获取5日历史数据...")
        data = ticker.history(period="5d")
        
        if not data.empty:
            print(f"   ✓ 成功获取数据！")
            print(f"     - 数据行数: {len(data)}")
            print(f"     - 最新价格: ${data['Close'].iloc[-1]:.2f}")
            print(f"     - 最新日期: {data.index[-1].strftime('%Y-%m-%d')}")
            print(f"     - 日期范围: {data.index[0].strftime('%Y-%m-%d')} 至 {data.index[-1].strftime('%Y-%m-%d')}")
            return True
        else:
            print("   ✗ 获取的数据为空")
            return False
            
    except Exception as e:
        print(f"   ✗ 获取数据失败")
        print(f"     错误类型: {type(e).__name__}")
        error_msg = str(e)
        if len(error_msg) > 200:
            error_msg = error_msg[:200] + "..."
        print(f"     错误详情: {error_msg}")
        
        # 分析常见错误
        if "DNS" in str(e) or "resolve host" in str(e):
            print("\n   ⚠️  DNS解析失败 - 可能的原因：")
            print("     - 网络防火墙限制")
            print("     - DNS服务器问题")
            print("     - 需要配置代理")
        elif "timeout" in str(e).lower():
            print("\n   ⚠️  连接超时 - 可能的原因：")
            print("     - 网络速度慢")
            print("     - Yahoo Finance服务器响应慢")
            print("     - 需要增加超时时间")
        elif "403" in str(e) or "Forbidden" in str(e):
            print("\n   ⚠️  访问被拒绝 - 可能的原因：")
            print("     - IP被Yahoo Finance限制")
            print("     - 需要使用代理")
            print("     - Cookie/User-Agent问题")
        
        return False
    
    finally:
        print("\n" + "=" * 60)


def test_alternative_ticker():
    """测试备选代码"""
    print("\n4. 测试备选代码 (XAUUSD=X)...")
    try:
        import yfinance as yf
        ticker = yf.Ticker("XAUUSD=X")
        data = ticker.history(period="5d")
        
        if not data.empty:
            print(f"   ✓ 备选代码可用！")
            print(f"     - 最新价格: ${data['Close'].iloc[-1]:.2f}")
            return True
        else:
            print("   ✗ 备选代码也无数据")
            return False
    except Exception as e:
        print(f"   ✗ 备选代码失败: {type(e).__name__}")
        return False


def print_summary(yfinance_ok):
    """打印总结"""
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    if yfinance_ok:
        print("\n✅ Yahoo Finance 完全可用")
        print("\n建议：")
        print("  - 可以直接使用 yfinance 获取实时数据")
        print("  - 运行 generate_premarket_plan.py 将使用真实API数据")
        print("\n示例代码：")
        print("  python generate_premarket_plan.py")
    else:
        print("\n⚠️  Yahoo Finance 当前不可用")
        print("\n不用担心！系统会自动使用备用方案：")
        print("  1. 网络备用数据源（基于真实市场价格）")
        print("  2. 数据来源会在报告页脚显示")
        print("\n建议：")
        print("  - 直接运行程序，系统会自动处理")
        print("  - 查看页脚确认数据来源")
        print("  - 如需Yahoo Finance，可以：")
        print("    • 在本地无限制网络环境运行")
        print("    • 配置HTTP代理")
        print("    • 使用VPN")
        print("\n示例代码：")
        print("  # 仍然可以正常使用")
        print("  python generate_premarket_plan.py")
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    try:
        yfinance_ok = test_yfinance_connection()
        
        if not yfinance_ok:
            test_alternative_ticker()
        
        print_summary(yfinance_ok)
        
        # 返回状态码
        sys.exit(0 if yfinance_ok else 1)
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n测试过程发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
