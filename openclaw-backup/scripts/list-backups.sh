#!/bin/bash
# 列出所有备份

BACKUP_DIR="$HOME/.openclaw-backups"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "备份目录不存在: $BACKUP_DIR"
    echo "还没有创建过备份"
    exit 0
fi

echo "OpenClaw 备份列表:"
echo "=================="
echo ""

count=0
for backup in $(ls -t "$BACKUP_DIR" | grep "^openclaw-backup-"); do
    count=$((count + 1))
    path="$BACKUP_DIR/$backup"
    size=$(du -sh "$path" 2>/dev/null | cut -f1)
    
    # 提取时间
    timestamp=$(echo "$backup" | sed 's/openclaw-backup-//')
    date_part=$(echo "$timestamp" | cut -d'-' -f1-3 | tr '-' '/')
    time_part=$(echo "$timestamp" | cut -d'-' -f4 | sed 's/\(..\)\(..\)\(..\)/\1:\2:\3/')
    
    echo "[$count] $backup"
    echo "    时间: $date_part $time_part"
    echo "    大小: $size"
    
    # 显示备份信息
    if [ -f "$path/BACKUP_INFO.txt" ]; then
        echo "    内容:"
        grep -E "^(工作区|凭据|Skills)" "$path/BACKUP_INFO.txt" 2>/dev/null | while read line; do
            echo "      $line"
        done
    fi
    echo ""
done

if [ $count -eq 0 ]; then
    echo "还没有创建过备份"
    echo ""
    echo "创建备份: ~/.openclaw/skills/openclaw-backup/scripts/backup.sh"
else
    echo "-------------------"
    echo "共 $count 个备份"
    echo ""
    echo "恢复备份: ~/.openclaw/skills/openclaw-backup/scripts/restore.sh <备份名>"
fi
