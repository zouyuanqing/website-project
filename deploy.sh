#!/bin/bash

# 信息收集系统部署脚本
# 自动化部署到生产环境

set -e  # 遇到错误立即退出

echo "🚀 开始部署信息收集系统..."

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印彩色信息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查Python版本
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version="3.7"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        print_error "Python版本过低，需要3.7+，当前版本: $python_version"
        exit 1
    fi
    
    print_info "Python版本检查通过: $python_version"
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 未安装"
        exit 1
    fi
    
    print_info "系统要求检查完成"
}

# 创建虚拟环境
create_venv() {
    print_info "创建Python虚拟环境..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_info "虚拟环境创建完成"
    else
        print_warning "虚拟环境已存在，跳过创建"
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    print_info "虚拟环境已激活"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖包..."
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    pip install -r requirements.txt
    
    print_info "依赖包安装完成"
}

# 配置环境变量
setup_environment() {
    print_info "配置环境变量..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env文件不存在，从模板创建..."
        cp .env.example .env
        
        # 生成随机密钥
        secret_key=$(python3 -c "import secrets; print(secrets.token_hex(32))")
        sed -i "s/your-secret-key-change-in-production/$secret_key/" .env
        
        print_warning "请编辑 .env 文件，修改管理员账号等配置"
        print_warning "默认管理员: admin@system.com / admin123"
    else
        print_info "环境配置文件已存在"
    fi
}

# 初始化数据库
init_database() {
    print_info "初始化数据库..."
    
    # 创建必要目录
    mkdir -p uploads
    mkdir -p instance
    
    # 设置目录权限
    chmod 755 uploads
    chmod 755 instance
    
    print_info "数据库初始化完成"
}

# 安装系统服务 (可选)
install_service() {
    read -p "是否安装为系统服务？(y/N): " install_service
    
    if [[ $install_service =~ ^[Yy]$ ]]; then
        print_info "安装系统服务..."
        
        # 获取当前目录
        current_dir=$(pwd)
        current_user=$(whoami)
        
        # 创建服务文件
        cat > /tmp/form-system.service << EOF
[Unit]
Description=Form Collection System
After=network.target

[Service]
Type=simple
User=$current_user
WorkingDirectory=$current_dir
Environment=PATH=$current_dir/venv/bin
ExecStart=$current_dir/venv/bin/python run.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
        
        # 安装服务
        sudo mv /tmp/form-system.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable form-system
        
        print_info "系统服务安装完成"
        print_info "启动服务: sudo systemctl start form-system"
        print_info "查看状态: sudo systemctl status form-system"
        print_info "查看日志: sudo journalctl -u form-system -f"
    fi
}

# 安装Nginx配置 (可选)
install_nginx() {
    read -p "是否配置Nginx反向代理？(y/N): " install_nginx
    
    if [[ $install_nginx =~ ^[Yy]$ ]]; then
        print_info "配置Nginx..."
        
        read -p "请输入域名 (例: example.com): " domain_name
        
        if [ -z "$domain_name" ]; then
            print_error "域名不能为空"
            return
        fi
        
        # 创建Nginx配置
        cat > /tmp/form-system-nginx.conf << EOF
server {
    listen 80;
    server_name $domain_name;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /uploads/ {
        alias $(pwd)/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /static/ {
        alias $(pwd)/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
        
        print_info "Nginx配置文件已生成: /tmp/form-system-nginx.conf"
        print_warning "请手动将配置文件复制到Nginx配置目录"
        print_warning "sudo cp /tmp/form-system-nginx.conf /etc/nginx/sites-available/form-system"
        print_warning "sudo ln -s /etc/nginx/sites-available/form-system /etc/nginx/sites-enabled/"
        print_warning "sudo nginx -t && sudo systemctl reload nginx"
    fi
}

# 创建启动脚本
create_startup_script() {
    print_info "创建启动脚本..."
    
    cat > start.sh << 'EOF'
#!/bin/bash
# 启动脚本

cd "$(dirname "$0")"

# 激活虚拟环境
source venv/bin/activate

# 启动应用
python run.py
EOF
    
    chmod +x start.sh
    
    print_info "启动脚本创建完成: ./start.sh"
}

# 显示部署结果
show_result() {
    echo ""
    echo "🎉 部署完成！"
    echo "=================================="
    print_info "系统信息:"
    echo "  📁 项目目录: $(pwd)"
    echo "  🐍 Python版本: $(python3 --version)"
    echo "  📝 配置文件: .env"
    echo ""
    print_info "启动方式:"
    echo "  1. 直接启动: ./start.sh"
    echo "  2. 虚拟环境: source venv/bin/activate && python run.py"
    if systemctl is-enabled form-system &>/dev/null; then
        echo "  3. 系统服务: sudo systemctl start form-system"
    fi
    echo ""
    print_info "访问地址:"
    echo "  🌐 用户端: http://localhost:5000"
    echo "  ⚙️ 管理端: http://localhost:5000/admin/login"
    echo ""
    print_warning "重要提醒:"
    echo "  1. 请修改 .env 文件中的管理员密码"
    echo "  2. 生产环境请配置HTTPS"
    echo "  3. 定期备份数据库文件"
    echo "=================================="
}

# 主函数
main() {
    echo "信息收集系统自动部署脚本"
    echo "========================="
    
    # 检查是否在正确目录
    if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
        print_error "请在项目根目录运行此脚本"
        exit 1
    fi
    
    # 执行部署步骤
    check_requirements
    create_venv
    install_dependencies
    setup_environment
    init_database
    create_startup_script
    
    # 可选配置
    install_service
    install_nginx
    
    # 显示结果
    show_result
}

# 捕获Ctrl+C
trap 'echo -e "\n❌ 部署被中断"; exit 1' INT

# 运行主函数
main "$@"
