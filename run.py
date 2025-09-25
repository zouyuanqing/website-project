#!/usr/bin/env python3
"""
信息收集系统启动文件
"""
import os
import sys
from app import create_app
from models import db, Admin
from config import Config

def create_admin_user():
    """创建默认管理员用户"""
    admin = Admin.query.filter_by(email=Config.ADMIN_EMAIL).first()
    if not admin:
        admin = Admin(
            email=Config.ADMIN_EMAIL,
            name='系统管理员'
        )
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print(f"默认管理员账号已创建:")
        print(f"邮箱: {Config.ADMIN_EMAIL}")
        print(f"密码: {Config.ADMIN_PASSWORD}")
    else:
        print("管理员账号已存在")

def main():
    """主函数"""
    # 创建Flask应用
    app = create_app()
    
    # 验证生产环境配置
    try:
        Config.validate_production_config()
    except ValueError as e:
        print(f"⚠️  配置错误: {e}")
        if Config.FLASK_ENV == 'production':
            print("生产环境不允许启动，请修复配置后重试")
            return
        else:
            print("开发环境继续启动，但请在生产环境中修复这些问题")
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("数据库表创建完成")
        
        # 创建默认管理员
        create_admin_user()
        
        # 创建上传目录
        upload_dir = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_dir, exist_ok=True)
        print(f"上传目录创建完成: {upload_dir}")
    
    # 启动应用
    print("\n" + "="*50)
    print("🚀 信息收集系统启动成功!")
    print("="*50)
    print(f"📱 访问地址: http://localhost:5000")
    print(f"👤 用户注册: http://localhost:5000/register")
    print(f"🔐 用户登录: http://localhost:5000/login")
    print(f"⚙️  管理后台: http://localhost:5000/admin/login")
    
    # 只在开发环境显示默认凭据
    if Config.FLASK_ENV == 'development':
        print(f"📧 管理员邮箱: {Config.ADMIN_EMAIL}")
        print(f"🔑 管理员密码: {Config.ADMIN_PASSWORD}")
        print("⚠️  警告: 生产环境中请修改默认密码!")
    else:
        print("🔒 生产环境 - 管理员凭据已隐藏")
    
    print("="*50)
    print("按 Ctrl+C 停止服务器")
    print("="*50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.DEBUG,
            use_reloader=Config.FLASK_ENV == 'development'
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        sys.exit(0)

if __name__ == '__main__':
    main()
