#!/usr/bin/env python3
"""
时间显示修复测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timezone, timedelta
from app import format_datetime, utc_to_local

def test_time_conversion():
    """测试时间转换功能"""
    print("🕒 时间显示修复测试")
    print("=" * 50)
    
    # 创建一个UTC时间
    utc_time = datetime(2025, 1, 20, 10, 30, 0)  # UTC 10:30
    print(f"原始UTC时间: {utc_time}")
    
    # 转换为北京时间
    beijing_time = utc_to_local(utc_time)
    print(f"北京时间: {beijing_time}")
    
    # 测试格式化函数
    formatted_time = format_datetime(utc_time)
    print(f"格式化时间: {formatted_time}")
    
    # 测试各种格式
    print("\n🎨 格式化测试:")
    print(f"完整时间: {format_datetime(utc_time, '%Y-%m-%d %H:%M:%S')}")
    print(f"仅日期: {format_datetime(utc_time, '%Y-%m-%d')}")
    print(f"简短时间: {format_datetime(utc_time, '%m-%d %H:%M')}")
    print(f"中文格式: {format_datetime(utc_time, '%Y年%m月%d日 %H:%M')}")
    
    # 测试None值处理
    print(f"\nNone值测试: '{format_datetime(None)}'")
    
    print("\n✅ 时间转换测试完成!")

if __name__ == "__main__":
    test_time_conversion()