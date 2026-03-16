---
name: image-search
description: 搜索网络图片并下载。使用搜狗/百度图片搜索，无需 API key。支持搜索动漫、人物、风景等任何图片。
---

# Image Search Skill

搜索网络图片，无需 API key。

## 快速使用

```bash
# 搜索图片
python3 ~/.openclaw/skills/image-search/scripts/image_search.py search "韩立 凡人修仙传" --count 5

# 下载图片
python3 ~/.openclaw/skills/image-search/scripts/image_search.py download "<图片URL>" --output image.jpg
```

## 命令

### search - 搜索图片

```bash
image_search.py search <关键词> [--count N]
```

- `--count` 返回图片数量，默认 10

### download - 下载图片

```bash
image_search.py download <URL> --output <文件名>
```

## 示例

```bash
# 搜索动漫角色
image_search.py search "韩立 凡人修仙传" --count 5

# 搜索风景
image_search.py search "富士山 日落" --count 3

# 下载第一张
image_search.py download "https://example.com/image.jpg" --output photo.jpg
```

## 数据源

- 搜狗图片（主要）
- 百度图片（备选）

## 注意

- 搜索结果可能受版权保护，仅供个人使用
- 部分图片可能无法下载（防盗链）
