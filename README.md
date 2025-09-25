# 信息收集系统

一个功能完整的在线信息收集平台，支持动态表单创建、文件上传、支付集成等功能。适用于学校、企业等组织进行高效的数据采集和管理。

## 📋 功能特性

### 🎯 核心功能
- **动态表单创建**：支持多种字段类型（文本、数字、日期、选择框、文件上传等）
- **用户管理**：完整的用户注册/登录系统，支持邮箱或手机号登录
- **文件上传**：支持图片、视频、文档等多种文件格式
- **数据导出**：支持Excel、CSV、ZIP等多种导出格式
- **响应式设计**：适配PC端和移动端设备

### 💳 支付功能
- **多种支付方式**：集成微信支付、支付宝支付
- **收款账户管理**：支持多个收款账户配置
- **支付订单管理**：完整的支付流程和订单状态跟踪
- **支付统计**：详细的收入统计和分析

### 🔐 安全特性
- **权限管理**：区分普通用户和管理员权限
- **密码加密**：使用bcrypt加密存储密码
- **文件安全**：上传文件类型验证和大小限制
- **会话管理**：安全的用户会话控制

## 🚀 快速开始

### 环境要求
- Python 3.7+
- pip 包管理器
- SQLite（默认数据库）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd 网站
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **环境配置**
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量（重要！）
# 修改 SECRET_KEY、ADMIN_EMAIL、ADMIN_PASSWORD 等配置
```

4. **启动应用**
```bash
# 开发环境启动
python run.py

# 或者使用
python app.py
```

5. **访问应用**
- 用户端：http://localhost:5000
- 管理员登录：http://localhost:5000/admin/login

### 默认账户

#### 管理员账户
- 邮箱：admin@demo.com
- 密码：admin123

> **⚠️ 安全提醒：** 首次部署时请立即修改默认管理员密码！

## 🐳 Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Dockerfile

```bash
# 构建镜像
docker build -t form-system .

# 运行容器
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/form_system.db:/app/form_system.db \
  form-system
```

## 📁 项目结构

```
网站/
├── app.py                 # 主应用入口文件
├── run.py                 # 启动脚本
├── config.py              # 配置文件
├── models.py              # 数据库模型定义
├── forms.py               # WTForms表单类
├── payment_config.py      # 支付配置模块
├── requirements.txt       # Python依赖列表
├── Dockerfile            # Docker镜像构建文件
├── docker-compose.yml    # 多容器编排配置
├── .env.example          # 环境变量模板
├── README.md             # 项目说明文档
├── templates/            # Jinja2模板文件
│   ├── admin/           # 管理端页面
│   ├── user/            # 用户端页面
│   ├── auth/            # 登录注册页面
│   └── base.html        # 基础模板
├── static/              # 静态资源
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript文件
│   └── images/         # 图片资源
├── uploads/             # 用户上传文件存储目录
└── instance/           # 实例配置目录
    └── form_system.db   # SQLite数据库文件
```

## 🔧 配置说明

### 环境变量配置

创建 `.env` 文件并配置以下变量：

```env
# 应用配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DEBUG=True

# 数据库配置
DATABASE_URL=sqlite:///form_system.db

# 管理员账号配置
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=your-secure-password

# 文件上传配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=104857600  # 100MB

# 支付配置（可选）
WECHAT_APP_ID=your_wechat_app_id
WECHAT_MCH_ID=your_merchant_id
ALIPAY_APP_ID=your_alipay_app_id
```

### 支付配置

如需使用支付功能，请配置相应的支付参数：

1. **微信支付**：需要配置APP_ID、商户号、API密钥等
2. **支付宝**：需要配置APP_ID、应用私钥、支付宝公钥等

详细配置请参考 `payment_config.py` 文件。

## 📖 使用指南

### 管理员操作

1. **登录管理后台**
   - 访问 `/admin/login`
   - 使用管理员账户登录

2. **创建表单**
   - 进入"表单管理"
   - 点击"创建表单"
   - 配置表单字段和属性

3. **管理提交记录**
   - 查看用户提交的数据
   - 审核和管理提交状态
   - 导出数据报表

4. **用户管理**
   - 查看注册用户列表
   - 管理用户状态

### 用户操作

1. **注册登录**
   - 支持邮箱或手机号注册
   - 安全的密码验证

2. **填写表单**
   - 浏览可用表单
   - 在线填写和提交
   - 上传附件文件

3. **查看记录**
   - 查看自己的提交历史
   - 跟踪提交状态

## 🛠️ 开发指南

### 技术栈

- **后端**：Python Flask 2.3.3
- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **数据库**：SQLite（默认）/ PostgreSQL / MySQL
- **ORM**：SQLAlchemy
- **认证**：Flask-Login
- **表单**：WTForms

### 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=1

# 运行开发服务器
flask run
```

### 数据库管理

```bash
# 初始化数据库
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"

# 创建管理员用户
python -c "from app import create_app; from models import db, Admin; app = create_app(); app.app_context().push(); admin = Admin(name='管理员', email='admin@example.com'); admin.set_password('admin123'); db.session.add(admin); db.session.commit()"
```

## 🚦 API 文档

### 主要 API 端点

#### 用户相关
- `POST /login` - 用户登录
- `POST /register` - 用户注册
- `GET /logout` - 用户登出

#### 表单相关
- `GET /form/<id>` - 查看表单
- `POST /form/<id>` - 提交表单
- `GET /submission/<id>` - 查看提交记录

#### 管理员相关
- `GET /admin/forms` - 表单管理
- `GET /admin/users` - 用户管理
- `GET /admin/export/forms/<id>` - 导出表单数据

## 🔒 安全建议

1. **生产环境部署**
   - 更改默认密码
   - 设置强密钥
   - 启用HTTPS
   - 配置防火墙

2. **数据库安全**
   - 定期备份数据
   - 限制数据库访问权限
   - 监控异常操作

3. **文件上传安全**
   - 验证文件类型
   - 限制文件大小
   - 扫描恶意文件

## 📊 性能优化

### 推荐配置

- **内存**：1GB以上
- **存储**：根据上传文件需求调整
- **并发**：使用Gunicorn部署多进程

### 生产环境部署

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# 使用Nginx反向代理
# 配置SSL证书
# 设置静态文件缓存
```

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库文件权限
   - 确认数据库路径正确

2. **文件上传失败**
   - 检查uploads目录权限
   - 确认文件大小限制

3. **支付功能异常**
   - 验证支付配置参数
   - 检查网络连接

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# Docker环境查看日志
docker-compose logs -f app
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 技术支持

- **问题反馈**：请通过 GitHub Issues 提交
- **技术讨论**：欢迎在 Discussions 中交流
- **安全问题**：请私信联系维护者

## 🔄 更新日志

### v1.0.0 (2025-01-20)
- ✨ 初始版本发布
- 🎯 完整的表单管理功能
- 💳 集成支付系统
- 📱 响应式界面设计
- 🔐 用户权限管理
- 📊 数据导出功能

---

**感谢您使用信息收集系统！** 如果您觉得这个项目对您有帮助，请给我们一个 ⭐️