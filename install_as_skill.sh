#!/bin/bash

##############################################################################
# gpt-image2-ppt-skills -- Claude ​Code Skill 安装脚本
#
# 把当前仓库内容拷贝到 ~/.claude/skills/gpt-image2-ppt-skills/
# 并安装 Python 依赖、引导配置 .env。
#
# 用法：bash install_as_skill.sh
##############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info()    { echo -e "${BLUE}(i)  $1${NC}"; }
print_success() { echo -e "${GREEN}[OK] $1${NC}"; }
print_warning() { echo -e "${YELLOW}(!)  $1${NC}"; }
print_error()   { echo -e "${RED}[X] $1${NC}"; }
print_header()  { echo ""; echo "========================================"; echo "$1"; echo "========================================"; echo ""; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

main() {
    print_header "gpt-image2-ppt-skills -- 安装"

    SKILL_DIR="$HOME/.claude/skills/gpt-image2-ppt-skills"
    print_info "目标目录: $SKILL_DIR"

    if [ -d "$SKILL_DIR" ]; then
        print_warning "Skill 目录已存在: $SKILL_DIR"
        read -p "是否覆盖？(y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "取消"
            exit 0
        fi
        # 备份用户的 .env
        if [ -f "$SKILL_DIR/.env" ]; then
            cp "$SKILL_DIR/.env" "/tmp/gpt-image2-ppt.env.bak"
            print_info "已备份现有 .env 到 /tmp/gpt-image2-ppt.env.bak"
        fi
        rm -rf "$SKILL_DIR"
    fi

    print_info "创建 Skill 目录..."
    mkdir -p "$SKILL_DIR"
    print_success "目录已创建"

    print_info "复制项目文件..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # 拷贝核心文件，排除 .git / outputs / venv / .env / __pycache__
    rsync -a \
        --exclude='.git' \
        --exclude='outputs' \
        --exclude='venv' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='.env' \
        "$SCRIPT_DIR/" "$SKILL_DIR/"

    print_success "文件复制完成"

    # 恢复备份的 .env
    if [ -f "/tmp/gpt-image2-ppt.env.bak" ]; then
        mv "/tmp/gpt-image2-ppt.env.bak" "$SKILL_DIR/.env"
        print_success "已恢复用户 .env"
    fi

    print_info "检查 Python 环境..."
    if ! command_exists python3; then
        print_error "未找到 python3，请先安装 Python 3.8+"
        exit 1
    fi
    print_success "Python: $(python3 --version)"

    print_info "安装 Python 依赖..."
    if command_exists pip3; then
        pip3 install -q -r "$SKILL_DIR/requirements.txt"
    else
        pip install -q -r "$SKILL_DIR/requirements.txt"
    fi
    print_success "依赖安装完成（requests + python-dotenv）"

    print_header "配置 API 密钥"

    if [ -f "$SKILL_DIR/.env" ]; then
        print_info "已存在 .env，跳过"
    else
        cp "$SKILL_DIR/.env.example" "$SKILL_DIR/.env"
        print_success "已生成 $SKILL_DIR/.env"
        print_warning "请编辑该文件填入 OPENAI_API_KEY："
        print_info "  nano $SKILL_DIR/.env"
    fi

    print_header "安装完成"

    print_success "已装到 $SKILL_DIR"
    echo ""
    print_info "下一步："
    print_info "  1. 编辑 .env 填 API key:  nano $SKILL_DIR/.env"
    print_info "  2. 重启 Claude ​Code 让 skill 生效"
    print_info "  3. 直接对 Claude 说：'帮我用 gpt-image2-ppt 生成一份 5 页 PPT'"
    echo ""
    print_info "冒烟测试（可选）："
    print_info "  cd $SKILL_DIR"
    print_info "  python3 scripts/generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --slides 1"
    echo ""
}

trap 'print_error "安装过程出错"; exit 1' ERR

main
