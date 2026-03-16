#!/bin/bash
# OpenClaw 恢复脚本

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_DIR="$HOME/.openclaw-backups"

# 检查参数
if [ -z "$1" ]; then
    error "用法: $0 <备份目录>"
    echo ""
    echo "可用备份:"
    ls -t "$BACKUP_DIR" 2>/dev/null | grep "^openclaw-backup-" | head -5 | while read b; do
        echo "  - $b"
    done
    exit 1
fi

RESTORE_FROM="$1"

# 支持相对路径
if [[ "$RESTORE_FROM" != /* ]]; then
    RESTORE_FROM="$BACKUP_DIR/$RESTORE_FROM"
fi

if [ ! -d "$RESTORE_FROM" ]; then
    error "备份目录不存在: $RESTORE_FROM"
    exit 1
fi

echo ""
warn "=========================================="
warn "  即将从备份恢复 OpenClaw"
warn "  这将覆盖当前配置和工作区！"
warn "=========================================="
echo ""
echo "备份来源: $RESTORE_FROM"
if [ -f "$RESTORE_FROM/BACKUP_INFO.txt" ]; then
    echo ""
    cat "$RESTORE_FROM/BACKUP_INFO.txt"
fi
echo ""
read -p "确认恢复? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "已取消"
    exit 0
fi

log "开始恢复..."

# 1. 停止 gateway（如果在运行）
if pgrep -f "openclaw gateway" > /dev/null; then
    log "停止 OpenClaw gateway..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

# 2. 恢复工作区
if [ -f "$RESTORE_FROM/workspace.tar.gz" ]; then
    log "恢复工作区..."
    # 先备份当前工作区（以防万一）
    if [ -d "$OPENCLAW_DIR/workspace" ]; then
        mv "$OPENCLAW_DIR/workspace" "$OPENCLAW_DIR/workspace.bak.$(date +%s)"
    fi
    tar -xzf "$RESTORE_FROM/workspace.tar.gz" -C "$OPENCLAW_DIR"
    log "  ✓ 工作区已恢复"
fi

# 3. 恢复主配置
if [ -f "$RESTORE_FROM/openclaw.json" ]; then
    log "恢复主配置..."
    cp "$RESTORE_FROM/openclaw.json" "$OPENCLAW_DIR/"
    log "  ✓ openclaw.json 已恢复"
fi

# 4. 恢复凭据
if [ -f "$RESTORE_FROM/credentials.tar.gz" ]; then
    log "恢复凭据..."
    tar -xzf "$RESTORE_FROM/credentials.tar.gz" -C "$OPENCLAW_DIR"
    log "  ✓ 凭据已恢复"
fi

# 5. 恢复环境变量
if [ -f "$RESTORE_FROM/.env" ]; then
    log "恢复环境变量..."
    cp "$RESTORE_FROM/.env" "$OPENCLAW_DIR/"
    log "  ✓ .env 已恢复"
fi

log "恢复完成！"
echo ""
warn "请手动重启 OpenClaw gateway:"
echo "  openclaw gateway start"
