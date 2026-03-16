#!/usr/bin/env python3
"""
简易图片搜索 - 直接爬取搜索引擎结果
"""
import sys
import json
import urllib.parse
import urllib.request
import re
import os

#!/usr/bin/env python3
"""
简易图片搜索 - 直接爬取搜索引擎结果
"""
import sys
import json
import urllib.parse
import urllib.request
import re
import os
import ssl

# 忽略 SSL 证书验证（某些网站需要）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def search_baidu_images(query, count=5):
    """搜索百度图片"""
    encoded = urllib.parse.quote(query)
    url = f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.baidu.com/",
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        return {"error": str(e), "source": "baidu"}
    
    # 百度图片的数据在 data-imgurl 或 JSON 中
    patterns = [
        r'data-imgurl["\s]*=["\s]*["\']([^"\']+)["\']',
        r'"objURL":"([^"]+)"',
        r'"hoverURL":"([^"]+)"',
        r'data-objurl="([^"]+)"',
    ]
    
    all_matches = []
    for pattern in patterns:
        all_matches.extend(re.findall(pattern, html))
    
    # 去重并过滤
    seen = set()
    results = []
    for url in all_matches:
        url = url.replace('\\/', '/')
        if url not in seen and not url.endswith('.gif') and url.startswith('http'):
            seen.add(url)
            results.append(url)
            if len(results) >= count:
                break
    
    return {"query": query, "count": len(results), "images": results, "source": "baidu"}


def search_sogou_images(query, count=5):
    """搜索搜狗图片"""
    encoded = urllib.parse.quote(query)
    url = f"https://pic.sogou.com/pics?query={encoded}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        return {"error": str(e), "source": "sogou"}
    
    # 搜狗图片
    pattern = r'"oriPicUrl":"([^"]+)"'
    matches = re.findall(pattern, html)
    
    seen = set()
    results = []
    for url in matches:
        url = url.replace('\\/', '/')
        if url not in seen and not url.endswith('.gif'):
            seen.add(url)
            results.append(url)
            if len(results) >= count:
                break
    
    return {"query": query, "count": len(results), "images": results, "source": "sogou"}


def search_images(query, count=5):
    """尝试多个搜索引擎"""
    # 先试百度
    result = search_baidu_images(query, count)
    if result.get("images"):
        return result
    
    # 再试搜狗
    result = search_sogou_images(query, count)
    if result.get("images"):
        return result
    
    return {"query": query, "count": 0, "images": [], "error": "No results from any source"}


def download_image(url, output_path):
    """下载图片"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
        
        with open(output_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        return str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: image_search.py search <query> [--count N]")
        print("       image_search.py download <url> --output <path>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        count = 10
        
        if "--count" in sys.argv:
            idx = sys.argv.index("--count")
            if idx + 1 < len(sys.argv):
                count = int(sys.argv[idx + 1])
        
        result = search_images(query, count)
        
        if "error" in result and not result.get("images"):
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        print(f"Found {result['count']} images for '{query}' (source: {result.get('source', 'unknown')}):\n")
        for i, url in enumerate(result['images'], 1):
            print(f"{i}. {url[:100]}{'...' if len(url) > 100 else ''}")
        
        # 输出完整 JSON 到 stderr
        print("\n---JSON---", file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        
    elif cmd == "download":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        output = "downloaded_image.jpg"
        
        if "--output" in sys.argv:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv):
                output = sys.argv[idx + 1]
        
        result = download_image(url, output)
        if result is True:
            print(f"Downloaded to: {output}")
        else:
            print(f"Download failed: {result}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
