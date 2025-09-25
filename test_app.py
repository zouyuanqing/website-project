#!/usr/bin/env python3
"""
简化版测试运行文件
"""
import os
import sys
from flask import Flask
from models import db
from config import Config

def test_imports():
    """测试关键导入是否正常"""
    try:
        from payment_config import get_payment_processor, PaymentResult
        print("✅ payment_config 导入成功")
        
        # 测试支付处理器
        processor = get_payment_processor()
        print("✅ 支付处理器初始化成功")
        
        # 测试创建一个简单的支付结果
        result = PaymentResult(
            success=True,
            message="测试成功",
            qr_code="test_qr_code"
        )
        print(f"✅ PaymentResult 创建成功: {result.qr_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return False

def test_basic_app():
    """测试基础Flask应用"""
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # 初始化数据库
        db.init_app(app)
        
        @app.route('/test')
        def test_route():
            return "测试路由工作正常"
        
        print("✅ 基础Flask应用创建成功")
        return app
        
    except Exception as e:
        print(f"❌ Flask应用创建失败: {str(e)}")
        return None

def main():
    print("开始测试核心功能...")
    print("="*50)
    
    # 测试导入
    if not test_imports():
        print("导入测试失败，停止测试")
        return
    
    # 测试Flask应用
    app = test_basic_app()
    if not app:
        print("Flask应用测试失败，停止测试")
        return
    
    print("="*50)
    print("✅ 核心功能测试通过！")
    print("现在可以尝试修复主应用程序了")
    
    # 尝试启动测试服务器
    print("\n🚀 启动测试服务器...")
    try:
        app.run(host='localhost', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 测试服务器已停止")

if __name__ == '__main__':
    main()