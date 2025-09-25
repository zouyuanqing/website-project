# Heroku 部署指南

本指南将帮助您将网站项目部署到 Heroku 平台，实现远程访问。

## 前置要求

1. 注册 [Heroku](https://www.heroku.com/) 账户
2. 安装 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. 安装 [Git](https://git-scm.com/)

## 部署步骤

### 1. 安装 Heroku CLI

访问 [Heroku CLI 下载页面](https://devcenter.heroku.com/articles/heroku-cli) 下载并安装适用于 Windows 的版本。

安装完成后，在命令行中验证安装：
```bash
heroku --version
```

### 2. 登录 Heroku

```bash
heroku login
```

这将打开浏览器窗口，要求您登录 Heroku 账户。

### 3. 创建 Heroku 应用

```bash
heroku create your-app-name
```

如果不指定应用名称，Heroku 会自动生成一个唯一的名称。

### 4. 设置环境变量

```bash
heroku config:set FLASK_ENV=production -a your-app-name
heroku config:set SECRET_KEY=your-secret-key-here-change-in-production -a your-app-name
heroku config:set ADMIN_EMAIL=admin@yourdomain.com -a your-app-name
heroku config:set ADMIN_PASSWORD=your-admin-password-change-in-production -a your-app-name
```

### 5. 部署应用

```bash
git push heroku main
```

### 6. 运行数据库迁移

```bash
heroku run python -c "from app import create_app; from models import db; app=create_app(); with app.app_context(): db.create_all()" -a your-app-name
```

## 访问您的应用

部署完成后，您可以通过以下 URL 访问您的应用：

- 应用主页: `https://your-app-name.herokuapp.com`
- 用户登录: `https://your-app-name.herokuapp.com/login`
- 用户注册: `https://your-app-name.herokuapp.com/register`
- 管理后台: `https://your-app-name.herokuapp.com/admin/login`

默认管理员账户:
- 邮箱: `admin@yourdomain.com`
- 密码: `your-admin-password-change-in-production`

## 注意事项

1. **安全性**: 部署到生产环境前，请务必修改默认的 SECRET_KEY 和管理员密码
2. **数据库**: Heroku 的文件系统是临时的，SQLite 数据库会在应用重启时丢失。建议使用 Heroku PostgreSQL 插件
3. **文件上传**: 上传的文件也会在应用重启时丢失。建议使用 AWS S3 或其他云存储服务

## 添加 PostgreSQL 数据库（推荐）

```bash
heroku addons:create heroku-postgresql:hobby-dev -a your-app-name
```

Heroku 会自动设置 DATABASE_URL 环境变量，应用已经配置为自动使用这个变量。

## 故障排除

### 查看日志

```bash
heroku logs --tail -a your-app-name
```

### 重启应用

```bash
heroku restart -a your-app-name
```

### 进入应用的命令行

```bash
heroku run bash -a your-app-name
```