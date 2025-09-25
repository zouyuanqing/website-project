#!/usr/bin/env python3
"""
测试个人中心功能
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, PaymentOrder, PaymentAccount, Submission
from config import Config

def create_test_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 登录管理
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/test-dashboard')
    def test_dashboard():
        """测试个人中心页面"""
        # 模拟用户登录状态
        user = User.query.first()
        if not user:
            # 创建测试用户
            user = User(name="测试用户", email="test@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()
        
        # 模拟支付统计数据
        user_payment_stats = {
            'total_payments': 3,
            'paid_orders': 2,
            'pending_payments': 1,
            'total_paid_amount': 299.80,
            'wechat_payments': 2,
            'alipay_payments': 1,
            'wechat_amount': 199.80,
            'alipay_amount': 100.00
        }
        
        # 模拟提交记录
        submissions = []
        
        # 模拟支付订单
        payment_orders = []
        
        return render_template('user/dashboard.html',
                               submissions=submissions,
                               payment_stats=user_payment_stats,
                               payment_orders=payment_orders)
    
    @app.route('/api/payment-accounts')
    def api_payment_accounts():
        """获取收款账户信息API"""
        try:
            accounts = PaymentAccount.query.all()
            account_list = []
            
            for account in accounts:
                account_data = {
                    'id': account.id,
                    'account_name': account.account_name,
                    'account_type': account.account_type,
                    'account_holder': account.account_holder,
                    'get_account_display': account.get_account_display()
                }
                account_list.append(account_data)
            
            return jsonify({
                'success': True,
                'accounts': account_list
            })
        except Exception as e:
            print(f"获取收款账户失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': '获取收款账户信息失败'
            }), 500
    
    @app.route('/api/user/profile', methods=['POST'])
    def api_update_profile():
        """更新用户个人信息API（测试版）"""
        return jsonify({
            'success': True,
            'message': '个人信息更新成功（测试模式）'
        })
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("数据库表创建完成")
        
        # 创建测试收款账户
        if not PaymentAccount.query.first():
            from models import Admin
            
            # 创建测试管理员
            admin = Admin.query.first()
            if not admin:
                admin = Admin(name="测试管理员", email="admin@test.com")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
            
            # 创建测试收款账户
            accounts = [
                PaymentAccount(
                    account_name="微信收款",
                    account_type="wechat_pay",
                    account_number="wx123456789",
                    account_holder="张三",
                    created_by=admin.id
                ),
                PaymentAccount(
                    account_name="支付宝收款",
                    account_type="alipay",
                    account_number="alipay@example.com",
                    account_holder="李四",
                    created_by=admin.id
                ),
                PaymentAccount(
                    account_name="银行卡收款",
                    account_type="bank_card",
                    account_number="6222021234567890123",
                    account_holder="王五",
                    bank_name="中国工商银行",
                    bank_branch="北京分行",
                    created_by=admin.id
                )
            ]
            
            for account in accounts:
                db.session.add(account)
            
            db.session.commit()
            print("测试收款账户创建完成")
    
    print("🚀 启动个人中心测试服务器...")
    print("📱 访问地址: http://localhost:5002/test-dashboard")
    
    app.run(host='localhost', port=5002, debug=True)