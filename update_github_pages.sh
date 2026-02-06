#!/bin/bash
# 更新 GitHub Pages 的脚本
# Script to update GitHub Pages with latest report

set -e

echo "================================================"
echo "  更新 GitHub Pages 黄金盘前计划报告"
echo "  Updating GitHub Pages Gold Pre-Market Report"
echo "================================================"
echo ""

# 生成最新报告
echo "正在生成最新报告..."
python3 generate_premarket_plan.py

# 查找最新生成的报告
LATEST_REPORT=$(ls -t gold_premarket_plan_*.html 2>/dev/null | head -1)

if [ -z "$LATEST_REPORT" ]; then
    echo "错误：未找到生成的报告文件"
    exit 1
fi

echo "找到报告：$LATEST_REPORT"

# 复制为 index.html
echo "复制为 index.html..."
cp "$LATEST_REPORT" index.html

echo ""
echo "✓ index.html 已更新"
echo ""
echo "下一步："
echo "  1. git add index.html"
echo "  2. git commit -m 'Update GitHub Pages report'"
echo "  3. git push origin main"
echo ""
echo "完成后访问: https://lyd-666.github.io/B/"
echo ""
