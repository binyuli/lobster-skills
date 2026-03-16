---
name: openclaw-backup
description: 备份和恢复 OpenClaw 配置、工作区和凭据。使用场景：(1) 定期备份 OpenClaw 数据 (2) 更新前备份 (3) 迁移到新服务器 (4) 恢复到之前的备份。
---

# OpenClaw 备份技能

简单实用的 OpenClaw 备份工具。

## 备份内容

| 文件/目录 | 说明 |
|-----------|------|
| `~/.openclaw/workspace/` | 工作区（MEMORY.md、配置、memory/ 等） |
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/credentials/` | 凭据（WhatsApp、Telegram 等） |
| `~/.openclaw/.env` | 环境变量 |

## 使用方法

### 手动备份
```bash
~/.openclaw/skills/openclaw-backup/scripts/backup.sh
```

### 查看备份列表
```bash
~/.openclaw/skills/openclaw-backup/scripts/list-backups.sh
```

### 恢复备份
```bash
~/.openclaw/skills/openclaw-backup/scripts/restore.sh <备份目录>
```

### 设置定时备份
```bash
# 每天凌晨 3 点备份
echo "0 3 * * * ~/.openclaw/skills/openclaw-backup/scripts/backup.sh >> ~/.openclaw/logs/backup.log 2>&1" | crontab -
```

## 备份位置

所有备份存放在 `~/.openclaw-backups/` 目录下，格式：
```
~/.openclaw-backups/openclaw-backup-YYYYMMDD-HHMMSS/
├── workspace.tar.gz
├── openclaw.json
├── credentials.tar.gz
├── .env
└── BACKUP_INFO.txt
```

## 保留策略

默认保留最近 7 个备份，自动清理旧的。

## 注意事项

- 备份前会自动清理超过 7 天的旧备份
- 恢复前请先停止 OpenClaw gateway
- 恢复后需要重启 gateway
