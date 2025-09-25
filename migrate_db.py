#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加支付功能支持（包括收款账户管理）
"""

from app import create_app
from models import db
import os

def migrate_database():
    """执行数据库迁移"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 开始数据库迁移...")
            
            # 创建所有表（包括新的PaymentOrder表）
            db.create_all()
            
            print("✅ 数据库迁移完成！")
            print("📋 已创建的表包括：")
            print("  - User (用户表)")
            print("  - Admin (管理员表)")
            print("  - Form (表单表)")
            print("  - FormField (表单字段表)")
            print("  - Submission (提交记录表)")
            print("  - SubmissionData (提交数据表)")
            print("  - UploadFile (上传文件表)")
            print("  - PaymentOrder (支付订单表) [新增]")
            print("  - PaymentAccount (收款账户表) [新增]")
            
        except Exception as e:
            print(f"❌ 数据库迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()