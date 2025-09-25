#!/bin/bash

# 信息收集系统启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_title() {
    echo -e "${BLUE}$1${NC}"
}

# 检查Python环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi
    
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_info "Python版本: $python_version"
}

# 检查依赖
check_dependencies() {
    print_info "检查Python依赖包..."
    
    missing_packages=()
    
    # 检查主要依赖包
    packages=("flask" "flask_sqlalchemy" "flask_login" "flask_wtf" "werkzeug")
    
    for package in "${packages[@]}"; do
        if ! python3 -c "import $package" &> /dev/null; then
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        print_error "缺少依赖包: ${missing_packages[*]}"
        print_info "正在安装依赖包..."
        pip3 install -r requirements.txt
    else
        print_info "依赖包检查完成"
    fi
}

# 检查数据库
check_database() {
    print_info "检查数据库..."
    
    if [ ! -f "form_system.db" ]; then
        print_warning "数据库文件不存在，将自动创建"
    else
        print_info "数据库文件存在"
    fi
}

# 检查配置文件
check_config() {
    print_info "检查配置文件..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env文件不存在，使用默认配置"
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_info "已从示例文件创建.env"
        fi
    else
        print_info "配置文件存在"
    fi
}

# 创建必要目录
create_directories() {
    print_info "创建必要目录..."
    
    directories=("uploads" "instance" "logs")
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_info "创建目录: $dir"
        fi
    done
}

# 显示系统信息
show_system_info() {
    print_title "🚀 信息收集系统"
    echo "=================================="
    echo "项目目录: $(pwd)"
    echo "Python版本: $(python3 --version 2>&1)"
    echo "启动时间: $(date)"
    echo "=================================="
    echo ""
}

# 启动应用
start_application() {
    local mode=${1:-"development"}
    
    case $mode in
        "dev"|"development")
            print_info "启动开发服务器..."
            python3 run.py
            ;;
        "prod"|"production")
            print_info "启动生产服务器..."
            if command -v gunicorn &> /dev/null; then
                gunicorn -c gunicorn.conf.py wsgi:application
            else
                print_warning "Gunicorn未安装，使用开发服务器"
                FLASK_ENV=production python3 run.py
            fi
            ;;
        *)
            print_error "未知模式: $mode"
            echo "使用方法: $0 [dev|prod]"
            exit 1
            ;;
    esac
}

# 显示帮助信息
show_help() {
    echo "信息收集系统启动脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 [模式] [选项]"
    echo ""
    echo "模式:"
    echo "  dev, development    开发模式 (默认)"
    echo "  prod, production    生产模式"
    echo ""
    echo "选项:"
    echo "  -h, --help         显示帮助信息"
    echo "  -c, --check        仅检查环境，不启动"
    echo "  -v, --version      显示版本信息"
    echo ""
    echo "示例:"
    echo "  $0                 # 开发模式启动"
    echo "  $0 prod            # 生产模式启动"
    echo "  $0 --check         # 仅检查环境"
}

# 主函数
main() {
    local mode="development"
    local check_only=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--check)
                check_only=true
                shift
                ;;
            -v|--version)
                echo "信息收集系统 v1.0.0"
                exit 0
                ;;
            dev|development)
                mode="development"
                shift
                ;;
            prod|production)
                mode="production"
                shift
                ;;
            *)
                print_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 显示系统信息
    show_system_info
    
    # 环境检查
    check_python
    check_dependencies
    check_database
    check_config
    create_directories
    
    if [ "$check_only" = true ]; then
        print_info "环境检查完成，程序退出"
        exit 0
    fi
    
    # 启动应用
    echo ""
    print_info "访问地址:"
    echo "  🌐 用户端: http://localhost:5000"
    echo "  ⚙️ 管理端: http://localhost:5000/admin/login"
    echo "  📧 默认管理员: admin@system.com"
    echo "  🔑 默认密码: admin123"
    echo ""
    print_warning "按 Ctrl+C 停止服务器"
    echo ""
    
    # 捕获退出信号
    trap 'echo -e "\n👋 服务器已停止"; exit 0' INT TERM
    
    start_application "$mode"
}

# 检查是否在正确目录
if [ ! -f "app.py" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 运行主函数
main "$@"
