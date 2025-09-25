#!/usr/bin/env python3
"""
创建演示数据脚本
"""

from app import create_app
from models import db, Admin, PaymentAccount, User

def create_demo_data():
    """创建演示数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 创建演示数据...")
            
            # 创建管理员账户
            admin = Admin.query.filter_by(email='admin@demo.com').first()
            if not admin:
                admin = Admin(
                    name='演示管理员',
                    email='admin@demo.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.flush()  # 获取admin.id
                print("✅ 创建管理员账户: admin@demo.com / admin123")
            
            # 创建测试用户
            user = User.query.filter_by(email='user@demo.com').first()
            if not user:
                user = User(
                    name='测试用户',
                    email='user@demo.com'
                )
                user.set_password('user123')
                db.session.add(user)
                print("✅ 创建测试用户: user@demo.com / user123")
            
            # 创建收款账户
            accounts_data = [
                {
                    'account_name': '微信收款账户',
                    'account_type': 'wechat',
                    'account_number': 'wxpay_demo_123456',
                    'account_holder': '张三',
                },
                {
                    'account_name': '支付宝收款账户',
                    'account_type': 'alipay',
                    'account_number': 'alipay_demo@example.com',
                    'account_holder': '李四',
                },
                {
                    'account_name': '银行卡收款账户',
                    'account_type': 'bank_card',
                    'account_number': '6222021234567890123',
                    'account_holder': '王五',
                    'bank_name': '中国工商银行',
                    'bank_branch': '北京分行营业部',
                }
            ]
            
            for account_data in accounts_data:
                existing_account = PaymentAccount.query.filter_by(
                    account_number=account_data['account_number']
                ).first()
                
                if not existing_account:
                    payment_account = PaymentAccount(
                        created_by=admin.id,
                        **account_data
                    )
                    db.session.add(payment_account)
                    print(f"✅ 创建收款账户: {account_data['account_name']}")
            
            db.session.commit()
            
            print("🎉 演示数据创建完成！")
            print("📋 账户信息：")
            print("  - 管理员: admin@demo.com / admin123")
            print("  - 测试用户: user@demo.com / user123")
            print("  - 已创建3个演示收款账户")
            
        except Exception as e:
            print(f"❌ 演示数据创建失败: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    create_demo_data()