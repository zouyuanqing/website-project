# 信息收集系统 - 部署包说明

## 📦 完整的项目文件清单

### 核心应用文件
- `app.py` - Flask主应用文件，包含所有路由和核心逻辑
- `run.py` - 应用启动脚本，包含数据库初始化
- `wsgi.py` - WSGI入口文件，用于生产环境部署
- `config.py` - 应用配置文件
- `models.py` - 数据库模型定义
- `forms.py` - 表单类定义和验证

### 前端文件
- `templates/` - HTML模板目录
  - `base.html` - 基础模板
  - `index.html` - 首页
  - `auth/` - 用户认证页面
  - `user/` - 用户功能页面  
  - `admin/` - 管理员页面
- `static/` - 静态资源目录
  - `css/style.css` - 自定义样式
  - `js/script.js` - JavaScript功能

### 部署配置文件
- `requirements.txt` - Python依赖包列表
- `Dockerfile` - Docker容器构建文件
- `docker-compose.yml` - Docker Compose配置
- `gunicorn.conf.py` - Gunicorn生产服务器配置
- `.env.example` - 环境变量配置模板
- `.gitignore` - Git忽略文件配置

### 脚本工具
- `start.sh` - 智能启动脚本，支持开发/生产模式
- `deploy.sh` - 自动化部署脚本

### 文档
- `README.md` - 完整的项目说明文档
- `DEPLOYMENT.md` - 本文件，部署说明

## 🚀 快速部署指南

### 方式一：一键部署 (推荐)
```bash
# 1. 解压项目到目标目录
unzip form-system.zip
cd form-system

# 2. 运行自动部署脚本
chmod +x deploy.sh
./deploy.sh

# 3. 启动系统
./start.sh
```

### 方式二：手动部署
```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，修改必要配置

# 3. 启动应用
python run.py
```

### 方式三：Docker部署
```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 🔧 系统配置

### 默认账号信息
- **管理员邮箱**: admin@system.com
- **管理员密码**: admin123
- **首次部署后请立即修改密码**

### 访问地址
- **用户端**: http://localhost:5000
- **管理后台**: http://localhost:5000/admin/login

### 重要目录
- `instance/uploads/` - 文件上传存储目录
- `form_system.db` - SQLite数据库文件
- `logs/` - 日志文件目录（生产环境）

## 🏫 学校服务器部署建议

### 1. 环境准备
```bash
# 安装Python 3.7+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 创建应用用户（可选）
sudo useradd -m -s /bin/bash formapp
sudo su - formapp
```

### 2. 项目部署
```bash
# 上传项目文件
scp -r form-system/ user@server:/home/formapp/

# 进入项目目录
cd /home/formapp/form-system/

# 运行部署脚本
chmod +x deploy.sh start.sh
./deploy.sh
```

### 3. 系统服务配置
部署脚本会提示是否安装为系统服务，选择"是"可以：
- 开机自启动
- 自动重启故障恢复
- 系统日志记录

### 4. Nginx反向代理（推荐）
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /uploads/ {
        alias /home/formapp/form-system/instance/uploads/;
        expires 1y;
    }
    
    location /static/ {
        alias /home/formapp/form-system/static/;
        expires 1y;
    }
}
```

## 🔒 安全配置

### 1. 修改默认密码
首次登录管理后台后，立即修改管理员密码

### 2. 配置HTTPS
生产环境建议使用SSL证书：
```bash
# 使用Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 文件权限设置
```bash
# 设置合适的文件权限
chmod 755 /home/formapp/form-system/
chmod 755 /home/formapp/form-system/instance/uploads/
chmod 600 /home/formapp/form-system/.env
```

### 4. 防火墙配置
```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📊 系统监控

### 1. 日志查看
```bash
# 应用日志
tail -f logs/error.log
tail -f logs/access.log

# 系统服务日志
sudo journalctl -u form-system -f
```

### 2. 性能监控
```bash
# 查看进程状态
sudo systemctl status form-system

# 查看资源使用
htop
df -h
```

### 3. 数据库备份
```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
backup_dir="/home/formapp/backups"
mkdir -p $backup_dir
cp form_system.db "$backup_dir/form_system_$(date +%Y%m%d_%H%M%S).db"
tar -czf "$backup_dir/uploads_$(date +%Y%m%d_%H%M%S).tar.gz" instance/uploads/
# 保留最近30天的备份
find $backup_dir -name "*.db" -mtime +30 -delete
find $backup_dir -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# 添加到定时任务
crontab -e
# 添加：0 2 * * * /home/formapp/form-system/backup.sh
```

## 🔧 故障排除

### 1. 应用无法启动
```bash
# 检查依赖
pip list | grep -i flask

# 检查配置
cat .env

# 查看详细错误
python run.py
```

### 2. 数据库问题
```bash
# 重新初始化数据库
rm form_system.db
python run.py
```

### 3. 文件上传失败
```bash
# 检查上传目录权限
ls -la instance/uploads/
chmod 755 instance/uploads/
```

### 4. 端口占用
```bash
# 查看端口使用
sudo netstat -tlnp | grep :5000

# 停止占用进程
sudo pkill -f "python run.py"
```

## 📞 技术支持

遇到问题时，请提供以下信息：
1. 操作系统版本
2. Python版本
3. 错误日志
4. 部署步骤

联系方式：
- 📧 邮箱：support@example.com
- 🐛 GitHub Issues
- 📚 项目文档：README.md

## ✅ 部署检查清单

### 部署前检查
- [ ] Python 3.7+ 已安装
- [ ] 服务器资源充足（CPU 1核+，内存 1GB+，磁盘 1GB+）
- [ ] 网络连接正常
- [ ] 域名解析配置（如需要）

### 部署后检查
- [ ] 应用正常启动
- [ ] 数据库初始化成功
- [ ] 管理员账号可以登录
- [ ] 用户注册功能正常
- [ ] 表单创建和提交功能正常
- [ ] 文件上传功能正常
- [ ] 日志记录正常

### 安全检查
- [ ] 默认密码已修改
- [ ] 环境变量配置正确
- [ ] 文件权限设置合适
- [ ] 防火墙规则配置
- [ ] HTTPS证书配置（生产环境）

### 性能检查
- [ ] 响应时间正常
- [ ] 内存使用合理
- [ ] 磁盘空间充足
- [ ] 数据备份策略已设置

---

🎉 **恭喜！您的信息收集系统已成功部署！**

如有任何问题，请查阅 README.md 或联系技术支持。
