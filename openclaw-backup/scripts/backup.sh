#!/bin/bash
# OpenClaw 备份脚本

set -e

# 配置
OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_DIR="$HOME/.openclaw-backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="openclaw-backup-$TIMESTAMP"
MAX_BACKUPS=7

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 创建备份目录
mkdir -p "$BACKUP_DIR"
CURRENT_BACKUP="$BACKUP_DIR/$BACKUP_NAME"
mkdir -p "$CURRENT_BACKUP"

log "开始备份 OpenClaw..."
log "备份目录: $CURRENT_BACKUP"

# 1. 备份工作区
if [ -d "$OPENCLAW_DIR/workspace" ]; then
    log "备份工作区..."
    tar -czf "$CURRENT_BACKUP/workspace.tar.gz" \
        --exclude='*.log' \
        --exclude='node_modules' \
        --exclude='.git' \
        -C "$OPENCLAW_DIR" workspace
    log "  ✓ workspace.tar.gz ($(du -h "$CURRENT_BACKUP/workspace.tar.gz" | cut -f1))"
else
    warn "工作区目录不存在，跳过"
fi

# 2. 备份主配置
if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
    log "备份主配置..."
    cp "$OPENCLAW_DIR/openclaw.json" "$CURRENT_BACKUP/"
    log "  ✓ openclaw.json"
fi

# 3. 备份凭据
if [ -d "$OPENCLAW_DIR/credentials" ]; then
    log "备份凭据..."
    tar -czf "$CURRENT_BACKUP/credentials.tar.gz" \
        -C "$OPENCLAW_DIR" credentials
    log "  ✓ credentials.tar.gz ($(du -h "$CURRENT_BACKUP/credentials.tar.gz" | cut -f1))"
fi

# 4. 备份环境变量
if [ -f "$OPENCLAW_DIR/.env" ]; then
    log "备份环境变量..."
    cp "$OPENCLAW_DIR/.env" "$CURRENT_BACKUP/"
    log "  ✓ .env"
fi

# 5. 备份 skills 目录列表（不备份内容，只记录有哪些）
if [ -d "$OPENCLAW_DIR/skills" ]; then
    log "记录已安装的 skills..."
    ls -1 "$OPENCLAW_DIR/skills" > "$CURRENT_BACKUP/installed-skills.txt" 2>/dev/null || true
    log "  ✓ installed-skills.txt"
fi

# 6. 生成备份信息
cat > "$CURRENT_BACKUP/BACKUP_INFO.txt" << INFO
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份主机: $(hostname)
OpenClaw 版本: $(openclaw --version 2>/dev/null || echo "未知")
工作区大小: $(du -sh "$OPENCLAW_DIR/workspace" 2>/dev/null | cut -f1 || echo "未知")
凭据数量: $(find "$OPENCLAW_DIR/credentials" -type f 2>/dev/null | wc -l)
已安装 Skills: $(ls -1 "$OPENCLAW_DIR/skills" 2>/dev/null | wc -l)
INFO

log "  ✓ BACKUP_INFO.txt"

# 7. 计算总大小
TOTAL_SIZE=$(du -sh "$CURRENT_BACKUP" | cut -f1)
log "备份完成！总大小: $TOTAL_SIZE"

# 8. 清理旧备份
log "清理旧备份（保留最近 $MAX_BACKUPS 个）..."
cd "$BACKUP_DIR"
ls -t | grep "^openclaw-backup-" | tail -n +$((MAX_BACKUPS + 1)) | while read old; do
    rm -rf "$old"
    log "  已删除: $old"
done

echo ""
log "当前备份列表:"
ls -t | grep "^openclaw-backup-" | head -5 | while read b; do
    size=$(du -sh "$BACKUP_DIR/$b" | cut -f1)
    echo "  - $b ($size)"
done
