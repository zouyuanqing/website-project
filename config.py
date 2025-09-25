import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # 数据库配置 - 支持Heroku PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # 修复Heroku PostgreSQL URL格式问题
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or os.environ.get('DATABASE_URL') or 'sqlite:///form_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传设置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 默认100MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'}
    
    # Session设置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=int(os.environ.get('SESSION_LIFETIME_HOURS', 24)))
    
    # 管理员默认账号（生产环境必须通过环境变量设置）
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@system.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # 应用环境
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # Heroku特定配置
    if 'DYNO' in os.environ:
        # 在Heroku上运行
        FLASK_ENV = 'production'
        DEBUG = False
    
    @staticmethod
    def validate_production_config():
        """验证生产环境配置"""
        if Config.FLASK_ENV == 'production':
            issues = []
            
            if Config.SECRET_KEY == 'dev-key-change-in-production':
                issues.append("生产环境必须设置安全的SECRET_KEY")
            
            if len(Config.SECRET_KEY) < 32:
                issues.append("SECRET_KEY长度至少需要32个字符")
            
            if Config.ADMIN_PASSWORD == 'admin123':
                issues.append("生产环境必须修改默认管理员密码")
            
            if Config.DEBUG:
                issues.append("生产环境必须关闭DEBUG模式")
            
            if issues:
                raise ValueError(f"生产环境配置错误:\n" + "\n".join(f"- {issue}" for issue in issues))
        
        return True