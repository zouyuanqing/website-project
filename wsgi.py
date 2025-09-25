#!/usr/bin/env python3
"""
WSGI入口文件
用于Gunicorn或其他WSGI服务器
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from app import create_app
from models import db, Admin
from config import Config

# 创建应用实例
application = create_app()

# 初始化数据库
with application.app_context():
    try:
        db.create_all()
        
        # 创建默认管理员
        admin = Admin.query.filter_by(email=Config.ADMIN_EMAIL).first()
        if not admin:
            admin = Admin(
                email=Config.ADMIN_EMAIL,
                name='系统管理员'
            )
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print(f"默认管理员账号已创建: {Config.ADMIN_EMAIL}")
        
        # 创建上传目录
        upload_dir = os.path.join(application.instance_path, application.config['UPLOAD_FOLDER'])
        os.makedirs(upload_dir, exist_ok=True)
        
        print("应用初始化完成")
        
    except Exception as e:
        print(f"应用初始化失败: {e}")

# Heroku特定设置
if 'DYNO' in os.environ:
    # 在Heroku上运行，设置日志输出到stdout
    import logging
    from logging import StreamHandler
    handler = StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)

if __name__ == "__main__":
    # 获取端口（Heroku动态分配）
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)