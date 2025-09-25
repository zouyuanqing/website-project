#!/usr/bin/env python3
"""
Heroku部署脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_heroku_cli():
    """检查是否安装了Heroku CLI"""
    try:
        result = subprocess.run(['heroku', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Heroku CLI已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到Heroku CLI")
        print("请先安装Heroku CLI:")
        print("1. 访问 https://devcenter.heroku.com/articles/heroku-cli")
        print("2. 下载并安装适用于Windows的Heroku CLI")
        print("3. 安装完成后重启命令行")
        return False

def login_heroku():
    """登录Heroku"""
    try:
        print("正在登录Heroku...")
        subprocess.run(['heroku', 'login'], check=True)
        print("✅ Heroku登录成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Heroku登录失败")
        return False

def create_heroku_app():
    """创建Heroku应用"""
    try:
        print("正在创建Heroku应用...")
        result = subprocess.run(['heroku', 'create'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Heroku应用创建成功: {result.stdout.strip()}")
        
        # 获取应用名称
        output = result.stdout.strip()
        # 提取应用名称 (格式: https://<app-name>.herokuapp.com/ | https://git.heroku.com/<app-name>.git)
        app_name = output.split('https://')[1].split('.herokuapp.com')[0]
        return app_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Heroku应用创建失败: {e.stderr}")
        return None

def setup_heroku_config(app_name):
    """设置Heroku环境变量"""
    config_vars = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'your-secret-key-here-change-in-production',
        'ADMIN_EMAIL': 'admin@yourdomain.com',
        'ADMIN_PASSWORD': 'your-admin-password-change-in-production'
    }
    
    try:
        print("正在设置环境变量...")
        for key, value in config_vars.items():
            subprocess.run(['heroku', 'config:set', f'{key}={value}', '-a', app_name], 
                          capture_output=True, text=True, check=True)
        print("✅ 环境变量设置成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 环境变量设置失败: {e.stderr}")
        return False

def deploy_to_heroku():
    """部署到Heroku"""
    try:
        print("正在部署到Heroku...")
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        print("✅ 部署成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失败: {e}")
        return False

def get_app_info(app_name):
    """获取应用信息"""
    try:
        result = subprocess.run(['heroku', 'info', '-a', app_name], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def main():
    print("🚀 开始部署到Heroku...")
    
    # 检查Heroku CLI
    if not check_heroku_cli():
        return
    
    # 登录Heroku
    if not login_heroku():
        return
    
    # 创建Heroku应用
    app_name = create_heroku_app()
    if not app_name:
        return
    
    print(f"应用查看: https://{app_name}.herokuapp.com")
    
    # 设置环境变量
    if not setup_heroku_config(app_name):
        return
    
    # 部署应用
    if not deploy_to_heroku():
        return
    
    # 显示应用信息
    print("\n" + "="*50)
    print("🎉 部署完成!")
    print("="*50)
    print(f"应用查看: https://{app_name}.herokuapp.com")
    print(f"管理后台: https://{app_name}.herokuapp.com/admin/login")
    print("\n重要提醒:")
    print("1. 请尽快登录管理后台修改默认管理员密码")
    print("2. 在生产环境中请设置安全的SECRET_KEY")
    print("3. 如需数据库持久化，请添加Heroku PostgreSQL插件")
    print("="*50)

if __name__ == '__main__':
    main()