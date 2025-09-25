#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付功能测试脚本
用于验证微信支付和支付宝接口集成是否正常
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_config import PaymentProcessor, get_payment_processor
import json

def test_payment_config():
    """测试支付配置"""
    print("🧪 开始测试支付配置...")
    
    try:
        processor = get_payment_processor()
        print("✅ 支付处理器初始化成功")
        
        # 测试微信支付配置
        wechat_config = processor.wechat_config
        print(f"📱 微信支付配置:")
        print(f"   - App ID: {wechat_config.app_id}")
        print(f"   - 商户号: {wechat_config.mch_id}")
        print(f"   - 沙箱模式: {wechat_config.sandbox}")
        print(f"   - 回调地址: {wechat_config.notify_url}")
        
        # 测试支付宝配置
        alipay_config = processor.alipay_config
        print(f"🐜 支付宝配置:")
        print(f"   - App ID: {alipay_config.app_id}")
        print(f"   - 沙箱模式: {alipay_config.sandbox}")
        print(f"   - 回调地址: {alipay_config.notify_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ 支付配置测试失败: {str(e)}")
        return False

def test_wechat_payment():
    """测试微信支付订单创建"""
    print("\n🧪 开始测试微信支付...")
    
    try:
        processor = get_payment_processor()
        
        # 创建测试订单
        result = processor.create_wechat_payment(
            order_no="TEST_WX_" + str(int(__import__('time').time())),
            amount=0.01,  # 1分钱测试
            description="测试微信支付订单"
        )
        
        if result.success:
            print("✅ 微信支付订单创建成功")
            print(f"   - 支付链接: {result.payment_url}")
            print(f"   - 交易号: {result.trade_no}")
            print(f"   - 返回数据: {json.dumps(result.data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 微信支付订单创建失败: {result.message}")
            print(f"   - 错误代码: {result.error_code}")
            
        return result.success
        
    except Exception as e:
        print(f"❌ 微信支付测试异常: {str(e)}")
        return False

def test_alipay_payment():
    """测试支付宝支付订单创建"""
    print("\n🧪 开始测试支付宝支付...")
    
    try:
        processor = get_payment_processor()
        
        # 创建测试订单
        result = processor.create_alipay_payment(
            order_no="TEST_ALIPAY_" + str(int(__import__('time').time())),
            amount=0.01,  # 1分钱测试
            description="测试支付宝支付订单"
        )
        
        if result.success:
            print("✅ 支付宝支付订单创建成功")
            print(f"   - 支付链接: {result.payment_url}")
            print(f"   - 交易号: {result.trade_no}")
        else:
            print(f"❌ 支付宝支付订单创建失败: {result.message}")
            print(f"   - 错误代码: {result.error_code}")
            
        return result.success
        
    except Exception as e:
        print(f"❌ 支付宝支付测试异常: {str(e)}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始支付功能集成测试")
    print("=" * 50)
    
    # 测试结果记录
    results = []
    
    # 1. 测试支付配置
    results.append(("支付配置", test_payment_config()))
    
    # 2. 测试微信支付
    results.append(("微信支付", test_wechat_payment()))
    
    # 3. 测试支付宝支付
    results.append(("支付宝支付", test_alipay_payment()))
    
    # 输出测试结果总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    success_count = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(results)} 项测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试通过！支付功能集成成功！")
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接")
        print("\n📝 故障排除建议:")
        print("   1. 检查 .env 文件中的支付配置是否正确")
        print("   2. 确认网络连接正常")
        print("   3. 检查支付平台开发者账号是否配置正确")
        print("   4. 查看详细错误日志进行调试")
    
    return success_count == len(results)

if __name__ == "__main__":
    main()